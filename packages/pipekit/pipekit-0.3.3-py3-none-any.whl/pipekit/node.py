#!/usr/bin/env python3

import asyncio
from functools import partial
from itertools import chain
from threading import Barrier, Thread

import janus
from box import Box

from . import pipe
from .component import Component, ComponentInterrupted
from .message import Message
from .utils import aiter, isdict, islist


class Node(Component):
    """Processes messages."""

    globals = Box()

    def configure(self, process=None, inbox=None, ifilters=None, ofilters=None, outbox=None,
                  conditions=None, blocking=False, scale=None, **settings):
        if callable(process):
            self.process = process
        self.inbox = self._join_pipes(inbox, Inbox)
        self.ifilters = ifilters or PriorityRegistry()
        self.ofilters = ofilters or PriorityRegistry()
        for filter_ in chain(self.ifilters.values(), self.ofilters.values()):
            filter_.parent = self
        self.outbox = self._join_pipes(outbox, Outbox)
        self.children = [self.inbox, self.outbox]
        self.conditions = conditions or []
        self.blocking = self.__class__ is ThreadedNode or blocking
        self.scale = int(scale or 1)
        self.layers = list()
        self.locals = Box()

        # Used by ProcessorWrapper to control behavior of input feed.
        self.wait_for_pending = True

        self.streams = dict()
        return settings

    def __str__(self):
        process_str = ''
        if not hasattr(self.process, 'stub') and not hasattr(self.process, 'overloaded'):
            process_str = f' {self.process}'
        return f'<{self.type} {self.id}{process_str}>'

    def _join_pipes(self, pipes, class_):
        if not isinstance(pipes, dict):
            pipes = dict(default=pipes)
        msgbox = self.workflow.make_component(class_, id=f'{self.id}.{class_.__name__.lower()}',
                                              parent=self, **pipes)
        return msgbox

    _dependent_statuses = set()

    async def test(self, messages):
        self.debug(f'~~~~~~ begin {messages}')
        async for c, m in messages:
            self.debug(f'~~~~~~ message from {messages} {c} {m}')
            yield c, m
            self.debug(f'~~~~~~ yielded from {messages} {c} {m}')
        self.debug(f'~~~~~~ end {messages}')

    def start(self, *args):
        coroutines = [super().start(*args)]
        self.layers = ([self.inbox] +
                       self.ifilters.ordered() +
                       self.spawn_processor() +
                       self.ofilters.ordered() +
                       [self.outbox])
        for layer in self.layers:
            if isinstance(layer, Component):
                coroutines.append(layer.start())
        return asyncio.gather(*coroutines)

    async def run(self):
        if not self.aborted:
            await super().run()
            conditions = set(self.conditions)
            while self.running and conditions:
                for event in conditions.copy():
                    if self.hasstatus(f'{event.rsplit(":", 1)[0]}:aborted'):
                        self.abort()
                    elif self.hasstatus(event):
                        conditions.remove(event)
                if conditions:
                    await asyncio.sleep(0.1)

        self.status = 'cleared'
        if self.running:
            try:
                await self._run()
            except Exception as exc:
                self.exception('Fatal error')
                self.abort(exc)
                if False and True:  # TODO: make this configurable
                    raise

        if not self.aborted:
            self.status = 'finished'
        self.status = 'exited'

    async def _run(self):
        if not self.running:
            self.debug('*** _run exiting')
            return

        # for layer in self.layers:
        #     if isinstance(layer, Component) and hasattr(layer, 'ready'):
        #         self.debug(f'Waiting on layer {layer} to be ready')
        #         await layer.ready.wait()
        #         self.debug(f'Layer {layer} is ready')
        stack = self.layers[0]
        for layer in self.layers[1:]:
            stack = layer(stack)
            # stack = layer(self.test(stack))
        # async for result in self.test(stack):
        async for result in stack:
            if not self.running:
                break

    def spawn_processor(self):
        # self._processor = self.get_processor()
        # if self.blocking:
        #     raise NotImplementedError(f'Node.blocking in {self}')
        #     # self._processor = ThreadedProcessor(self._processor, scale=self.scale)

        # if self.scale > 1:
        #     self._processor = MultiProcessor(self)

        self._processor = ProcessorWrapper(self)
        return [self._pre_processor, self._processor, self._post_processor]

    async def _pre_processor(self, messages):
        """Generate an event on the first message reaching the processor."""
        first_message = True
        async for channel, message in messages:
            # self.debug(f'*** pre-proc {channel}: {message}')
            if not self.running:
                break

            if first_message:
                self.status = 'processing-started'
                first_message = False
            yield (channel, message)
            # self.debug('*** pre-proc loop')
        # self.debug('*** pre-proc end')

    async def _post_processor(self, messages):
        """Generate an event on the last message leaving the processor."""
        async for channel, message in messages:
            # self.debug(f'*** post-proc {channel}: {message}')
            if not self.running:
                break

            yield (channel, message)
            # self.debug('*** post-proc loop')
        # self.debug('*** post-proc end')
        self.status = 'processing-finished'

    # def get_processor(self):
    #     if isinstance(self, WithRetry):
    #         self._retryable = None
    #         return self._retryable_processor
    #
    #     return self.processor

    # async def _retryable_processor(self, messages, id_=None):
    #     if self._retryable is None:
    #         self._retryable = RetryableMessages(self, messages)
    #     async for channel, message in self.processor(self._retryable, id_):
    #         # self.debug(f'*** _retryable {channel}: {message}')
    #         yield channel, message
    #         # self.debug('*** _retryable loop')
    #     # self.debug('*** _retryable end')

    async def processor(self, messages, id_=None):
        """Process and yield new (channel, message)."""
        async for channel, message in messages:
            yield await self.process(channel, message)

    async def process(self, channel, message):
        raise NotImplementedError(f'process() in {self}')

    process.stub = True

    def drop(self, message):  # TODO: implement message accounting and leak detection
        self._processor.drop(message)

    async def retry(self, channel, message, wait=False):
        """Insert a message back into the input queue for retrying it."""
        await self._processor.retry(channel, message, wait)

    def merged_settings(self, message, key=None, msgmap=None):
        """Return node settings, with values overridden from the message if present."""
        settings = self.settings.to_dict()
        message = message.to_dict()
        if key:
            settings = settings[key]
            message = message[key]
        if msgmap is None:
            msgmap = list(settings)
        if islist(msgmap):
            msgmap = dict(zip(msgmap, msgmap))
        elif not isdict(msgmap):
            raise TypeError(f'Argument msgmap must be a mapping or a sequence, not {type(msgmap)}')

        return Box(settings, **dict((arg, message[msgarg]) for arg, msgarg in msgmap.items()))

    __MISSING__ = object()

    def named_value(self, key, message=None, default=__MISSING__, settings=None):
        """Return `message`'s attribute named by settings' `key` element.

        If `default` is provided, the element will be given this value if
        it doesn't exist yet.

        We use the `__MISSING__` value because `None` is a valid default.

        """
        if settings is None:
            settings = self._settings
        attrs = settings.setdefault('attrs', {})
        if default is not self.__MISSING__:
            attrs.setdefault(key, default)
        if hasattr(message, 'data'):
            return message.data[attrs[key]]


class WithRetry:
    pass


class ProcessorWrapper:
    """Wraps `Node.processor()` to provide retry mechanism and parallelism."""

    def __init__(self, node):
        self.node = node
        self.running = True
        self.exc = None
        # self.processor = self.node.processor

    async def infeed(self, messages):
        """Loop through all messages from the inbox and relay them to the input queue."""
        self.node.debug('*** multi-processor infeed running')
        async for channel, message in messages:
            # TODO: account for dropped messages
            self.node.debug(f'*** multi-processor infeed rcv msg pending={self.pending} {message}')  # noqa: E501
            self.pending[f'{id(message)}-{message.meta.id}'] = message
            self.node.debug(f'*** infeed got {message} from {channel}')
            await self.iqueue.put((channel, message))
            self.node.debug(f'*** infeed put {message} from {channel}')

        if self.pending:
            if self.node.wait_for_pending:
                pending = None
                self.node.debug(f'*** infeed exhausted pending={pending}')
                while self.pending and self.node.running:
                    if pending != len(self.pending):
                        pending = len(self.pending)
                        self.node.debug(f'*** multi-processor infeed waiting pending={pending}')
                    await asyncio.sleep(0.1)
            if self.pending:
                plural = 's' if len(self.pending) != 1 else ''
                self.node.warning(f'ProcessorWrapper exiting with {len(self.pending)} pending '
                                  f'message{plural}')
        self.node.debug('*** infeed stopping collectors')
        self.running = False
        self.node.debug('*** infeed exiting')

    async def _input_iter(self):
        wait = self.iwait
        while self.node.running and self.running:
            queues_are_empty = True
            for queue in (self.rqueue, self.iqueue):
                try:
                    yield queue.get_nowait()

                    queues_are_empty = False
                except asyncio.QueueEmpty:
                    # self.node.debug('*** _input_iter empty')
                    pass

            if queues_are_empty:
                await asyncio.sleep(wait)
                if wait < 0.1:
                    wait *= 2
            else:
                wait = self.iwait

    async def collector(self, id_):
        """Launch an instance of the node processor, and relay its output to the output queue."""
        self.node.debug(f'*** multi-processor collector-{id_} running processor={self.node.processor}')  # noqa: E501
        async for channel, message in self.node.processor(self._input_iter(), id_=id_):
            self.node.debug(f'*** multi-processor collector-{id_} rcv msg {message}')
            await self.oqueue.put((channel, message))
            self.node.debug(f'*** multi-processor collector-{id_} snt msg {message}')
        self.node.debug(f'*** multi-processor collector-{id_} stopped')
        await self.oqueue.put((None, pipe.EOT))
        self.node.debug(f'*** multi-processor collector-{id_} exited')

    async def outfeed(self, messages):
        """Launch all processor instances and return an iterator that feeds on the output queue."""
        self.iqueue = asyncio.Queue(maxsize=self.node.scale)  # input queue
        self.rqueue = asyncio.Queue()                         # retry queue
        self.oqueue = asyncio.Queue(maxsize=1)                # output queue
        self.iwait = 0.001  # initial scaleback wait value for input queue
        # self.finished = asyncio.Event()
        # self.exhausted = False
        self.pending = dict()  # messages currently handled by node processor
        # coroutines = [self.node.loop.create_task(self.infeed(messages))]
        coroutines = list()
        for i in range(self.node.scale):
            # coroutines.append(self.node.loop.create_task(self.collector(i)))
            coroutines.append(asyncio.ensure_future(self.collector(i)))
        coroutines.append(asyncio.ensure_future(self.infeed(messages)))
        running = self.node.scale
        wait = self.iwait

        self.node.debug(f'*** multi-processor outfeed started {running} collectors')
        while running or not self.oqueue.empty():
            if self.oqueue.empty():
                # Raise any exception from collectors.
                for coroutine in coroutines:
                    try:
                        # self.node.debug('*** error?')
                        coroutine.result()
                    except asyncio.InvalidStateError:
                        # self.node.debug('*** nope')
                        pass

                if self.node.hasstatus('aborted'):
                    self.node.debug('*** outfeed aborting')
                    break

                await asyncio.sleep(wait)
                if wait < 0.1:
                    wait *= 2
                continue

            else:
                wait = self.iwait

            self.node.debug(f'*** multi-processor outfeed waiting for msg pending={len(self.pending)}')  # noqa: E501
            channel, message = await self.oqueue.get()
            self.node.debug(f'*** multi-processor outfeed rcv msg pending={len(self.pending)} {message}')  # noqa: E501
            self.oqueue.task_done()
            if message is pipe.EOT:
                running -= 1
                self.node.debug(f'*** multi-processor outfeed collector ended left={running}')
            else:
                self.pending.pop(f'{id(message)}-{message.meta.id}', None)
                # if self.pending == 0 and self.exhausted:
                #     self.node.debug('*** multi-processor outfeed finishing')
                #     # self.finished.set()
                yield channel, message

            self.node.debug(f'*** multi-processor outfeed processed msg pending={len(self.pending)} {message}')  # noqa: E501

        self.node.debug('*** outfeed stopped running')
        self.running = False
        for coroutine in coroutines:
            if self.node.hasstatus('aborted'):
                self.node.debug(f'*** outfeed cancelling {coroutine}')
                coroutine.cancel()
            self.node.debug(f'*** outfeed awaiting {coroutine}')
            try:
                await coroutine
            except asyncio.CancelledError:
                pass

        self.node.debug('*** outfeed all awaited')

    def drop(self, message, component=None):
        """Drop message and stop tracking it."""
        self.pending.pop(f'{id(message)}-{message.meta.id}', None)
        message.drop(component or self.node)

    async def retry(self, channel, message, wait=False):
        """Insert a message back into the input queue for retrying it."""
        self.node.debug(f'Retrying message {message}')
        self.pending[f'{id(message)}-{message.meta.id}'] = message

        async def retry(channel, message, wait):
            if wait:
                await asyncio.sleep(wait)  # tight loop mitigation
            await self.rqueue.put((channel, message))

        if wait is None:
            wait = 0.000001

        # Schedule push to retry queue to free up caller.
        self.node.debug(f'Requeuing message {message}')
        asyncio.ensure_future(retry(channel, message, wait))

    __call__ = outfeed


class Inbox(pipe.Manifold):

    async def receiver(self):
        message = None
        active_channels = 0
        last_channel = False
        self.debug('Ready to receive')
        for channel, _pipe in self._active_channels():
            if not self.running:
                # self.debug('*** NOT running anymore')
                return

            if _pipe is None:
                if active_channels == 1:
                    last_channel = True
                if message is False:  # all channels are empty
                    await asyncio.sleep(0.05)

                message = False
                active_channels = 0
                continue

            active_channels += 1
            try:
                # self.debug(f'*** about to receive message from {channel}')
                message = await self.try_while_running(
                        partial(_pipe.receive, wait=last_channel))
                # self.debug(f'*** received message from {channel}: {message}')
            except asyncio.QueueEmpty:
                # self.debug(f'*** no message to receive from {channel}')
                continue

            except ComponentInterrupted:
                # self.debug('*** receiving interrupted')
                return

            except Exception:
                self.exception(f'Error while receiving on channel {channel}, {_pipe}')
                raise

            self.debug(f'Got message from {channel}: {message}')
            if message == pipe.EOT:
                _pipe.stop()
            else:
                message.checkin(self)
                yield (channel, message)

        self.debug('Finished receiving')

    def _active_channels(self):
        active_channels = self.channels.copy()
        while active_channels:
            yield None, None  # signal start of channels sweep

            for channel, _pipe in active_channels.copy().items():
                if not _pipe.running:
                    self.debug(f'Skipping stopped channel {channel}')
                    del active_channels[channel]
                else:
                    yield channel, _pipe

    # async def Xreceiver(self):
    #     self.debug('Receiving')
    #     self.debug(f'Setting up channels {list(self.channels)}')
    #     # __import__('pudb').set_trace()
    #     # import sys; sys.exit()
    #     feeder = deque()
    #     events = Box(received=asyncio.Event())
    #     # receivers = dict()
    #     for channel, pipe in self._active_channels():
    #         self.debug(f'Setting up channel {channel}')
    #         events[channel] = asyncio.Event()
    #         events[channel].set()
    #         # receivers[channel] = asyncio.ensure_future(
    #         #     self.channel_receiver(channel, feeder, events))
    #         asyncio.ensure_future(self.channel_receiver(channel, feeder, events))
    #
    #     self.debug('Waiting for feeder')
    #     while self.running and (len(feeder) or await events.received.wait()):
    #         for channel in self.channels:
    #             events[channel].clear()
    #         events.received.clear()
    #         channel, message = feeder.popleft()
    #
    #         self.debug(f'Got message from {channel}: {message}')
    #         if message == pipe.EOT:
    #             self.debug('Exhausted channel: %s' % channel)
    #             pipe.stop()
    #             # self.debug(f'* setting event for channel {channel}')
    #             events[channel].set()
    #             # receivers[channel].cancel()
    #             try:
    #                 await pipe.send(pipe.EOT)
    #             except NotImplementedError:
    #                 pass
    #             # self.debug('-----------------------------')
    #             if not list(self._active_channels()):
    #                 self.debug('Stopping: no more active channels')
    #                 self.stop()
    #                 # TODO: cancel channel receiver coroutines
    #                 break
    #         else:
    #             message.checkin(self)
    #             yield channel, message
    #
    #         for channel in self.channels:
    #             events[channel].set()
    #
    #     self.debug('Finished receiving')

    async def channel_receiver(self, channel, feeder, events):
        self.debug(f'Receiver for {channel} is ready')
        pipe = self.channels[channel]
        while pipe.running and self.running and await events[channel].wait():
            # self.debug(f'* receiving from channel {channel}')
            events[channel].clear()
            try:
                feeder.append((channel, await pipe.receive()))
            except Exception:
                self.exception(f'Error while receiving on channel {channel}, {pipe}')
                raise

            # self.debug(f'* received from channel {channel} (next event: {events[channel].is_set()})')  # noqa: E501
            events.received.set()
        self.debug(f'Receiver for {channel} is exiting')

    def X_active_channels(self):
        channels = self.channels.copy()
        while channels:
            for channel, _pipe in channels.copy().items():
                del channels[channel]
                if not _pipe.running:
                    self.debug(f'skipping stopped channel {channel}')
                else:
                    yield channel, _pipe
        if channels:
            pass  # TODO: channel clean-ups


class RetryableMessages:
    """Queue sitting between the inbox and the processor where retries can be inserted back."""

    def __init__(self, node, messages):
        self.node = node
        self.messages = messages
        self._queueiter = None

    def __aiter__(self):
        if self._queueiter is None:  # singleton queueiter, for when we're using MultiProcessor
            self._queueiter = self.queueiter()
        return self._queueiter

    async def infeed(self):
        """Feed the inbox to the queue."""

        async def enqueue(channel, message):
            self.forwarded.clear()
            await self.queue.put((channel, message))
            await self.node.try_while_running(partial(self.forwarded.wait))

        # TODO: implement freeze detection - investigate where messages are stuck
        try:
            async for channel, self.newmsg in self.messages:
                self.node.debug(f'*** retryable: feeding {self.newmsg}')
                await enqueue(channel, self.newmsg)
            self.node.debug(f'*** retryable: main infeed done (pending: {self.pending})')
            while self.node.running and not self._retry_queue.empty():
                channel, self.newmsg = await self._retry_queue.get()
                self.node.debug(f'*** retryable: refeeding {self.newmsg}')
                await enqueue(channel, self.newmsg)
            self.node.debug(f'*** retryable: retry infeed done (pending: {self.pending})')
            self.exhausted = True
            if self.pending > 0:
                self.node.debug(
                        f'RetryableMessages waiting to exit: {self.pending} pending messages')
                await self.node.try_while_running(partial(self.all_processing_done.wait))
            self.node.debug('*** retryable: infeed ready to exit')
        except ComponentInterrupted:
            pass
        finally:
            await self.queue.put(pipe.EOT)
        self.node.debug('*** retryable: infeed exited')

    async def queueiter(self):
        """Turn the queue into an iterator that the processor can consume."""
        self.queue = asyncio.Queue()
        self._retry_queue = asyncio.Queue()
        self.forwarded = asyncio.Event()
        self.all_processing_done = asyncio.Event()
        self.exhausted = False
        self.newmsg = None
        self.pending = 0  # number of messages currently handled by node processor
        infeed = self.node.loop.create_task(self.infeed())
        self.node.debug('*** retryable: infeed created')

        # while self.node.running:
        #     try:
        #         item = await self.node.try_while_running(self.queue.get)
        #         if item == pipe.EOT:
        #             self.queue.task_done()  # for EOT
        #             break
        #
        #         else:
        #             channel, message = item
        #     except ComponentInterrupted:
        #         pass
        #     else:
        #         # self.node.debug(f'*** retryable: forwarding {message.type} msg {message.meta.id}')  # noqa: E501
        #         self.queue.task_done()
        #         if message is self.newmsg:
        #             self.forwarded.set()
        #         self.pending += 1
        #         yield channel, message

        self.node.debug('*** retryable: consuming queue')
        # messages = aiter(self.queue.get, pipe.EOT)
        # try:
        # async for channel, message in messages:
        async for channel, message in aiter(self.queue.get, pipe.EOT):
            self.node.debug(f'*** retryable: forwarding {message}')
            self.queue.task_done()
            if message is self.newmsg:
                self.forwarded.set()
            self.pending += 1
            yield channel, message
            self.node.debug(f'*** retryable: forwarded (pending: {self.pending}) {message}')  # noqa: E501

        self.node.debug('*** retryable: queueiter exiting')
        self.queue.task_done()
        await infeed
        self.node.debug('*** retryable: queueiter exited')

    def processing_done(self):
        """Signal that a message is not in the processor anymore."""
        self.pending -= 1
        if self.exhausted:
            self.all_processing_done.set()

    async def retry(self, channel, message, now=True, wait=0.001, id_=None):
        """Insert a message back into the queue for retrying it."""
        self.node.debug(f'*** retryable: retrying {message}')
        await asyncio.sleep(wait)  # tight loop mitigation
        queue = self.queue if self.exhausted else self._retry_queue
        await queue.put((channel, message))
        self.processing_done()


class Outbox(pipe.Manifold):
    def __call__(self, messages):
        return self._sender(messages)

    async def _sender(self, messages):
        self.debug('Ready to send')
        try:
            async for channel, message in self.sender(messages):
                yield channel, message

        except Exception:
            self.error(f'*** outbox {self.id} caught an exception')
            self.status = 'aborted'
            # self.exception('Node failure')
            raise

        else:
            self.status = 'finished'
        finally:
            self.status = 'exited'

    async def sender(self, messages):
        async for channel, message in messages:
            channel = channel or 'default'
            self.debug(f'*** got msg   {channel}: {message} [{self.channels[channel].id}]')  # noqa: E501
            if not self.running:
                break

            if channel is Message.DROP:
                self.debug(f'*** dropping message: {message}')
                self.parent.drop(message)
            else:
                self.debug(f'Sending message to {channel}: {message}')
                if channel in self.channels:
                    try:
                        await self.try_while_running(partial(self.channels[channel].send, message))
                    except ComponentInterrupted:
                        self.debug(f'*** aborted sending message to {channel}: {message}')
                        break

                    self.debug(f'*** sent to   {channel}: {message} [{self.channels[channel].id}]')  # noqa: E501
                    message.checkout(self)
                    self.debug(f'*** yielding  {channel}: {message}')
                    yield channel, message

                    self.debug(f'*** yielded   {channel}: {message}')
                else:
                    raise KeyError(f'Channel "{channel}" does not exist in {self}')

        self.debug('Finished sending')
        try:
            for _pipe in self.channels.values():
                self.debug(f'*** sending {pipe.EOT} to {_pipe}')
                await self.try_while_running(partial(_pipe.send, pipe.EOT))
        except ComponentInterrupted:
            self.debug(f'*** aborted sending {pipe.EOT} to {_pipe}')
            pass


class ThreadedNode(Node):
    pass


class ThreadedProcessor:
    def __init__(self, processor, scale):
        self.processor = processor
        self.scale = scale
        self.iqueue = janus.Queue(maxsize=self.scale)
        self.oqueue = janus.Queue(maxsize=self.scale)
        self.barrier = Barrier(self.scale)

    async def __call__(self, messages):
        async for channel, message in self.run_threads(messages):
            yield channel, message

    async def run_threads(self, messages):
        asyncio.ensure_future(self.thread_feeder(messages))
        self.threads = dict((i, Thread(target=self.thread_consumer, args=(i,)).start())
                            for i in range(self.scale))
        queue_iter = aiter(self.oqueue.async_q.get, (None, pipe.EOT))
        async for channel, message in queue_iter:
            self.oqueue.async_q.task_done()
            yield channel, message

        # Empty queue of threads' EOTs
        for i in range(self.scale):
            if i:  # skip the one already consumed by aiter above
                await self.oqueue.async_q.get()
            self.oqueue.async_q.task_done()
            # print(f'thread {i} EOT received back')

        while self.threads:  # FIXME: join threads instead, and move or retire del self.threads[]
            asyncio.sleep(0.1)  # ... while at it, catch exceptions and clean up queue with task_done  # noqa: E501
        # print(f'all threads stopped')

    async def thread_feeder(self, messages):
        async for (channel, message) in messages:
            # TODO: recreate dead threads, report thread failures
            await self.iqueue.async_q.put((channel, message))
        for i in range(self.scale):
            await self.iqueue.async_q.put((None, pipe.EOT))
            # print(f'thread {i} EOT sent')

    def thread_consumer(self, threadnum):  # runs in thread
        # print(f'thread {threadnum} started')
        queue_iter = iter(self.iqueue.sync_q.get, (None, pipe.EOT))
        for channel, message in self.processor(queue_iter):
            self.iqueue.sync_q.task_done()
            self.oqueue.sync_q.put((channel, message))
        # print(f'thread {threadnum} EOT received')
        self.iqueue.sync_q.task_done()  # for EOT which does not make it past queue iterator
        # print(f'thread {threadnum} task done')
        self.barrier.wait()
        self.oqueue.sync_q.put((None, pipe.EOT))  # TODO: use threading.Event to send just one
        # print(f'thread {threadnum} EOT sent back')
        del self.threads[threadnum]
        # print(f'thread {threadnum} stopped')


class PriorityRegistry(dict):
    def ordered(self):
        return [item for _, item in sorted(self.items())]


class CmdRunner:

    async def runcmd(self, *args, raise_=True, **kwargs):
        try:
            proc = await asyncio.create_subprocess_exec(
                *map(str, args), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                **kwargs)
            await proc.wait()
            exitcode = await proc.wait()
            stdout = (await proc.stdout.read()).decode()
            stderr = (await proc.stderr.read()).decode()
            if exitcode:
                raise RuntimeError(f'Command {args} ({kwargs}) returned with exitcode {exitcode}, '
                                   f'stdout: {stdout or None}, stderr: {stderr or None}')

        except Exception as e:
            self.logger.exception(f'Error running command: {e}')
            if raise_:
                raise

        return exitcode, stdout, stderr

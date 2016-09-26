import asyncio

from .connection.input import Input
from .connection.output import Output
from .connection.connection_set import ConnectionSet


class TestHelper:
    def __init__(self, stream, timeout=5):
        ins = [Input(in_) for in_ in stream.ins]
        outs = [Output(out) for out in stream.outs]
        self.sinks = [Input(out) for out in stream.outs]
        for out, sink in zip(outs, self.sinks):
            out.pipe(sink)
        self.ins = ConnectionSet(ins)
        self.outs = ConnectionSet(outs)
        self.stream = stream
        self._timeout = timeout
        self._loop = asyncio.get_event_loop()

    def run(self, ins={}):
        for key, value in ins.items():
            self.ins[key]._queue.extend(value)
            self.ins[key].close()
        task = self._loop.create_task(self.stream.run(self.ins, self.outs))
        self._loop.run_until_complete(asyncio.wait_for(task, self._timeout, loop=self._loop))
        return {sink.name: list(sink._queue) for sink in self.sinks}

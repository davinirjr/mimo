from .connection.input import Input
from .connection.output import Output
from .connection.connection_set import ConnectionSet


class TestHelper:
    def __init__(self, stream):
        ins = [Input(in_) for in_ in stream.ins]
        outs = [Output(out) for out in stream.outs]
        self.ins = ConnectionSet(ins)
        self.outs = ConnectionSet(outs)
        self.stream = stream

    def run(self, ins):
        for key, value in ins.items():
            self.ins[key].clear()
            self.ins[key].extend(value)
        outs = {out.name: [] for out in self.outs}
        while self.stream.run(self.ins, self.outs):
            for out in self.outs:
                outs[out.name].extend(out.entities)
                out.clear()
        return outs

from mimo.stream import Stream


class ApplyStream(Stream):

    IN = ['entity']
    OUT = ['entity']

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self, ins, outs):
        fn = self.fn
        while len(ins.entity) > 0 and outs.entity.push(fn(ins.entity.pop())):
            continue
        return len(ins.entity) > 0

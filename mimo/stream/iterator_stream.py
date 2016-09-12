from mimo.stream import Stream


class IteratorStream(Stream):

    IN = []
    OUT = ['line']

    def __init__(self, iterator):
        super().__init__()
        self.iterator = iterator

    def run(self, ins, outs):
        for line in self.iterator:
            if not outs.line.push(line):
                return True
        return False

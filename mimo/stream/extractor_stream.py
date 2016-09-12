from mimo.stream import Stream


class ExtractorStream(Stream):

    IN = ['entity']
    OUT = ['entity']

    def __init__(self, path, ins, outs):
        super().__init__(ins, outs)
        self.path = path

    def run(self, ins, outs):
        path = self.path
        while len(ins.entity) > 0:
            entity = ins.entity.pop()
            for step in path:
                entity = step(entity)
            if not outs.entity.push(entity):
                break
        return len(ins.entity) > 0

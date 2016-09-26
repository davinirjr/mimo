class AsynchronousZip:
    def __init__(self, *iterables):
        self._iterables = iterables

    def __aiter__(self):
        return self

    async def __anext__(self):
        res = []
        for iterator in self._iterables:
            res.append(await iterator.__anext__())
        return tuple(res)

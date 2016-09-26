class AsynchronousRange:
    def __init__(self, fr, to=None, step=1):
        if to is None:
            self._iterator = iter(range(fr))
        else:
            self._iterator = iter(range(fr, to, step))

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._iterator)
        except StopIteration:
            raise StopAsyncIteration

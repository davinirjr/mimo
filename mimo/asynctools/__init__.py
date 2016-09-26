from .range import AsynchronousRange
from .zip import AsynchronousZip


def azip(*iterables):
    return AsynchronousZip(*iterables)


def arange(fr, to=None, step=1):
    return AsynchronousRange(fr, to, step)

from mimo.connection import Connection, ConnectionSet


class Stream:

    IN = []
    OUT = []

    def __init__(self, ins=None, outs=None, name=None):
        self.paused = False

        ins = self.IN if ins is None else ins
        outs = self.OUT if outs is None else outs
        self.ins = ConnectionSet(Connection(name) for name in ins)
        self.outs = ConnectionSet(Connection(name) for name in outs)
        self.children = {out: set() for out in outs}
        self.name = type(self).__name__ if name is None else name

    def run(self, ins, outs):
        """
        The main method to over-ride when implementing custom streams.
        :param ins: connection set of input connections
        :type ins: ConnectionSet
        :param outs: connection set of output connections
        :type outs: ConnectionSet
        :return: True if stream is paused
        """
        raise NotImplementedError

    def activate(self):
        """
        Run a step and propogate the output entities to any connected child streams.
        :return:
        """
        run = self.run
        ins = self.ins
        outs = self.outs
        children = self.children

        paused = True
        while paused:
            paused = run(ins, outs)
            updated_streams = set()
            for streams in children.values():
                updated_streams.update(stream for stream in streams if stream.paused)
            for out in outs.drain():
                updated_streams.update(children[out])
            for updated_stream in updated_streams:
                updated_stream.activate()
        self.paused = paused

    def pipe(self, stream, output=None, input=None):
        """
        Pipe the output of one stream to the input of another. If there are more than one outputs or inputs, the
        specific output/input must be specified.
        :param stream: stream to connect to
        :param output: name of the output connection (default: None)
        :param input: name of the input connection (default: None)
        :return: stream connected to
        """
        if len(self.outs) == 0:
            raise ValueError('{} has no output to pipe from'.format(self.name))
        elif len(stream.ins) == 0:
            raise ValueError('{} has no input to pipe to'.format(stream.name))

        if output is None:
            if len(self.outs) == 1:
                from_connection = next(iter(self.outs))
            else:
                raise ValueError('{} has multiple output and none chosen to pipe from'.format(self.name))
        else:
            from_connection = self.outs[output]

        if input is None:
            if len(stream.ins) == 1:
                to_connection = next(iter(stream.ins))
            else:
                raise ValueError('{} has multiple output and none chosen to pipe from'.format(stream.name))
        else:
            to_connection = stream.ins[input]

        from_connection.join(to_connection)
        self.children[from_connection.name].add(stream)
        return stream

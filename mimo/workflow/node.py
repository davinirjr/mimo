class Node:
    __slots__ = ('workflow', 'stream_id', 'input_ids', 'output_ids')

    def __init__(self, workflow, stream_id, input_ids, output_ids):
        self.workflow = workflow
        self.stream_id = stream_id
        self.input_ids = input_ids
        self.output_ids = output_ids

    def pipe(self, step, output=None, input=None):
        """
        Pipe the output of one stream to the input of another. If there are more than one outputs or inputs, the
        specific output/input must be specified.
        :param step: stream to connect to
        :param output: name of the output connection (default: None)
        :param input: name of the input connection (default: None)
        :return: stream connected to
        """
        if len(self.output_ids) == 0:
            raise ValueError('{} has no output to pipe from'.format(self.workflow.streams[self.stream_id]))
        elif len(step.input_ids) == 0:
            raise ValueError('{} has no input to pipe to'.format(self.workflow.streams[step.stream_id]))

        if output is None:
            if len(self.output_ids) == 1:
                output_id = next(iter(self.output_ids.values()))
            else:
                msg = '{} has multiple output and none chosen to pipe from'
                raise ValueError(msg.format(self.workflow.streams[self.stream_id]))
        else:
            output_id = self.output_ids[output]

        if input is None:
            if len(step.input_ids) == 1:
                input_id = next(iter(step.input_ids.values()))
            else:
                msg = '{} has multiple input and none chosen to pipe to'
                raise ValueError(msg.format(self.workflow.streams[step.stream_id]))
        else:
            input_id = step.input_ids[input]

        self.workflow.graph.add_edge(output_id, input_id)
        self.workflow.outputs[output_id].pipe(self.workflow.inputs[input_id])
        return step

    def push(self, item, input=None):
        if input is None:
            if len(self.input_ids) == 1:
                input_id = next(iter(self.input_ids.values()))
            else:
                msg = '{} has multiple input and none chosen to push to'
                raise ValueError(msg.format(self.workflow.streams[self.stream_id]))
        else:
            input_id = self.input_ids[input]

        self.workflow.inputs[input_id].put_nowait(item)

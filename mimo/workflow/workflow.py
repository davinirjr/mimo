from collections import deque
from uuid import uuid4
from lhc.graph import NPartiteGraph
from mimo.connection.input import Input
from mimo.connection.output import Output
from mimo.connection.connection_set import ConnectionSet
from .node import Node


class Workflow:
    def __init__(self, threshold=100):
        self.graph = NPartiteGraph(n=3)

        self.streams = {}
        self.input_sets = {}
        self.output_sets = {}
        self.inputs = {}
        self.outputs = {}

        self.threshold = threshold

    def __str__(self):
        graph = self.graph
        res = ['digraph {} {{'.format(graph.name)]
        partitions = [self.streams, self.inputs, self.outputs]
        for i, partition, shape in zip(range(3), graph.partitions, graph.shapes):
            for vertex in partition:
                res.append('    "{}" [shape={},label="{}"];'.format(vertex, shape, partitions[i][vertex].name))
        for fr, to in sorted(graph.graph.es):
            res.append('    "{}" -> "{}";'.format(fr, to))
        res.append('}')
        return '\n'.join(res)

    def run(self):
        stacked = set(self._get_head_streams()) | set(self._get_streams_with_input())
        stack = deque(stacked)
        while len(stack) > 0:
            stream_id = stack.popleft()
            stacked.remove(stream_id)
            stream = self.streams[stream_id]
            paused = stream.run(self.input_sets[stream_id], self.output_sets[stream_id])

            output_ids = self.graph.get_children(stream_id)
            for output_id in output_ids:
                output = self.outputs[output_id]
                input_ids = self.graph.get_children(output_id)
                inputs = [self.inputs[input_id] for input_id in input_ids]
                if any(input.is_full() for input in inputs):
                    continue
                for input in inputs:
                    input.extend(output.entities)
                output.entities.clear()
                for input_id in input_ids:
                    stream_ids = self.graph.get_children(input_id)
                    stack.extend(stream_id for stream_id in stream_ids if stream_id not in stacked)
                    stacked.update(stream_ids)
            if paused:
                stack.append(stream_id)
                stacked.add(stream_id)

    def add_stream(self, stream):
        stream_id, input_ids, output_ids = self._get_identifiers(stream)
        self._add_vertices(stream, stream_id, input_ids, output_ids)
        self._add_edges(stream_id, input_ids, output_ids)
        return Node(self, stream_id, input_ids, output_ids)

    def _get_head_streams(self):
        for stream_id in self.graph.partitions[0]:
            if len(self.graph.get_parents(stream_id)) == 0:
                yield stream_id

    def _get_streams_with_input(self):
        inputs = self.inputs
        for stream_id in self.graph.partitions[0]:
            input_ids = self.graph.get_parents(stream_id)
            if any(len(inputs[input_id]) > 0 for input_id in input_ids):
                yield stream_id

    def _get_identifiers(self, stream):
        return str(uuid4())[:8],\
               {name: str(uuid4())[:8] for name in stream.ins},\
               {name: str(uuid4())[:8] for name in stream.outs}

    def _add_vertices(self, stream, stream_id, input_ids, output_ids):
        self.streams[stream_id] = stream
        self.input_sets[stream_id] = ConnectionSet(Input(name, self.threshold) for name in stream.ins)
        self.output_sets[stream_id] = ConnectionSet(Output(name, self.threshold) for name in stream.outs)

        self.graph.add_vertex(stream_id, 0)
        for input, input_id in input_ids.items():
            self.inputs[input_id] = self.input_sets[stream_id][input]
            self.graph.add_vertex(input_id, 1)
        for output, output_id in output_ids.items():
            self.outputs[output_id] = self.output_sets[stream_id][output]
            self.graph.add_vertex(output_id, 2)

    def _add_edges(self, stream_id, input_ids, output_ids):
        for input, in_id in input_ids.items():
            self.graph.add_edge(in_id, stream_id)
        for output, out_id in output_ids.items():
            self.graph.add_edge(stream_id, out_id)

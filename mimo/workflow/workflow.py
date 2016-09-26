import asyncio

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
        loop = asyncio.get_event_loop()
        tasks = [stream.run(self.input_sets[stream_id], self.output_sets[stream_id])
                 for stream_id, stream in self.streams.items()]
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

    def add_stream(self, stream):
        stream_id, input_ids, output_ids = self._get_identifiers(stream)
        self._add_vertices(stream, stream_id, input_ids, output_ids)
        self._add_edges(stream_id, input_ids, output_ids)
        return Node(self, stream_id, input_ids, output_ids)

    def _get_identifiers(self, stream):
        return str(uuid4())[:8],\
               {name: str(uuid4())[:8] for name in stream.ins},\
               {name: str(uuid4())[:8] for name in stream.outs}

    def _add_vertices(self, stream, stream_id, input_ids, output_ids):
        self.streams[stream_id] = stream
        self.input_sets[stream_id] = ConnectionSet(Input(name, self.threshold) for name in stream.ins)
        self.output_sets[stream_id] = ConnectionSet(Output(name) for name in stream.outs)

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

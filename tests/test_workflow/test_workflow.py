import unittest

from mimo import Workflow, Stream


class TestWorkflow(unittest.TestCase):
    def test_run(self):
        workflow = Workflow()
        stream1 = Stream(outs=['entity'], fn=iterator_stream)
        stream2 = Stream(ins=['entity'], fn=collect_stream)
        step1 = workflow.add_stream(stream1)
        step2 = workflow.add_stream(stream2)
        step1.pipe(step2)

        workflow.run()

        self.assertIn('collection', stream2.state)
        self.assertEqual(list(range(100)), stream2.state['collection'])

    def test_add_stream(self):
        stream = Stream(['a'], ['b'])
        workflow = Workflow()
        node = workflow.add_stream(stream)

        self.assertEqual({node.stream_id: stream}, workflow.streams)
        self.assertEqual(stream.ins, list(conn.name for conn in workflow.inputs.values()))
        self.assertEqual(stream.outs, list(conn.name for conn in workflow.outputs.values()))
        self.assertEqual(workflow, node.workflow)
        self.assertIn(node.stream_id, workflow.streams)
        self.assertEqual(set(workflow.inputs), set(node.input_ids.values()))
        self.assertEqual(set(workflow.outputs), set(node.output_ids.values()))

    def test_get_head_streams(self):
        workflow = Workflow()
        stream1 = Stream(outs=['a'])
        stream2 = Stream(outs=['b'])
        stream3 = Stream(['c', 'd'], ['e'])
        step1 = workflow.add_stream(stream1)
        step2 = workflow.add_stream(stream2)
        step3 = workflow.add_stream(stream3)
        step1.pipe(step3, input='c')
        step2.pipe(step3, input='d')

        heads = set(workflow._get_head_streams())

        self.assertEqual({step1.stream_id, step2.stream_id}, heads)

    def test_get_streams_with_input(self):
        workflow = Workflow()
        stream1 = Stream(['a'])
        stream2 = Stream(['b'])
        step1 = workflow.add_stream(stream1)
        workflow.add_stream(stream2)

        workflow.input_sets[step1.stream_id].a.entities.extend([1, 2, 3])
        nodes_with_input = set(workflow._get_streams_with_input())

        self.assertEqual({step1.stream_id}, nodes_with_input)


def iterator_stream(ins, outs, state):
    if 'iterator' not in state:
        state['iterator'] = iter(range(100))
    iterator = state['iterator']
    for item in iterator:
        if not outs.entity.push(item):
            return True


def collect_stream(ins, outs, state):
    if 'collection' not in state:
        state['collection'] = []
    collection = state['collection']
    while len(ins.entity) > 0:
        collection.append(ins.entity.pop())


if __name__ == '__main__':
    unittest.main()

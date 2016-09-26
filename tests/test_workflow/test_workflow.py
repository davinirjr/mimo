import unittest

from mimo import Workflow, Stream


class TestWorkflow(unittest.TestCase):
    def test_run(self):
        workflow = Workflow()
        stream1 = Stream(outs=['entity'], fn=iterator_stream)
        stream2 = Stream(ins=['entity'], fn=collect_stream, state=[])
        step1 = workflow.add_stream(stream1)
        step2 = workflow.add_stream(stream2)
        step1.pipe(step2)

        workflow.run()

        self.assertEqual(list(range(100)), stream2.state)

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


async def iterator_stream(ins, outs, state):
    for item in iter(range(100)):
        await outs.entity.push(item)
    outs.entity.close()


async def collect_stream(ins, outs, state):
    async for item in ins.entity:
        state.append(item)


if __name__ == '__main__':
    unittest.main()

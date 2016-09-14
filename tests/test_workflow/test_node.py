import unittest

from mimo import Workflow, Stream


class TestStep(unittest.TestCase):
    def test_pipe(self):
        workflow = Workflow()
        step1 = workflow.add_stream(Stream(['a'], ['b']))
        step2 = workflow.add_stream(Stream(['c'], ['d']))

        step1.pipe(step2)

        self.assertEqual(2, len(workflow.streams))
        self.assertIn(step2.input_ids['c'], workflow.graph.graph.adjacency[step1.output_ids['b']].children)


if __name__ == '__main__':
    unittest.main()

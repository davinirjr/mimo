from mimo import Workflow, Stream


def main():
    workflow = Workflow(10)
    step1 = workflow.add_stream(Stream(outs=['a'], fn=stream1))
    step2 = workflow.add_stream(Stream(outs=['b'], fn=stream2))
    step3 = workflow.add_stream(Stream(['c', 'd'], fn=stream3))

    step1.pipe(step3, input='c')
    step2.pipe(step3, input='d')

    print(str(workflow))
    workflow.run()


def stream1(ins, outs, state):
    """
    Generates integers from 0 to 99.
    """
    if 'iterator' not in state:
        state['iterator'] = iter(range(100))
    iterator = state['iterator']
    for item in iterator:
        if not outs.a.push(item):
            return True


def stream2(ins, outs, state):
    """
    Generates integers from 99 to 0.
    """
    if 'iterator' not in state:
        state['iterator'] = iter(range(99, -1, -1))
    iterator = state['iterator']
    for item in iterator:
        if not outs.b.push(item):
            return True


def stream3(ins, outs, state):
    """
    Divide incoming entities by 10 and print to stdout
    """
    while len(ins.c) > 0 and len(ins.d) > 0:
        sys.stdout.write('{}\n'.format(ins.c.pop() + ins.d.pop()))

if __name__ == '__main__':
    import sys
    sys.exit(main())

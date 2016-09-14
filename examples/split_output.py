from mimo import Workflow, Stream


def main():
    workflow = Workflow(10)
    step1 = workflow.add_stream(Stream(outs=['a'], fn=stream1))
    step2 = workflow.add_stream(Stream(['b'], fn=stream2))
    step3 = workflow.add_stream(Stream(['c'], fn=stream3))

    step1.pipe(step2)
    step1.pipe(step3)

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
    Multiply incoming entities by 2 and print to stdout
    """
    while len(ins.b) > 0:
        sys.stdout.write('{}\n'.format(2 * ins.b.pop()))


def stream3(ins, outs, state):
    """
    Divide incoming entities by 10 and print to stdout
    """
    while len(ins.c) > 0:
        sys.stdout.write('{}\n'.format(ins.c.pop() / 10))

if __name__ == '__main__':
    import sys
    sys.exit(main())

from mimo import Workflow, Stream


def main():
    workflow = Workflow(10)
    step1 = workflow.add_stream(Stream(outs=['a'], fn=stream1))
    step2 = workflow.add_stream(Stream(['b'], ['c'], fn=stream2))
    step3 = workflow.add_stream(Stream(['d'], fn=stream3))

    step1.pipe(step2).pipe(step3)

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
    Multiplies the integers by 2.
    """
    while len(ins.b) > 0:
        item = ins.b.pop()
        if not outs.c.push(item * 2):
            break
    return len(ins.b) > 0


def stream3(ins, outs, state):
    """
    Print incoming entities to stdout
    """
    while len(ins.d) > 0:
        print(ins.d.pop())

if __name__ == '__main__':
    import sys
    sys.exit(main())

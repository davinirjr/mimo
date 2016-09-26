from mimo import Workflow, Stream, azip


def main():
    workflow = Workflow(10)
    step1 = workflow.add_stream(Stream(outs=['a'], fn=stream1))
    step2 = workflow.add_stream(Stream(outs=['b'], fn=stream2))
    step3 = workflow.add_stream(Stream(['c', 'd'], fn=stream3))

    step1.pipe(step3, input='c')
    step2.pipe(step3, input='d')

    print(str(workflow))
    workflow.run()


async def stream1(ins, outs, state):
    """
    Generates integers from 0 to 99.
    """
    for item in iter(range(100)):
        await outs.a.push(item)
    outs.a.close()


async def stream2(ins, outs, state):
    """
    Generates integers from 99 to 0.
    """
    for item in iter(range(99, -1, -1)):
        await outs.b.push(item)
    outs.b.close()


async def stream3(ins, outs, state):
    """
    Divide incoming entities by 10 and print to stdout
    """
    async for c, d in azip(ins.c, ins.d):
        sys.stdout.write('{}\n'.format(c + d))

if __name__ == '__main__':
    import sys
    sys.exit(main())

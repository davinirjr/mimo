from mimo import Workflow, Stream


def main():
    workflow = Workflow(10)
    step1 = workflow.add_stream(Stream(outs=['a'], fn=stream1))
    step2 = workflow.add_stream(Stream(['b'], ['c'], fn=stream2))
    step3 = workflow.add_stream(Stream(['d'], fn=stream3))

    step1.pipe(step2).pipe(step3)

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
    Multiplies the integers by 2.
    """
    async for item in ins.b:
        await outs.c.push(item * 2)
    outs.c.close()


async def stream3(ins, outs, state):
    """
    Print incoming entities to stdout
    """
    async for item in ins.d:
        print(item)

if __name__ == '__main__':
    import sys
    sys.exit(main())

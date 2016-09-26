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


async def stream1(ins, outs, state):
    """
    Generates integers from 0 to 99.
    """
    for item in iter(range(100)):
        await outs.a.push(item)
    outs.a.close()


async def stream2(ins, outs, state):
    """
    Multiply incoming entities by 2 and print to stdout
    """
    async for item in ins.b:
        sys.stdout.write('{}\n'.format(2 * item))


async def stream3(ins, outs, state):
    """
    Divide incoming entities by 10 and print to stdout
    """
    async for item in ins.c:
        sys.stdout.write('{}\n'.format(item / 10))

if __name__ == '__main__':
    import sys
    sys.exit(main())

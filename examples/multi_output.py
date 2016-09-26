from mimo import Workflow, Stream


def main():
    workflow = Workflow(10)
    step1 = workflow.add_stream(Stream(outs=['a', 'b'], fn=stream1))
    step2 = workflow.add_stream(Stream(['c'], fn=stream2))
    step3 = workflow.add_stream(Stream(['d'], fn=stream3))

    step1.pipe(step2, 'a')
    step1.pipe(step3, 'b')

    print(str(workflow))
    workflow.run()


async def stream1(ins, outs, state):
    """
    Generates one stream of integers from 0 to 99 and another from 100 to 1
    """
    for item in iter(range(100)):
        await outs.a.push(item)
        await outs.b.push(100 - item)
    outs.a.close()
    outs.b.close()


async def stream2(ins, outs, state):
    """
    Multiply incoming entities by 2 and print to stdout
    """
    async for item in ins.c:
        sys.stdout.write('{}\n'.format(2 * item))


async def stream3(ins, outs, state):
    """
    Divide incoming entities by 10 and print to stdout
    """
    async for item in ins.d:
        sys.stdout.write('{}\n'.format(item / 10))

if __name__ == '__main__':
    import sys
    sys.exit(main())

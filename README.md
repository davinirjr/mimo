[![Build Status](https://travis-ci.org/childsish/mimo.svg?branch=master)](https://travis-ci.org/childsish/mimo)

mimo
====

+ Multiple input and multiple output (as opposed to functions where inputs and outputs are always synchronised) 
* Less memory (because of streaming)

MiMo is a multi-input multi-output Python streaming library. It allows users to define a stream with multiple inputs and multiple outputs and run them completely from beginning to end. Back-pressure has also been implemented to prevent too much memory from being used.

Usage
-----

There are two core components in MiMo; the `Stream` and the `Workflow`. Streams to the computational processing but do not handle how the data is passed between streams. Workflows pass the data around streams but do no processing of their own. To create a workflow, the user needs to implement streams and pipe them together.

### Streams

Implementing a stream can be done through inheriting a sub-class from the `Stream` class or creating a `Stream`class with a custom function as the `fn` parameter. The following code shows the same implementation of a stream that will produce the numbers from 0 to 99.


```python
from mimo import Stream


# Method 1 (inheritance)

class MyStream(Stream):

    IN = []
    OUT = ['entity']

    def __init__(self):
        super().__init__()
        self.iterator = None
    
    def run(self, ins, outs):
        if self.iterator is None:
            self.iterator = iter(range(100))
        for item in self.iterator:
            if not outs.entity.pueh(item):
                return True


# Method 2 (constructor)

my_stream = Stream(outs=['entity], fn=my_stream_fn)

def my_stream_fn(ins, outs, state):
    if 'iterator' not in state:
        state['iterator'] = iter(range(100))
    for item in state['iterator']:
        if not outs.entity.push(item):
            return True
```

There are a few things to note about the `run` function.
1. It takes two parameters, `ins` and `outs`, that contain the input streams and the output streams. The names of the input and output streams are defined by the `IN` and `OUT` member variables and accessing the input and output streams can be done through the attributes. From the example above, accessing the `entity` output stream can be done with `outs.entity`.
2. Input streams can be popped and peeked. Input streams haven't been used in the above example, but the entities in the stream can be accessed one at a time with the functions `pop` and `peek`. Popping an entity will remove it from the input stream, and peeking will look at the top-most entity without removing it from the stream.
2. Output streams can be pushed. Pushing an entity to an output stream will make it available to any connected downstream streams. The `push` function return a boolean to indicate whether the stream is full or not (`True` if still pushable). A full stream ca still be pushed to, but users can make their custom streams back-pressure aware by testing this value.
3. The return value is a boolean. If a stream did not fully complete it's task (possibly due to back-pressure), then it should return `True` to indicate that it can be run again after downstream streams have completed. Otherwise a `False` (or equivalent like `None`) will prevent further execution of the stream until new input is available. 

### Workflows

Workflows are created by piping streams together. First a workflow must be instantiated and populated with the desired streams. The steps returned by populating a workflow can then be used to make the connections between the streams using the `pipe` function. The function returns the stream being piped to, so `pipe` calls can be chained.

```python
from mimo import Stream, Workflow


def main():
    workflow = Workflow()
    step1 = workflow.add_stream(Stream(outs=['a']))
    step2 = workflow.add_stream(Stream(['b'], ['c']))
    step3 = workflow.add_stream(Stream(['d']))
    
    step1.pipe(step2).pipe(step3)
    
    print(str(workflow))
    workflow.run()

if __name__ == '__main__':
    import sys
    sys.exit(main())
```

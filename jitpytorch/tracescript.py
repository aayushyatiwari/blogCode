import torch as t


def fn(x):
    for _ in range(x.dim()):
        x = x * x
    return x

scriptfn = t.jit.script(fn)
trace_fn = t.jit.trace(fn, [t.randn(5, 5)])


print(scriptfn.code)
print( " ------- ")
print(trace_fn.code)

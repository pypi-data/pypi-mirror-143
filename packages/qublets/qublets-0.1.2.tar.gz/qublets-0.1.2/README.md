Qublets
===

Qublets is an approachable Quantum Computing Library written in Python using Intel's [intel-qs](https://github.com/iqusoft/intel-qs) Quantum Computing Simulator. The goal of the library is to make introductory quantum computing approachable at the undergraduate (or lower) level.

Setup
---

Qublets is supposed to eliminate the hassle most other quantum computing libraries come with, but the setup is still a work in progress.

You will need [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) installed to proceed. Verify successful installation by checking that `which python` returns an anaconda path prior to attempting any qublets (intel-qs) setup.

If you're on Unix (including OS X), you should be able to get going by running [`manual-setup.sh`](./manual-setup.sh) and waiting a while. If you're on Windows, you can still do that by using [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) (highly recommended).

If you'd like to DIY, simply follow the [build instructions](https://github.com/iqusoft/intel-qs#build-instructions) for [intel-qs](https://github.com/iqusoft/intel-qs). Qublets is a python3 wrapper around it.

Getting Started
---

Qublets makes it easy to run simple quantum examples. Consider the classic "Superposition qubit" case:

```python
from qublets import QUInt

result = QUInt.zeros(1).hadamard().measure()
print(result)
```

As you can see, Qublets aims to be as readable as possible (although you can customize quite a bit later). Running the code above will yield a `1` 50% of the cases and a `0` the rest. That's it. You may also notice (most) Qublets operators are chainable and will return the object they operated on - this makes building circuits a breeze.

If you're familiar with quantum state names, you can make the above example even shorter by using a `|+〉`state:

```python
from qublets import QUInt

result = QUInt.pluses(1).measure()
print(result)
```

You may have noticed Qublets supports integers natively - in fact, it supports both unsigned and signed integers of any given size (that your computer can work with without combusting in flames). The example above easily generalizes to a 4-bit QInt:

```python
from qublets import QInt

result = QInt.pluses(4).measure()
print(result)
```
Now, you'd instead get a (mostly) uniformly random number between `-8` and `7`.

It wouldn't really be a quantum computing library if we didn't entangle some bits so let's do that quickly:
```python
from qublets import QUInt

q1 = QUInt.zeros(2)
q1[0].hadamard()
q1[1].c_negate(on=q1[0])
print(q1.measure())

# Or, just like before, we can use a shortcut
print(QUInt.fully_entangled(2).measure())
```

If you're familiar with quantum computing's ABCs, you'd likely be happy to see only `0` and `3` as the possible values of the measurements. That's because the classic `had`/`cnot` combo will give us a perfect `|Φ+〉`state (a bell pair) to work with. `fully_entangled`, on the other hand, will always entangle all the bits in a `QInt` using a chain of `cnot`s - which would be equivalent for only 2 bits.

Qublets also supports cross-q(u)int operations, built-in primitives, batch runs for your circuits, extracting probability amplitudes and more - you can find some inspirational samples in [docs/examples/](./docs/examples/)
# Gravitum

Gravitum is a library for implementing decompiled code with Python.

## Requirements

- Python 3.6+

## Installation

```
$ pip install gravitum
```

## Usage

Gravitum defines some int types (`int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`) which based on the int types of [numpy](https://github.com/numpy/numpy), and fixed the type conversion problem caused by the operation between numpy int and base int.

```python
from gravitum.types import int8, uint8, uint16, uint32

v1 = int8(1)
v2 = uint8(2)
v3 = uint16(3)

# int8
type(v1 + 1)
# uint8
type(v1 + v2)
# uint16
type(v1 + v3)
# cast type
v3 = uint32(v3)
```

Function `ptr` is provided to wrap `bytearray` , then you can operate like a pointer.

For a C program:

```c
unsigned __int8 v[12] = {1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12};
*((unsigned __int32 *)(v + 2) + 1) = 1;
```

You can write with Gravitum:

```python
from gravitum import uint8, uint32, ptr

v = bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

p = ptr(v, uint8)
p.add(2).cast(uint32).add(1).write(1)
```

Gravitum also implemented some functions (`ror4`, `rol4`, `byte1`, `low_byte`, `high_byte`, etc.) which are used in the code decompiled by IDA. You can reference them from `gravitum.defs`.

```python
from gravitum import uint32
from gravitum.defs import ror4

v = uint32(1)
v = ror4(v, 8)
```


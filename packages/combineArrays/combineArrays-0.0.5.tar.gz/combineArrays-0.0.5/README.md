# combineArrays
This package provides Python CFFI bindings to combine array z of Int32 with an array r of Double and return the result in array y
y_j = sum_i z(i*n+j)*r(i*n+j), i=0,..,m, j = 0,..,n

## Documentation
See doc/manual.pdf

## Installation
To install type:
```python
$ pip install combineArrays
```
## Usage
```python
from combineArrays import combine_arrays_v1
combine_arrays_v1( z, r, y, n, m)
### Parameters combine_arrays_v1
m: num rows, int64
n: num columns, int64
z: array 1, NumPy Array, int32
r: array 2, Numpy Array, float
y: reult, Numpy Array, float

from combineArrays import combine_arrays_v2
combine_arrays_v2( z, r, y, n, m)
### Parameters combine_arrays_v2
m: num rows, int64
n: num columns, int64
z: array 1, NumPy Array, int32
r: array 2, Numpy Array, float
y: reult, Numpy Array, float

from combineArrays import combine_arrays_v3
combine_arrays_v3( z, r, y, n, m)
### Parameters combine_arrays_v3
m: num rows, int64
n: num columns, int64
z: array 1, NumPy Array, int32
r: array 2, Numpy Array, float
y: reult, Numpy Array, float
```
## Test
To unit test type:
```python
$ test/test.py
```
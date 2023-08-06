# combineArrays
This package provides Python CFFI bindings to combine array z of Int32 with an array r of Double and return the result in array y
y_j = sum_i z(i*n+j)*r(i*n+j), i=0,..,m, j = 0,..,n

## Installation
To install type:
```python
$ pip install combineArrays
```
## Usage
```python
from combineArrays import combine_arrays_v1
from combineArrays import combine_arrays_v2
from combineArrays import combine_arrays_v3

# Parameters combine_arrays_v1
m: num rows, int64
n: num columns, int64
z: array 1, NumPy Array, int32
r: array 2, Numpy Array, float
y: reult, Numpy Array, float

# Parameters combine_arrays_v2
m: num rows, int64
n: num columns, int64
z: array 1, NumPy Array, int32
r: array 2, Numpy Array, float
y: reult, Numpy Array, float

# Parameters combine_arrays_v3
m: num rows, int64
n: num columns, int64
z: array 1, NumPy Array, int32
r: array 2, Numpy Array, float
y: reult, Numpy Array, float
```
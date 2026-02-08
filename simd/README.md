# Matrix Multiplication Benchmark

Clean, modular benchmarking for matrix multiplication implementations.

## Features

- **Python Naive**: Triple-nested loop implementation
- **C++ Naive**: Via ctypes wrapper 
- **NumPy**: Optimized BLAS backend
- **GPU**: CuPy implementation 

## Usage

```bash
python benchmark.py
```

## Installation

```bash
pip install numpy
pip install cupy-cuda12x
```


## Output

Shows timing comparisons and speedups vs Python naive implementation.

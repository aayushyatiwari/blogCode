import time
import numpy as np
import ctypes
from typing import List, Tuple, Optional

try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

def matmul_naive_python(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    n = len(A)
    C = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

class CppMatmul:
    def __init__(self, lib_path: str = './libmatmul.so'):
        try:
            self.lib = ctypes.CDLL(lib_path)
            self.lib.matmul_naive_c.argtypes = [
                ctypes.POINTER(ctypes.c_float),
                ctypes.POINTER(ctypes.c_float),
                ctypes.POINTER(ctypes.c_float),
                ctypes.c_int
            ]
            self.lib.matmul_naive_c.restype = None
            self.available = True
        except:
            self.available = False
    
    def matmul(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        n = A.shape[0]
        C = np.zeros((n, n), dtype=np.float32)
        pA = A.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        pB = B.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        pC = C.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        self.lib.matmul_naive_c(pA, pB, pC, n)
        return C

def benchmark_implementation(name: str, func, A, B, warmup: bool = True) -> float:
    if warmup:
        _ = func(A, B)
    
    start = time.time()
    _ = func(A, B)
    return (time.time() - start) * 1000

def run_benchmark(sizes: List[int]):
    cpp = CppMatmul()
    
    results = []
    print("\nMatrix Multiplication Benchmark")
    print("=" * 90)
    header = f"{'Size':<10}"
    if cpp.available:
        header += f"{'Python (ms)':<15} {'C++ (ms)':<15} {'NumPy (ms)':<15}"
    else:
        header += f"{'Python (ms)':<15} {'NumPy (ms)':<15}"
    if GPU_AVAILABLE:
        header += f"{'GPU (ms)':<15}"
    print(header)
    print("-" * 90)
    
    for n in sizes:
        A_list = [[float(i+j) for j in range(n)] for i in range(n)]
        B_list = [[float(i-j) for j in range(n)] for i in range(n)]
        A_np = np.array(A_list, dtype=np.float32)
        B_np = np.array(B_list, dtype=np.float32)
        
        timings = {}
        
        timings['python'] = benchmark_implementation("Python", matmul_naive_python, A_list, B_list)
        
        if cpp.available:
            timings['cpp'] = benchmark_implementation("C++", cpp.matmul, A_np, B_np)
        
        timings['numpy'] = benchmark_implementation("NumPy", lambda a, b: a @ b, A_np, B_np)
        
        if GPU_AVAILABLE:
            A_gpu = cp.array(A_np)
            B_gpu = cp.array(B_np)
            timings['gpu'] = benchmark_implementation("GPU", lambda a, b: a @ b, A_gpu, B_gpu)
        
        row = f"{n}x{n:<6} {timings['python']:<15.3f}"
        if cpp.available:
            row += f"{timings['cpp']:<15.3f}"
        row += f"{timings['numpy']:<15.3f}"
        if GPU_AVAILABLE:
            row += f"{timings['gpu']:<15.3f}"
        print(row)
        
        results.append({'size': n, **timings})
    
    print("=" * 90)
    print_speedups(results, cpp.available)
    
    return results

def print_speedups(results: List[dict], cpp_available: bool):
    print("\nSpeedup vs Python Naive")
    print("=" * 70)
    header = f"{'Size':<10}"
    if cpp_available:
        header += f"{'C++ Speedup':<20}"
    header += f"{'NumPy Speedup':<20}"
    if GPU_AVAILABLE:
        header += f"{'GPU Speedup':<20}"
    print(header)
    print("-" * 70)
    
    for r in results:
        row = f"{r['size']}x{r['size']:<6}"
        if cpp_available and 'cpp' in r:
            row += f"{r['python']/r['cpp']:<20.1f}x"
        row += f"{r['python']/r['numpy']:<20.1f}x"
        if GPU_AVAILABLE and 'gpu' in r:
            row += f"{r['python']/r['gpu']:<20.1f}x"
        print(row)
    print("=" * 70)

if __name__ == "__main__":
    sizes = [5, 10, 50, 100, 500]
    results = run_benchmark(sizes)

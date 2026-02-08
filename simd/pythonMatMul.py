import ctypes
import numpy as np

lib = ctypes.CDLL('./libmatmul.so') # importing the cpp matmul Single-Precision General Matrix-Vector multiplication

def matmul_naive(m, n):
    im = len(m[0])
    result = [[0]*(len(n[0])) for _ in range(len(m))]
    for i in range(len(m)):
        for j in range(len(n[0])):
            result[i][j] = 0
            for k in range(im):
                result[i][j] += m[i][k] * n[k][j]
    return result


def main():

    A3 = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

    B3 = [[9, 8, 7],
         [6, 5, 4],
         [3, 2, 1]]
    
    A2 = [[1, 2],
         [3, 4]]

    B2 = [[5, 6],
         [7, 8]]
    
    
    npx = np.asarray(A3) @ np.asarray(B3)
    npy = np.asarray(A2) @ np.asarray(B2)
    print(npy) 
    print(matmul(A2, B2))



    

if __name__ == "__main__":
    main()

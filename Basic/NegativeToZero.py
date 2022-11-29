import numpy as np
arr = np.array([1, -2, 3, 4, -5])
arr[arr < 0] = 0
print(arr)
# [1 0 3 4 0]

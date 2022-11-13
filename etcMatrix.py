import numpy as np

# Inverse Matrix
arr = np.array([[2, 5], [1, 3]])
arr_inv = np.linalg.inv(arr)
print(arr_inv)
# [[ 3. -5.]
#  [-1.  2.]]

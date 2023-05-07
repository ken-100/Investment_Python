import numpy as np


# Max
A = np.array([[2, 5], [1, 3]])
print(A)
[[2 5]
 [1 3]]

np.max(A)
# 5

# A = np.where(A > 3, 1, A)
print(A)
# [[2 1]
#  [1 3]]



# Inverse Matrix
A = np.array([[2, 5], [1, 3]])
A_inv = np.linalg.inv(A)
print(A_inv)
# [[ 3. -5.]
#  [-1.  2.]]




# Transposed Matrix
print(A.T)
# [[2 1]
#  [5 3]]



# Matrix multiplication
A = np.array([[1, 0, 0, 1], 
              [0, 1,0, -1]])

Sigma = np.array([[ 0.71, -0.743,  0.43,  0 ],
                  [-0.43,  0.46,  -0.26,  0 ],
                  [ 0.43 ,-0.26,  -0.46,  0 ],
                  [    0,     0,      0, 0.2 ]
                 ])

np.dot( np.dot(A,Sigma), A.T)
np.dot(A,Sigma) @ A.T          #

# array([[ 0.91 , -0.943],
#        [-0.63 ,  0.66 ]])


# Diagonal Matrix
A = np.array([[3, 0],
              [1, 2]])

eig, P = np.linalg.eig(A)
print("Eigenvalues\n",eig)
print("\nEigenvectors\n",P)
 
D = np.dot(np.dot(np.linalg.inv(P), A), P)
print("\nDiagonal matrix\n",D)

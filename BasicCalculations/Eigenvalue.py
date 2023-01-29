import numpy as np
from numpy import linalg as LA


Q = np.array([[1,0.3],[0.3,1]])

print(np.linalg.eigvals(Q))
print(LA.eigvals(Q))
# [1.3 0.7]
# [1.3 0.7]

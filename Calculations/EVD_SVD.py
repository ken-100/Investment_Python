import numpy as np
from numpy.linalg import eig,svd,matrix_rank

# 固有値分解 EVD Eigen Value Decomposition
# https://www.headboost.jp/docs/linear-algebra-for-programmers/factorization/eigen/#:~:text=%E5%9B%BA%E6%9C%89%E5%80%A4%E5%88%86%E8%A7%A3%E3%81%A8%E3%81%AF%E3%80%81%E3%81%82%E3%82%8B,%E3%81%99%E3%82%8B%E3%81%93%E3%81%A8%E3%82%92%E8%A8%80%E3%81%84%E3%81%BE%E3%81%99%E3%80%82&text=%E3%81%93%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E8%A1%8C%E5%88%97%20A,%E3%81%AE%E3%81%8C%E5%9B%BA%E6%9C%89%E5%80%A4%E5%88%86%E8%A7%A3%E3%81%A7%E3%81%99%E3%80%82

# 特異値分解 SVD:Singular Value Decomposition
# https://qiita.com/kidaufo/items/0f3da4ca4e19dc0e987e

# さまざまな行列48個一覧
# https://mathlandscape.com/matrixes/#toc6


#EVD
A = np.array([
    [3,1],
    [0,2]] )

# tmp = 3
# A = np.random.rand(tmp, tmp)
print("A\n",A)

B = np.linalg.inv(A)
print("\nInverse: B\n",B)
# A^-1 = 1 / (ad-bc) [d, -b]
#                    [-c, a]

C = A @ B 
print("\nAB=E\n",C)

C = B @ A
print("\nBA=E\n",C)

values,V = eig(A)

print("\nEigenvalue\n",values)
print("\nEigeVector V\n",V)
print("\nInverse V^-1\n",np.linalg.inv(V))

AA = V @ np.diag(values) @ np.linalg.inv(V)
print("\n A=V Λ V^-1\n",np.linalg.inv(V))


# SVD
A = np.array([[2, 4, 1, 3], [1, 5, 3, 2], [5, 7, 0, 7]])
A = np.array([[1,1,0], [0,0,1]])
A = np.array([[6,0,6], [2,4,-5]])

print("Matrix A\n", A)

print("\nTransposed: A^T\n",A.T)

B = A @ A.T 
print("\nTransposed: B = A A^T\n",B)

C = A.T @ A 
print("\nTransposed: C = A^T A\n",C)

U_values,U = eig(B)
U_values = U_values**0.5 
print("\n left values \n",U_values)
print("\n left U\n",U)

V_values,V = eig(C)
V = (A.T @ U[:,0] ) / U_values[0]
V = V.reshape(A.shape[1], 1)

for i in range(1,len(A)):
    tmp = ( A.T @ U[:,i] ) / U_values[i]
    tmp = tmp.reshape(A.shape[1], i)
    V = np.append(V, tmp, axis=1)

print("\n right values \n",V_values)
print("\n right V\n",V)

X = np.diag(U_values)   
print("\n X\n",X)

AA = np.round( U @ X @ V.T ,2)
print("\n A = U X V\n",AA)
print("\n A\n",A)

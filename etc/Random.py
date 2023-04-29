import numpy as np
i = 2
np.random.seed(0)


# Uniform distribution / More than 0.0, less than 1.0
print(np.random.rand(i))
print(np.random.rand(i,i))    
print(np.random.random_sample(i))
print(np.random.random(i))
print("*2 × 2 is random.rand only\n")



# Normal distribution / mean 0, variance 1 
print(np.random.randn(i))
print(np.random.randn(i,i))


# Multidimensional normal distribution
np.random.multivariate_normal(np.zeros(i),np.identity(i)) #(mean, cov, size, check_valid, tol)



# https://note.nkmk.me/python-numpy-random/


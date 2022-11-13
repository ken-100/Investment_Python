import math
import numpy as np
import matplotlib.pyplot as plt

print(math.e)
print(np.e)
print(np.exp(1))
# 2.718281828459045
# 2.718281828459045
# 2.718281828459045

print(np.exp(2))
print(math.exp(2))
# 7.38905609893065
# 7.38905609893065

print(np.exp(0))
print(np.exp(-2))
# 1.0
# 0.1353352832366127

x = list(range(-10,5))
y = np.exp(x)   # Impossible with "math"

fig, ax = plt.subplots(1, 1, squeeze=False,figsize=(8,3),tight_layout=True)
ax[0,0].plot(x, y)
ax[0,0].set_title("y=exp(x)")
plt.show()






print(np.log(2))
# 0.6931471805599453

print(np.log2(2))
# 1.0

x = list(range(1,5))
y = np.log(x)   # Impossible with "math"

fig, ax = plt.subplots(1, 1, squeeze=False,figsize=(8,3),tight_layout=True)
ax[0,0].plot(x, y)
ax[0,0].set_title("y=exp(x)")
plt.show()

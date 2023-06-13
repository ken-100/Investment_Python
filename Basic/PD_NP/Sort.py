import pandas as pd
import numpy as np

arr = np.arange(4).reshape((2, 2))
df = pd.DataFrame(arr,columns=["x","y"])
print(df)
#    x  y
# 0  0  1
# 1  2  3


df = df.sort_values("x", ascending=False).reset_index(drop=True)
print(df)
#    y  x
# 0  3  2
# 1  1  0


df = df.sort_values("x").reset_index(drop=True)
print(df)
#    y  x
# 0  1  0
# 1  3  2

df = df.sort_values(0, ascending=False, axis=1).reset_index(drop=True)
print(df)
#    y  x
# 0  1  0
# 1  3  2



arr = np.arange(6).reshape((3, 2))
df = pd.DataFrame(arr,columns=["x","y"])
print(df)
#    x  y
# 0  0  1
# 1  2  3
# 2  4  5

print(np.argsort(df, axis=0))
#    x  y
# 0  0  0
# 1  1  1
# 2  2  2

print(np.argsort(df, axis=1))
#    x  y
# 0  0  1
# 1  0  1
# 2  0  1

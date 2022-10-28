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

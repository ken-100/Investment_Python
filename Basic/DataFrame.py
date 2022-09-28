import pandas as pd
import numpy as np

# pd.set_option('display.max_columns', 70)
# pd.set_option('display.max_rows', None)

df = pd.DataFrame(columns = ["A","B"])
df = pd.DataFrame(index = ["a","b"], columns = ["A","B"])
df = pd.DataFrame(np.zeros([2,2]), index = ["a","b"], columns = ["A","B"])
for i in range(0,3):
    exec(f"df{i} = df")



a =list(range(0,4))
print(a)
# [0, 1, 2, 3]

a = list(range(0,8,2))
print(a)
# [0, 2, 4, 6]

a = np.reshape(a,(2,2))
print(a)
# [[0 2]
#  [4 6]]

pd.DataFrame(a)

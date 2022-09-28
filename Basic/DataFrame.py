import pandas as pd
import numpy as np

# pd.set_option('display.max_columns', 70)
# pd.set_option('display.max_rows', None)

df = pd.DataFrame(columns = ["A","B"])
df = pd.DataFrame(index = ["a","b"], columns = ["A","B"])
df = pd.DataFrame(np.zeros([2,2]), index = ["a","b"], columns = ["A","B"])
for i in range(0,3):
    exec(f"df{i} = df")

df2

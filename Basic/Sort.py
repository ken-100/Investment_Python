import pandas as pd
import numpy as np

arr = np.arange(12).reshape((4, 3))
df = pd.DataFrame(arr,columns=["x","y","z"])

df = df.sort_values("x", ascending=False).reset_index(drop=True)
df

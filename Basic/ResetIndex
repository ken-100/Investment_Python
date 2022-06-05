import pandas as pd
import numpy as np

arr = np.arange(12).reshape((4, 3))
df = pd.DataFrame(arr,columns=["x","y","z"])

df = df.loc[df["x"] >= 4,:].reset_index(drop=True)
df

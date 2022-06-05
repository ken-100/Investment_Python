import pandas as pd
import numpy as np

arr = np.arange(12).reshape((4, 3))
df = pd.DataFrame(arr,columns=["x","y","z"])
    
df.loc[:,"x"] = df.loc[:,"x"].apply("{:.1%}".format)
df.loc[:,"y"] = df.loc[:,"y"].apply("{:.2f}".format)

df

import pandas as pd
import numpy as np

arr = np.arange(12).reshape((4, 3))
df = pd.DataFrame(arr,columns=["x","y","z"])
    
df.loc[:,"x"] = df.loc[:,"x"].apply("{:.1%}".format)
df.loc[:,"y"] = df.loc[:,"y"].apply("{:.2f}".format)
df
#         x      y   z
# 0    0.0%   1.00   2
# 1  300.0%   4.00   5
# 2  600.0%   7.00   8
# 3  900.0%  10.00  11


Array = np.array([[1.0, 2.5, 3.234, 5.99, 99.99999], [0.3, -23.543, 32.9999, 33.0000001, -0.000001]])
Array = Array.astype(int)
print(Array)
# [[  1   2   3   5  99]
#  [  0 -23  32  33   0]]

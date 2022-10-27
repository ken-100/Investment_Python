import pandas as pd
import numpy as np


print(float("nan"))
print(float("NaN"))
print(float("NAN"))
# nan
# nan
# nan


Array = np.array([[1, 2], [3,float("nan")]])
pd.isnull(Array)
# array([[False, False],
#        [False,  True]])

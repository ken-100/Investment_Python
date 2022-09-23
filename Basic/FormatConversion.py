import pandas as pd
import numpy as np


tmp = 1
tmp1 = '{:.1%}'.format(tmp)
print(tmp1)
tmp2 = '{:.2f}'.format(tmp)
print(tmp2)


i = 4
df = pd.DataFrame(np.reshape(list(range(0,i*i)), (i, i))  )
df[0] = df[0].apply("{:,.0%}".format)
df[1] = df[1].apply("{:,.2f}".format)
df

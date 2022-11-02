import pandas as pd
import numpy as np


tmp = 1
tmp1 = '{:.1%}'.format(tmp)
print(tmp1)
# 100.0%

tmp2 = '{:.2f}'.format(tmp)
print(tmp2)
# 1.00

i = 4
df = pd.DataFrame(np.reshape(list(range(0,i*i)), (i, i))  )
df[0] = df[0].apply("{:,.0%}".format)
df[1] = df[1].apply("{:,.2f}".format)
print(df)
#         0      1   2   3
# 0      0%   1.00   2   3
# 1    400%   5.00   6   7
# 2    800%   9.00  10  11
# 3  1,200%  13.00  14  15



for i in range(0,len(df)):
    tmp = df.loc[i,0]
    df.loc[i,0] = float(tmp.replace(",","").replace("%",""))/100
print(df)

#       0      1   2   3
# 0   0.0   1.00   2   3
# 1   4.0   5.00   6   7
# 2   8.0   9.00  10  11
# 3  12.0  13.00  14  15

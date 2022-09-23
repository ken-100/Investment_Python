from sklearn.datasets import load_iris
import pandas as pd
import numpy as np

# https://qiita.com/ao_log/items/fe9bd42fd249c2a7ee7a

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['Target'] = iris.target
df.loc[df['Target'] == 0, 'Target'] = "setosa"
df.loc[df['Target'] == 1, 'Target'] = "versicolor"
df.loc[df['Target'] == 2, 'Target'] = "virginica"

Target = df["Target"].unique().tolist()

tmp = np.reshape(Target, (len(Target),1))
Count = pd.DataFrame(tmp,columns=["Target"] )

for i in range(0,len(tmp)):
    tmp1 = df["Target"].value_counts()[tmp[i]]
    Count.loc[i,"Count"] = tmp1[0]
    Count.loc[i,"%"] = round(tmp1[0] / len(df) ,2)

Count["Count"] = Count["Count"].apply("{:,.0f}".format)
Count["%"] = Count["%"].apply("{:,.1%}".format)

Count

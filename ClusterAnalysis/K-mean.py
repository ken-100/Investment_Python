import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

#K-means
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
c = KMeans(n_clusters=3,random_state=3).fit_predict(df) #pred_cluster
# c = KMeans(n_clusters=3, init='k-means++', random_state=3).fit_predict(df) #pred_cluster # k-mean++

M = pd.DataFrame(confusion_matrix(iris.target,c))
M.index = iris_dataset.target_names
S = accuracy_score(iris.target,c)
print("accuracy_score=" + str(S))
M

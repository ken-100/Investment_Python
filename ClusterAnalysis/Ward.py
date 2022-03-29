#Ward
import pandas as pd
from sklearn import datasets
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

iris = datasets.load_iris() #DataLoad
df = pd.DataFrame(iris.data, columns=iris.feature_names)

#ward,euclidean
linkage_result = linkage(df, method="ward", metric="euclidean")

fig = plt.figure(figsize=(10, 4))
dn = dendrogram(linkage_result, labels=list(iris.target_names[iris.target]), above_threshold_color="grey")

#Coloring
label_colors = {"setosa": "c", "versicolor": "m", "virginica": "y"}

ax = plt.gca()
xlbls = ax.get_xmajorticklabels()
for lbl in xlbls:
    lbl.set_color(label_colors[lbl.get_text()])
plt.title("IrisDataset")
plt.ylabel("Distance")
plt.tight_layout()
plt.show()

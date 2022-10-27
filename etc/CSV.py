import pandas as pd
import numpy as np

df = pd.DataFrame(np.zeros([2,2]), index = ["a","b"], columns = ["A","B"])

pd.DataFrame(df).to_csv("df.csv")
#pd.DataFrame(df).to_csv("df.csv",encoding="utf_8_sig")  #<-for Japanese

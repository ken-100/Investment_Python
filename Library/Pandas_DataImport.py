df = pd.DataFrame(np.zeros([2,2]), index = ["a","b"], columns = ["A","B"])


pd.DataFrame(df).to_csv('df.csv', encoding="utf_8_sig")


df = pd.read_csv('df.csv')
df
#   Unnamed:0 A    B
# 0 a         0.0  0.0
# 1 b         0.0  0.0


df = pd.read_csv('df.csv', index_col=0)
df
#   A   B
# a 0.0 0.0
# b 0.0 0.0


df = pd.read_csv('df.csv', header=None)
df
#   0   1   2
# 0 NaN A   B
# 1 a   0.0 0.0
# 2 b   0.0 0.0

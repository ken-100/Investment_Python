import pandas as pd
df = pd.DataFrame({"A": ["A1", "A2", "A3"],
                   "B": ["B1", "B2", "B3"],
                   "C": ["C1", "C2", "C3"]},
                  index=["ONE", "TWO", "THREE"])
print(df)
#         A   B   C
# ONE    A1  B1  C1
# TWO    A2  B2  C2
# THREE  A3  B3  C3

df["D"] = 0
print(df)
#         A   B   C  D
# ONE    A1  B1  C1  0
# TWO    A2  B2  C2  0
# THREE  A3  B3  C3  0

df.loc["FOUR",:] = 0
print(df)

df.insert(1, "AA", 1)
print(df)
#         A  AA   B   C    D
# ONE    A1   1  B1  C1  0.0
# TWO    A2   1  B2  C2  0.0
# THREE  A3   1  B3  C3  0.0
# FOUR    0   1   0   0  0.0

df = df.drop(["D","AA"], axis=1)
print(df)
#         A   B   C
# ONE    A1  B1  C1
# TWO    A2  B2  C2
# THREE  A3  B3  C3
# FOUR    0   0   0

df = df.T
df.insert(1, "FIVE", 1)
df = df.T
print(df)
#         A   B   C
# ONE    A1  B1  C1
# FIVE    1   1   1
# TWO    A2  B2  C2
# THREE  A3  B3  C3
# FOUR    0   0   0

df = df.drop(["FOUR","FIVE"], axis=0)
print(df)
#         A   B   C
# ONE    A1  B1  C1
# TWO    A2  B2  C2
# THREE  A3  B3  C3

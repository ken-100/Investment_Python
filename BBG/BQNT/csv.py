import pandas as pd
df = pd.read_csv("test.csv")
df


import pandas as pd
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['Tokyo', 'Osaka', 'Nagoya']
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data)
df.to_csv("output.csv")
df

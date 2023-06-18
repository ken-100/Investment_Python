import pandas as pd
df = pd.io.html.read_html("https://stats.bls.gov/news.release/empsit.b.htm")
df = df[0]
df

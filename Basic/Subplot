import pdblp
from xbbg import blp
import matplotlib.pyplot as plt

con = pdblp.BCon(timeout=10000)
con.start()
T = ["USDJPY Curncy","EURJPY Curncy"]
df = con.bdh(T, "px_open", "20200101", "20210101").reset_index()
df.columns = ["data"] + T
df.loc[:,"BM"] = 120

x = df.loc[:,"data"]
fig = plt.figure()


j = 1
for i in range(0,2):
    exec(f"ax{i} = fig.add_subplot(1, 2, {j})")
    exec(f"y = df.loc[:,T[i]]")
    exec(f"ax{i}.plot(x,y, color = 'Blue')")
    exec(f"ax{i}.plot(x,df.loc[:,'BM'], color = 'Gray')")
    exec(f"ax{i}.set_title(i)")
    exec(f"ax{i}.set_ylim(100,140)")
    plt.xlabel("x-lable")
    plt.ylabel("y-lable")
    exec(f"ax{i}.set_yticks(list(range(100,150,10)))")
    j += 1
    
plt.gcf().autofmt_xdate()
fig.tight_layout()

# https://www.yutaka-note.com/entry/matplotlib_axis

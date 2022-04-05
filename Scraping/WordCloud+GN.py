from pylab import rcParams
import feedparser
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

url = []
s = ["SP500+OR+(US+Stock)","Oil"]

for i in range(0,len(s)):
    url += ["https://news.google.com/rss/search?q={"+s[i]+"}+when:3"]
#     webbrowser.open("https://news.google.com/search?q="+s[i]+"%20when%3A3d&hl=en-US&gl=US&ceid=US%3Aen")
    
    
url += ["https://news.google.com/news/rss"]
topic = ["WORLD","NATION","BUSINESS"]
s = s + ["Headline"] + topic
tmp = "https://news.google.com/news/rss/headlines/section/topic/"
for i in range(0,len(topic)):
    url += [tmp+topic[i]]
    
    
rcParams['figure.figsize'] = 7,7

for i in range(0,len(url)):
    d = feedparser.parse(url[i])
    news = list()

    for j, entry in enumerate(d.entries, 1):
        p = entry.published_parsed
        sortkey = "%04d%02d%02d%02d%02d%02d" % (p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour, p.tm_min, p.tm_sec)

        tmp = {"no": j, "title": entry.title, "summary": entry.summary, "link": entry.link,"published": entry.published, "link": entry.link,"sortkey": sortkey }
        news.append(tmp)

    df = pd.DataFrame(news).loc[:,['title','link','sortkey']]
    
    WC = ""
    for j in range(0,len(df)):
        WC += df.loc[j,"title"]

    WC = WordCloud().generate(WC.lower())
    WC.to_file(str(i)+".png")
    plt.imshow(WC)
    plt.axis('off')
    print(str(i)+":"+s[i])
    plt.show()
   

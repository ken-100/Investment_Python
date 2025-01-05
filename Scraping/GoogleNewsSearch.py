import webbrowser

url = []
s = ["Treasury+Yield","SP500+OR+(US+Stock)","china+(equity+OR+stock)","Oil"]  #Search content

for i in range(0,len(s)):
    url += ["https://news.google.com/rss/search?q={"+s[i]+"}+when:3"]
    webbrowser.open("https://news.google.com/search?q="+s[i]+"%20when%3A3d&hl=en-US&gl=US&ceid=US%3Aen")

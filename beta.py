from bs4 import BeautifulSoup
import requests
import re

param = {"q": "smp ypvdp"} 

a=[]
b=[]
c=[]

headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15"
}

r = requests.get("https://google.com/search", params=param, headers=headers)

soup = BeautifulSoup(r.content, "lxml")
soup.prettify()

title = soup.select(".DKV0Md span")

for t in title:
    a.append(f"{t.get_text()}\n")

snippets = soup.select(".aCOpRe span:not(.f)")

for d in snippets:
    b.append(f"{d.get_text()}\n\n")


print("="*20)

for i in range(5):
	c.append(a[i]+b[i])

print(c[0]+c[1])

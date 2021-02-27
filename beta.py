from bs4 import BeautifulSoup
import requests
import re

param = {"q": "coffee"}
headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15"
}

r = requests.get("https://google.com/search", params=param, headers=headers)

soup = BeautifulSoup(r.content, "lxml")
soup.prettify()

title = soup.select(".DKV0Md span")

for t in title:
    print(f"Title: {t.get_text()}\n")

snippets = soup.select(".aCOpRe span:not(.f)")

for d in snippets:
    print(f"Snippet: {d.get_text()}\n")

link = soup.findAll("a")

for link in soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
    print(re.split(":(?=http)", link["href"].replace("/url?q=", "")))
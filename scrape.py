from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import csv


url = "https://www.brainyquote.com"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = Request(url = url, headers= headers)
connect = urlopen(req)
html = connect.read()
connect.close()

page = soup(html, "html.parser")

links = page.find_all("a", {"class" : "bq_on_link_cl"})
l = []

out = open("parsed.csv", "w")
fields = ['Author', 'Quote']
writer = csv.DictWriter(out, fieldnames=fields)
writer.writeheader()

for link in links:
    l.append(link['href'])
counter = 0
for g in l:
    if(counter >= 500):
        break
    nUrl = url + g
    print("Parsing: " + nUrl)
    request = Request(url = nUrl, headers = headers)
    con = urlopen(request)
    nhtml = con.read()
    con.close()
    newPage = soup(nhtml, "html.parser")

    quotes = newPage.find_all("a", {"class" : "b-qt"})
    author = newPage.find_all("a", {"class" : "oncl_a"})
    # keywords = newPage.find_all("div", {"class" : "kw-box"})
    parsed = []

    for i in range(len(quotes)):

        auth = author[i].getText()
        quote = quotes[i].getText()
        # keyword = keywords[i].getText()
        data = {"Author" : auth, "Quote" : quote}
        parsed.append(data)

    writer.writerows(parsed)
    counter += 1

out.close()
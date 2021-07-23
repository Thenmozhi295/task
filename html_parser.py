import re
from bs4 import BeautifulSoup

htmlfile =open("/home/thenmozhi/writerpara.com/index.html","r")
index=htmlfile.read()

s=BeautifulSoup(index,'html.parser')
#print(s.prettify())

text=s.get_text(strip=True)
print(text)

text2=re.sub("[^A-Za-z0-9]+"," ",text)
print(text2)

import urllib.request
import bs4
from bs4 import BeautifulSoup
req=urllib.request.Request('https://mall.jd.com/index-782694.html')
response=urllib.request.urlopen(req)
f=response.read()

'''s=BeautifulSoup(f,"html.parser",from_encoding="gb2312")
f=BeautifulSoup(f,"html.parser")'''

'''t=f.find_all('span',class_="jdNum")
l=[]
a=0

for i in range(len(f)):
    if f[i:i+7]=='c-price':
        for e in range(i+9,i+20):
            if not f[e] in '0123456789.':
                b=e
                break
        l.append(f[i+9:b])

m=[]
for i in range(len(f)):
    if f[i:i+9]=='item-name':
        for e in range(i,i+300):
            if f[e]=='>':
                a=e
                break
        for e in range(i,i+300):
            if f[e]=='<':
                b=e
                break
        m.append(f[a+1:b])

d={}
for i in range(len(l)):
    d[m[i]]=l[i]

for i in d.items():
    print(i)'''

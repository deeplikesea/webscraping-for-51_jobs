from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import csv
import re

pages = ["http://search.51job.com/list/020000%252C080200%252C070200,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E6%258C%2596%25E6%258E%2598,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=4&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="]
# this URL is the first page that you want to collect data from
html = urlopen(pages[0])
#<!DOCTYPE html>  "html.parser"
#<?xml version="1.0" encoding="ISO-8859-1"?> "lxml.parser"
bsobj = BeautifulSoup(html, "html.parser")
changepages = bsobj.body.find("div", {"id" : "resultList"}).find("div", {"class" : "dw_page"}).ul.findAll("a", {"href": re.compile("http://")})

for link in range(0,len(changepages)-1):
    changepage = changepages[link-1].attrs["href"][7:]
    changepage = "http://"+urllib.parse.quote(changepage)
    pages.append(changepage)
row = []
i = 0

while (i < len(pages)):
    html=urlopen(pages[i])
    #<!DOCTYPE html>  "html.parser"
    #<?xml version="1.0" encoding="ISO-8859-1"?> "lxml.parser"
    bsobj = BeautifulSoup(html, "html.parser")
    results = bsobj.body.find("div", {"id" : "resultList"}).findAll("div", {"class" : "el"})
    print(results)
    del results[0]

    for result in results:
        el = []
        el.append(result.p.a.attrs["title"])
        el.append(result.find("span", {"class": "t2"}).a.get_text())
        el.append(result.find("span", {"class": "t3"}).get_text())
        el.append(result.find("span", {"class": "t4"}).get_text())
        el.append(result.find("span", {"class": "t5"}).get_text())
        el.append(result.p.a.attrs["href"])
        row.append(el)
    print("--------")
    print(len(row))
    i += 1


csvFile = open("E:/pj_51job.csv", "w", encoding='gbk', newline='')# use newline to avoid a empty row in the end
writer = csv.writer(csvFile)
# 写入的内容都是以列表的形式传入函数
for order in range(0,len(row)):
    writer.writerow(row[order])
csvFile.close()

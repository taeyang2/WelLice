import csv
import urllib.request
import re

from bs4 import BeautifulSoup

file = 'C:\WelLice_ext\StuffDic10.csv'

stuffData = {}

url = "https://terms.naver.com/list.nhn?cid=42785&categoryId=42795&so=st3.asc&viewType=&categoryType=&page="
for pageNum in range(101):
    pageNum = pageNum +1
    pageUrl = url + str(pageNum)
    print(pageUrl)

    # 쿡쿡TV 식재료 데이터 수집
    req = urllib.request.urlopen(pageUrl)
    res = req.read()

    soup = BeautifulSoup(res, 'html.parser')
    pageData = soup.select('div.thumb_area > div > a > img')
    #pageData = soup.select('div.subject > strong.title > a')

    print("pageData----",pageData)
    #print("pageData-------",pageData)

    for elements in pageData:
        data = str(elements)
        print("data-----", data)
        data2 = re.findall(r'"(.*?)"', data)
        print("data2----", data2)
        print(data2[2])
        data2[2] = data2[2].replace("id","")
        print("data2-2----", data2)

        # stuffData에 데이터 정리 : img alt="" -> value, data-id="" -> key
        for e1 in data2:
            key = data2[2]
            value = data2[0]
            stuffData[key] = value
    print("stuffData------", stuffData)

print("결과!!!!!", stuffData)
print(len(stuffData)) #1489개


# 쿡쿡TV에서 효능 데이터 수집
for sKey, sVal in stuffData.items():
    stuffUrl = f"https://terms.naver.com/entry.nhn?docId={sKey}&cid=42785&categoryId=42795"
    #stuffUrl.format(sKey)
    print("stuffUrl------",stuffUrl)


# with open(file, newline='') as f:
#     reader = csv.reader(f, delimiter = ',', quotechar = '|')
#
#     for row in reader:


import csv
import urllib.request
import re

from bs4 import BeautifulSoup




stuffData = {}
efficacyDict = {}

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
    print("stuffUrl------",stuffUrl)

    sReq = urllib.request.urlopen(stuffUrl)
    sRes = sReq.read()

    sSoup = BeautifulSoup(sRes, 'html.parser')
    sData = sSoup.select('p.txt')
    print("sData------", sData)

    sData2 = str(sData).split('<br/>')
    print("sData2-----", sData2)



    for e3 in sData2:
        if "<strong>· 효능 :</strong>" in e3:
            efficacy = e3.replace('<strong>· 효능 :</strong> ', '')
            print("efficacy1------", efficacy)
            efficacy2 = re.sub(r'\([^)]*\)', '', efficacy)
            print("efficacy2------", efficacy2)
            efficacy3 = efficacy2.split(',')
            result = []
            for e4 in efficacy3:
                result.append(e4.strip())
            print("result------", result)
        else :
            result = "결과 없음"
            print("result------", result)

        efficacyDict[sVal] = result
print("최종결과!!!!!!!!", efficacyDict)
print(len(efficacyDict))









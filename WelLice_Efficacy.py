import csv
import urllib.request
import re
import time
from bs4 import BeautifulSoup




stuffData = {}
efficacyDict = {}

url = "https://terms.naver.com/list.nhn?cid=42785&categoryId=42795&so=st3.asc&viewType=&categoryType=&page="
for pageNum in range(4): #101 페이지
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
count = 0
for sKey, sVal in stuffData.items():
    #count += 1
    #if count % 30 == 0:
        #time.sleep(1)

    time.sleep(1)
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
            efficacyDict[sVal] = result
        else :
            else_result = "결과 없음"
            print("else_result------", else_result)

    #efficacyDict[sVal] = result
print("최종결과!!!!!!!!", efficacyDict)
print(len(efficacyDict))


# 효능 데이터 확인 & Json
effect_igredient_list = []

count = 0
for ekey, evalue in efficacyDict.items():
    if evalue != '결과 없음':
        count = count + 1
        print("데이터확인---"+str(count)+"."+ekey)

        # Json
        for e5 in evalue:
            print("e5----",e5)
            if len(effect_igredient_list) != 0:
                print('1')
                in_effect = []
                for e6 in effect_igredient_list:
                    print("e6['effect']====",e6['effect'])
                    in_effect.append(e6['effect'])
                    print("in_effect---",in_effect)
                    #print("e6----",e6)
                if e5 not in in_effect:
                    print('1-1')
                    effect_igredient_list.append({'effect': e5, 'ingredient_list': [ekey]})
                    print("RESULT_effect_igredient_list", effect_igredient_list)


                elif e5 in in_effect:
                    print('1-2')
                    for e7 in effect_igredient_list:
                        if e7['effect'] == e5:
                            e7['ingredient_list'].append(ekey)
                            print("RESULT_effect_igredient_list", effect_igredient_list)

                    #effect_igredient['ingredient_list'].append(ekey)
                    #print("effect_igredient['ingredient_list']",effect_igredient['ingredient_list'])

            elif len(effect_igredient_list) == 0 :
                print('2')
                effect_igredient = {}
                effect_igredient['effect'] = e5
                effect_igredient['ingredient_list'] = [ekey]
                effect_igredient_list.append(effect_igredient)
                print("1st_not in_effect_igredient----------", effect_igredient)

print(effect_igredient_list)











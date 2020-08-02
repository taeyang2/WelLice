import urllib.request
from bs4 import BeautifulSoup
import re
import requests
import csv
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import sys
import json


# file = open('StuffDic.csv', 'r', encoding='utf-8')
# r = csv.reader(file)

#가나다
korCode = ['%EA%B0%80','%EB%82%98','%EB%8B%A4','%EB%9D%BC','%EB%A7%88','%EB%B0%94','%EC%82%AC','%EC%95%84','%EC%9E%90',
       '%EC%B0%A8','%EC%B9%B4','%ED%83%80','%ED%8C%8C','%ED%95%98']
kor = ['가','나','다','라','마','바','사','아','자','차','카','타','파','하']

#지역 구분
doNum = ['2','1','4','3','7','5','8','6','9']
do = ['서울/경기','강원도','충청남도','충청북도','경상남도','경상북도','전라남도','전라북도','제주도']

#지역별 음식 저장 할 리스트
locfood = [[],[],[],[],[],[],[],[],[]]

f = open('WelLice_data_editing.csv','w',newline='')
wr = csv.writer(f)


#지역별 url 작성
for d in doNum:
    siteUrl = "http://www.nongsaro.go.kr/portal/ps/psr/psrc/areaCkRyLst.ps?menuId=PS03934&pageIndex=1&pageSize=10&pageUnit=10&type=0"
    doUrl = siteUrl + d + "&schText="
    doIndex = doNum.index(d)
    doName = do[doIndex]
    print(doName)
    locfood[doIndex].append(doName)

#지역별 전체 Url 작성 후 데이터 수집
    for i in korCode:
        fullUrl = doUrl + i

        req = urllib.request.urlopen(fullUrl)
        res = req.read()

        soup = BeautifulSoup(res, 'html.parser')
        text = soup.select(('li > table > tbody > tr > td > a > span'))
        #print(text)


        for t in text:
            data = t.get_text().strip()
            if '(' in data or '[' in data or '<' in data:
                #괄호 안 내용 제거(data2 = ()를 제거한 텍스트)
                data2 = re.sub(r'\([^)]*\)','', data)
                data3 = re.sub(r'\<[^)]*\>','', data2)
                data4 = re.sub(r'\[([^]]*)\]', '', data3)
                locfood[doIndex].append(data4.strip())
            else:
                locfood[doIndex].append(data.strip())



    print(locfood[doIndex])
    print(len(locfood[doIndex]))

#제주향토음식과 타지역 향토음식 비교 후 중복 제거
for count in range(8):
    #print(count)

    for jeju_food in locfood[8]:
        if jeju_food in locfood[count]:
            locfood[8].remove(jeju_food)

locfood[8].remove('제주도')
#결과 확인
print(locfood[8])
print(len(locfood[8]))
count_locfood8 = 306-len(locfood[8])
print(count_locfood8)


#제주향토음식 데이터 내 중복 확인 후 제거(key만 리스트에 따로 저장)
groupby = list(set(locfood[8]))
result = dict()
for ip in groupby:
    result[ip] = locfood[8].count(ip)

print(result)
print(len(result))

#key만 리스트로 저장
dic_food_key = result.keys()
final_jeju_food = list(dic_food_key)
final_jeju_food.sort()

print(final_jeju_food)
print(len(final_jeju_food))


# 음식점 데이터 수집
for indexfood in final_jeju_food :
    print(indexfood)
    dining_url = 'https://www.diningcode.com/list.php?query=' + indexfood
    print(dining_url)

    #url의 html 파일 가져오기
    dining_html = requests.get(dining_url, headers={"User-Agent": "Mozilla/5.0"})
    print(dining_html)
    #가져온 html 파일을 html parser를 통해 정리
    dining_soup = BeautifulSoup(dining_html.text, "html.parser")

    restaurants = dining_soup.findAll("span",attrs = {"class":"btxt"})
    menu = dining_soup.findAll("span",attrs = {"class":"stxt"})
    area = dining_soup.findAll("i",attrs={"class":"loca"})
    addressData = str(dining_soup.findAll("span", attrs = {"class":"ctxt"}))
    #<i> 제거
    address = re.sub('<i.*?>.*?</i>','',addressData, 0, re.I|re.S)
    #print(address)

    #</span> 제거 후 <span> 단위로 슬라이싱
    remove_tag = address.split('</span>,')
    #print(remove_tag)
    #print(type(remove_tag))
    #print(remove_tag[0])
    #print(type(remove_tag[0]))

    #<span class="ctxt"> 제거
    remove_front_tag = []
    for r in remove_tag:
        remove_front_tag.append(r.replace(' <span class="ctxt">','').replace('</span>]',''))
    #print(remove_front_tag)
    #print(remove_front_tag[1])


    #업소주소 추출
    loclist = remove_front_tag[1::2]
    #print(loclist)

    #print(docurls[food.index(indexfood)])



    #데이터 정리
    for line1, line2, line3 in zip(restaurants, menu, loclist):
        menu_list = []
        # print(type(line1))
        # print(line1.get_text(), end = ":")
        restName = line1.get_text().split(' ')
        #print(restName)
        # print(type(line2))
        # print(line2.get_text())
        menulist = line2.get_text().split(',')
        for menus in menulist:
            menu_list.append(menus.strip())
        loca = line3
        print(restName)
        print(loca)

        #위도 경도 수집
        def get_from_bunzi(add):
            print(add)

            x = ""
            y = ""
            try:

                time.sleep(1)

                global pre_time
                this_time = time.time()
                pre_time = time.time()

                if abs(pre_time - this_time) < 1:
                    time.sleep(1)
                pre_time = time.time()
                try:
                    url = 'http://api.vworld.kr/req/address?service=address&request=getCoord&key=8C96FBD7-F4DA-384E-A0A1-1EDB5E856952&type=PARCEL&address=' + add
                    print(url)
                    session = requests.Session()
                    retry = Retry(connect=3, backoff_factor=1)
                    adapter = HTTPAdapter(max_retries=retry)
                    session.mount('http://', adapter)
                    session.mount('https://', adapter)
                    headers = {'Content-Type': 'application/json; charset=utf-8'}

                    res = session.get(url, headers=headers).text
                    json_root = json.loads(res)
                    sys.stdout.flush()
                    if json_root['response']['status'] == 'NOT_FOUND':
                        # print(datetime.datetime.now().isoformat() + "/ " + add + " / NOT")
                        sys.stdout.flush()
                        x = y = ""
                        #print('if문' + x)
                    else:
                        x = json_root['response']['result']['point']['x']
                        y = json_root['response']['result']['point']['y']
                        # print(datetime.datetime.now().isoformat() + "/ " + add + " / " + y + "," + x)
                        sys.stdout.flush()
                        #print('else문' + x, y)

                except Exception as e:
                    print(e)
                finally:
                    session.close()
            except Exception as e:
                print(e)
            return x, y


        if __name__ == "__main__":
            lat, lng = get_from_bunzi(loca)


        if restName[1] == '명동교자':
            search_result = '결과없음'
            print(search_result)
            print([indexfood,search_result])
            #wr.writerow([indexfood,search_result])
            break
        else:
            print([restName[1], loca, lat, lng, indexfood])
            wr.writerow([restName[1], loca, lat, lng, indexfood])
            


f.close()







import urllib.request
from bs4 import BeautifulSoup
import re
from collections import OrderedDict

#가나다
korCode = ['%EA%B0%80','%EB%82%98','%EB%8B%A4','%EB%9D%BC','%EB%A7%88','%EB%B0%94','%EC%82%AC','%EC%95%84','%EC%9E%90',
       '%EC%B0%A8','%EC%B9%B4','%ED%83%80','%ED%8C%8C','%ED%95%98']
kor = ['가','나','다','라','마','바','사','아','자','차','카','타','파','하']

#지역 구분
doNum = ['2','1','4','3','7','5','8','6','9']
do = ['서울/경기','강원도','충청남도','충청북도','경상남도','경상북도','전라남도','전라북도','제주도']

#지역별 음식 저장 할 리스트
locfood = [[],[],[],[],[],[],[],[],[]]



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
                #words = data4.split() #띄어쓰기 단위로 구분 후 가나다 별 리스트 형태로 음식명 저장
                #중복 제거
                #words2 = list(OrderedDict.fromkeys(words).keys())

                #지역별 음식명 리스트로 저장
                locfood[doIndex].append(data4)
            else:
                locfood[doIndex].append(data)

    print(locfood[doIndex])
    print(len(locfood[doIndex]))


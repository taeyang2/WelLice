import urllib.request
from bs4 import BeautifulSoup
import re

# 가나다
korCode = ['%EA%B0%80', '%EB%82%98', '%EB%8B%A4', '%EB%9D%BC', '%EB%A7%88', '%EB%B0%94', '%EC%82%AC', '%EC%95%84',
           '%EC%9E%90',
           '%EC%B0%A8', '%EC%B9%B4', '%ED%83%80', '%ED%8C%8C', '%ED%95%98']
kor = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하']


# 음식 코드 저장 할 리스트
food_code = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
jeju_food = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

count_kor = 0
count = 0


# 제주 향토음식 수집 (타 지역 비교 x)
for d in korCode:
    jeju_siteUrl = "https://www.nongsaro.go.kr/portal/ps/psr/psrc/areaCkRyLst.ps?menuId=PS03934&pageIndex=1&pageSize=10&pageUnit=10&type=09&schText="
    full_url = jeju_siteUrl + d
    #print(kor[korCode.index(d)])

    req = urllib.request.urlopen(full_url)
    res = req.read()

    soup = BeautifulSoup(res, 'html.parser')
    #data = str(soup.select(('li > table > tbody > tr > td > a')))
    data = soup.select(('li > table > tbody > tr > td > a'))

    for text in data:
        food = text.get_text().strip() #strip() : 양쪽 끝 /n 제거
        jeju_food[count_kor].append(food)
        #print(len(jeju_food[count_kor]))

    count_kor = count_kor + 1

    #print(jeju_food)



# 음식 코드 수집
    str_data = str(data)

    slice_lines = (str_data.split('</a>,'))
    #print(slice_lines)
    #print(slice_lines[0])
    

    for html in slice_lines:
        tag = re.findall(r"\'(.*?)\'", html) #음식 코드 추출
        food_code[count].extend(tag)

    #print(food_code)
    #print(food_code[count])
    #print(len(food_code[count]))

    #print("=====================================")

    count = count + 1
print('=========jeju_food==========')
print(jeju_food)
print('=========food_code==========')
print(food_code)

#(제주어) 제거
tmp = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

for list in jeju_food:
    for element in list:
        if '(' in element:
            del1 = re.sub(r'\([^)]*\)', '', element)
            tmp[jeju_food.index(list)].append(del1)
        else:
            tmp[jeju_food.index(list)].append(element)
    #print(tmp[jeju_food.index(list)])
print("==========tmp============")
print(tmp)

# 딕셔너리
sum_jeju_food = sum(tmp,[])
sum_food_code = sum(food_code, [])

#print(len(sum_jeju_food))
#print(len(sum_food_code))


food_dict = {}

for key in sum_jeju_food:
    food_dict[key] = sum_food_code[sum_jeju_food.index(key)]

from pprint import pprint as pp
pp(food_dict)







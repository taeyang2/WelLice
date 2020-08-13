import urllib.request
from bs4 import BeautifulSoup
import re
from pprint import pprint as pp
import csv

f = open('StuffDic9.csv','w',newline='')
wr = csv.writer(f)

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

pp(food_dict)

#print(len(food_dict))


# 식재료 데이터 수집
stuff = []
for val in food_dict.values():
    food_info_Url = "https://www.nongsaro.go.kr/portal/ps/psr/psrc/areaCkRyDtl.ps?menuId=PS03934&pageIndex=1&pageSize=10&pageUnit=10&cntntsNo="
    full_food_info_url = food_info_Url + val
    #print(full_food_info_url)

    req_food_info = urllib.request.urlopen(full_food_info_url)
    res_food_info = req_food_info.read()

    soup_food_info = BeautifulSoup(res_food_info, 'html.parser')
    #data = str(soup.select(('li > table > tbody > tr > td > a')))
    food_info_data = soup_food_info.select(('table > tbody > tr > td'))
    #print(food_info_data)
    stuff.extend(food_info_data[3])
    #print(stuff)

stuff_dict = {}

for code in sum_food_code:
    stuff_dict[code] = stuff[sum_food_code.index(code)]

pp(stuff_dict)

#딕셔너리 값(식재료) 수정
# val = stuff_dict.values()
# print(val)
# val_list = list(val)
# print(val_list)

for key, value in stuff_dict.items():
    ingredient = []

    print("value---", value)
    value = re.sub(r'\([^)]*\)', '', value)
    print("value2---", value)
    val_list = value.split(",")
    print("value3---", value)

    print("val_list---", val_list)
    for str in val_list:
        print("str---", str)
        a1 = re.sub(r'\([^)]*\)', '', str)
        print("a1---", a1)
        a2 = re.sub("[0-9]", '', a1)
        print("a2---", a2)
        a3 = re.sub("[a-z]", '', a2).strip()
        print("a3---", a3)
        a4 = a3.split(' ')
        print("a4---", a4)
        ingredient.append(a4[0])

    print(ingredient)
    # 딕셔너리 값 변경 코드
    stuff_dict[key] = ingredient

    for FoodName,FoodID in food_dict.items():
        if key == FoodID:

            print("결과!!!!!!!",FoodName, key, FoodID, ingredient)
            wr.writerow([FoodName, FoodID, ingredient])


    print("#########################")






#pp(stuff_dict)

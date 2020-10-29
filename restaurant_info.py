import csv
import json

# name, lat(위도), lng(경도), img, menu, address
# 경도(lng) : 127.0214236

input_file = 'C:/WelLice_ext/Search_result.csv'

with open(input_file, 'r', newline='') as csv_in_file:
    filereader = csv.reader(csv_in_file)
    restaurant_list = []  # 결과저장
    print("restaurant_list===", restaurant_list)
    for rows in filereader:
        # print(rows)
        restaurant_info = rows[1:]
        print("restaurant_info====", restaurant_info)
        if len(restaurant_list) != 0:
            print('=== 1 ===')
            in_address = []

            for info in restaurant_list:
                print('info===', info)
                print("info['address']===", info['address'])
                in_address.append(info['address'])
                print("in_address===", in_address)
            if restaurant_info[4] not in in_address:
                print('restaurant_info[0]===', restaurant_info[0])
                print('1-1')
                restaurant_list.append({'name': restaurant_info[0],
                                        'lat': restaurant_info[-1],
                                        'lng': restaurant_info[-2],
                                        'menu': restaurant_info[1:4],
                                        'address': restaurant_info[4]})
                print('RESULT_restaurant_list', restaurant_list)
            elif restaurant_info[4] in in_address:
                continue

        elif len(restaurant_list) == 0:
            print('2')
            restaurant = {}
            restaurant['name'] = restaurant_info[0]
            restaurant['lat'] = restaurant_info[-1]
            restaurant['lng'] = restaurant_info[-2]
            restaurant['menu'] = restaurant_info[1:4]
            restaurant['address'] = restaurant_info[4]
            restaurant_list.append(restaurant)

            print('1st_not_in_restaurant_list===', restaurant_list)

print(restaurant_list)

with open("restaurant.json", 'w', encoding='utf-8') as make_file:
    json.dump(restaurant_list, make_file, ensure_ascii=False, indent='\t')

print(len(restaurant_list)) # 809개




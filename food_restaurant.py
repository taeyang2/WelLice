import csv
import json

input_file = 'C:/WelLice_ext/Search_result.csv'

with open(input_file, 'r', newline='') as csv_in_file:
    filereader = csv.reader(csv_in_file)
    food_restaurant_list = []
    print("food_restaurant_list===", food_restaurant_list)
    
    for rows in filereader:
        # print(rows)
        temp_food_restaurant = {}
        temp_food_restaurant[rows[0]] = rows[1]
        print("temp_food_restaurant====", temp_food_restaurant)
        for food, restaurant in temp_food_restaurant.items():
            print("restaurant===", restaurant)
            # for ingredient in ingredient_list:
            # print("ingredient===", ingredient)
            if len(food_restaurant_list) != 0:
                print('=== 1 ===')
                in_food = []
                for food2 in food_restaurant_list:
                    print('food2===', food2)
                    print("food2['food']===", food2['food'])
                    in_food.append(food2['food'])
                    print("in_food===", in_food)
                if food not in in_food:
                    print('food===', food)
                    print('1-1')
                    food_restaurant_list.append({'food': food, 'restaurant': [restaurant]})
                    print('RESULT_food_restaurant_list', food_restaurant_list)
                elif food in in_food:
                    print('1-2')
                    for e in food_restaurant_list:
                        if e['food'] == food:
                            e['restaurant'].append(restaurant)
                            print('RESULT_food_restaurant_list', food_restaurant_list)
            elif len(food_restaurant_list) == 0:
                print('2')
                food_restaurant = {}
                food_restaurant['food'] = food
                food_restaurant['restaurant'] = [restaurant]
                food_restaurant_list.append(food_restaurant)

                print('1st_not_in_food_restaurant_list===', food_restaurant_list)

print(food_restaurant_list)

with open("food_restaurant.json", 'w', encoding='utf-8') as make_file:
    json.dump(food_restaurant_list, make_file, ensure_ascii=False, indent='\t')

# 제주향토음식 : 128개


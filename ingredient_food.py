import csv
import json

input_file = 'C:/WelLice_ext/stuffDic11.csv'

with open(input_file, 'r', newline='') as csv_in_file:
    filereader = csv.reader(csv_in_file)
    ingredient_food_list = [] #결과저장
    print("ingredient_food_list===",ingredient_food_list)
    #ingredient_food ={}
    for rows in filereader:
        #print(rows)
        temp_ingredient_food ={}
        temp_ingredient_food[rows[0]] = rows[2:]
        print("ingredient_food====",temp_ingredient_food)
        for FoodName, ingredient_list in temp_ingredient_food.items():
            print("ingredient_list===",ingredient_list)
            for ingredient in ingredient_list:
                print("ingredient===", ingredient)
                if len(ingredient_food_list) != 0:
                    print('=== 1 ===')
                    in_ingredient = []
                    for ingredient2 in ingredient_food_list:
                        print('ingredient2===',ingredient2)
                        print("ingredient2['ingredient']===",ingredient2['ingredient'])
                        in_ingredient.append(ingredient2['ingredient'])
                        print("in_ingredient===", in_ingredient)
                    if ingredient not in in_ingredient:
                        print('ingredient===', ingredient)
                        print('1-1')
                        ingredient_food_list.append({'ingredient':ingredient, 'food':[FoodName]})
                        print('RESULT_ingredient_food_list', ingredient_food_list)
                    elif ingredient in in_ingredient:
                        print('1-2')
                        for e in ingredient_food_list:
                            if e ['ingredient'] == ingredient:
                                e['food'].append(FoodName)
                                print('RESULT_ingredient_food_list', ingredient_food_list)
                elif len(ingredient_food_list) == 0:
                    print('2')
                    ingredient_food = {}
                    ingredient_food['ingredient'] = ingredient
                    ingredient_food['food'] = [FoodName]
                    ingredient_food_list.append(ingredient_food)
                
                    print('1st_not_in_ingredient_food===', ingredient_food_list)
                    
print(ingredient_food_list)

with open("ingredient_food.json",'w',encoding='utf-8') as make_file:
    json.dump(ingredient_food_list, make_file, ensure_ascii=False, indent='\t')


                        

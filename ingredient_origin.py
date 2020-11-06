import pandas as pd
import json

input_file = pd.read_excel('C:/WelLice_ext/식재료 유래 데이터.xlsx',
                           header=None,
                           keep_default_na=False)

input_file_df = input_file.dropna()

ingredient_origin_list = []

for index, row in input_file_df.iterrows():
     print("index===", index)
     print("row===", row)
     print("===========")

     ingredient = str(row[0]).strip()
     origin = str(row[1]).strip()

     ingredient_origin_list.append(
          {"ingredient" : ingredient,
           "origin" : origin
     })

print(ingredient_origin_list)

with open('ingredient_origin.json', 'w', encoding='utf-8') as make_file:
     json.dump(ingredient_origin_list, make_file, ensure_ascii=False, indent='\t')



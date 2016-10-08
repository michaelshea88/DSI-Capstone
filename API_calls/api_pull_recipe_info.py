# This script pulls 500 recipes from the Yummly recipe API

# To collect the 10k recipes for my analysis, I did 20 separate API pulls

# To make API calls you must get permission from the Yummly recipe API
# (https://developer.yummly.com/documentation_)

# Imports
import json
import requests
import pandas as pd
import numpy as np
import re

# API headers - ID and key
url = 'http://api.yummly.com/v1/api/recipes?'
headers = {'X-Yummly-App-ID':'your_ID', 'X-Yummly-App-Key':'your_key'}

# API search parameters
parameters = {'allowedCourse[]': 'course^course-Main Dishes',
              'excludedCourse[]': ['course^course-Appetizers', 'course^course-Salads',
                                   'course^course-Condiments and Sauces',
                                   'course^course-Lunch', 'course^course-Soups',
                                   'course^course-Snacks',
                                   'course^course-Breakfast and Brunch',
                                   'course^course-Side Dishes',],
              'allowedCuisine[]': 'cuisine^cuisine-asian',
              'excludedCuisine[]': ['cuisine^cuisine-american',
                                    'cuisine^cuisine-italian',
                                    'cuisine^cuisine-indian',
                                    'cuisine^cuisine-mexican', 'cuisine^cuisine-mediterranean',
                                    'cuisine^cuisine-chinese',
                                   'cuisine^cuisine-japanese'],
              'maxResult': 500,
             'start': 0}

# API call
response = requests.get(url, headers=headers, params=parameters)
print "Status code:", response.status_code

# Decode JSON
api_call = response.json()
print "Data type:", type(api_call)

# Print keys
response_keys = api_call.keys()
print "Response keys:", response_keys

# Print total match count
print "Total match count:", api_call['totalMatchCount']

# Extract data from decoded JSON, store in list of dicts
main_list = [] 
for search_result in api_call['matches']:
    sub_dict = {}
    sub_dict['id'] = search_result['id']
    sub_dict['recipe_name'] = search_result['recipeName']
    sub_dict['source_display_name'] = search_result['sourceDisplayName']
    sub_dict['course'] = search_result['attributes'].get('course')
    sub_dict['cuisine'] = search_result['attributes'].get('cuisine')
    sub_dict['ingredient_list'] = search_result['ingredients']
    
    main_list.append(sub_dict)

# Create Dataframe
df = pd.DataFrame(main_list)

# Send to .csv - change csv name with each API pull
df_main.to_csv('asian/main_as4.csv', encoding ='utf-8')

########

# Now make an additional set of API calls to get recipe_detail info
recipe_ids=[] #get list of recipe ids
for recipe in api_call['matches']:
    recipe_ids.append(recipe['id'])

# Second API call to get other features for each recipe
key_id= '' #need to get your own API key
url= 'http://api.yummly.com/v1/api/recipe/'

# Retrieve other features for all recipes
def get_recipe(_id):
    response = requests.get(url + _id + '?' + key_id)
    return response.json()

recipes=[]
for _id in recipe_ids :
    recipes.append(get_recipe(_id))
    
# For each recipe create a new dictionary of selected attributes and append into a list
recipe_details=[]
for recipe in recipes:
    _dict={}
    _dict['id']=recipe['id']
    _dict['ingredientCount']= len(recipe['ingredientLines'])
    _dict['numberOfServings']= recipe['numberOfServings']
    _dict['prepTimeInSeconds'] = recipe.get('prepTimeInSeconds')
    _dict['cookTimeInSeconds'] = recipe.get('cookTimeInSeconds')
    _dict['totalTimeInSeconds']= recipe.get('totalTimeInSeconds')
    
    recipe_details.append(_dict)

# Create dataframe
df_details=pd.DataFrame(recipe_details)

# Send to csv
df_details.to_csv('asian/main_as_details4.csv', encoding= 'utf-8') #change csv name with each API call
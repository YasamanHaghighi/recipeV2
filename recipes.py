import json
import requests

#X-Yummly-App-Key = 'da496643eba26f82c06429b0dd386eed'
#X-Yummly-App-ID = '4884cd95'
#api_url_base = 'https://api.yummly.com/v1/'

headers = {'Content-Type': 'application/json'}

keywords = input("Please enter your search string")
filename = keywords + '_info'
recipe_dic = {}



### Function to search for recipes
def search_recipe():

    api_url = 'http://api.yummly.com/v1/api/recipes?_app_id=4884cd95&_app_key=da496643eba26f82c06429b0dd386eed&q=' + keywords + '&requirePictures=true'
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

### Saving the results from search_recipe call
recipe_info = search_recipe()
if recipe_info is not None:
    print ("Successful")
    with open(filename, 'w') as outfile:
        json.dump(recipe_info, outfile)

else:
    print('[!] Request Failed')

with open(filename, 'r') as infile:
    recipe = json.loads(infile.read())

### Function to get recipes
def get_recipe():
    match_list=recipe["matches"]
    i=0
    with open('library', 'r') as infile:
        library = json.loads(infile.read())
    j=len(library)
    print (j)
    for matches in match_list:
        search_url = 'http://api.yummly.com/v1/api/recipe/' + match_list[i]["id"] + '?_app_id=4884cd95&_app_key=da496643eba26f82c06429b0dd386eed'
        api_url = search_url
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            recipe_info = json.loads(response.content.decode('utf-8'))
            recipe_dic[i]=recipe_info
            recipe_dic[i]["ingredients"]=recipe["matches"][i]["ingredients"]
            library[j]=recipe_dic[i]
            i += 1
            j += 1
        with open(keywords, 'w') as outfile:
            json.dump(recipe_dic, outfile)
        with open('library', 'w') as outfile:
            json.dump(library, outfile)
print ("Recipes are saved.")
get_recipe()

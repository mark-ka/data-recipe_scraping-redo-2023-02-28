# pylint: disable=missing-docstring,line-too-long
import sys
from os import path
import csv
from bs4 import BeautifulSoup
import requests


def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    soup = BeautifulSoup(html, "html.parser")
    recipes_soup = soup.find_all('div', class_= 'p-2 recipe-details')[:36]

    return parse_recipe(recipes_soup)


def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modelising a recipe'''
    recipes = []
    for recipe in article:
        name = recipe.find('p', class_='text-dark text-truncate w-100 font-weight-bold mb-0 recipe-name').string
        difficulty = recipe.find('span', class_='recipe-difficulty').string
        prep_time = recipe.find('span', class_='recipe-cooktime').string
        recipes.append({'name': name, 'difficulty': difficulty, 'prep_time': prep_time})

    return recipes

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    with open(f'recipes/{ingredient}.csv', 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=recipes[0].keys())
        writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    url = 'https://recipes.lewagon.com/'
    response = ''
    for page in range(start,4):
        new_response = requests.get(url, params={'search[query]': ingredient, 'page': page},).content
        response += str(new_response)
    return response

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file, encoding="utf-8")
    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        recipes = parse(scrape_from_internet(ingredient))
        write_csv(ingredient, recipes)
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()

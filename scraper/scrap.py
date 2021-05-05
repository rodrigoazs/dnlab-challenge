import time
import os
import requests
from itertools import chain
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from pymongo import MongoClient


# base URL
BASE_URL = 'https://www.urparts.com'

model = {
    "manufacturer": None,
    "category": None,
    "model": None,
    "part": None,
    "part_category": None
}


def scrap_a_tags(url, class_):
    # fix some sections url
    if url == 'index.cfm/page/catalogue/Doosan/Loader Parts/430':
        url = 'index.cfm/page/catalogue/Doosan/Loader Parts/430/Loader'

    # collect first page of list
    page = requests.get(os.path.join(BASE_URL, url))

    # create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # pull all content from the div
    content_list = soup.find(class_=class_)
    
    # 'index.cfm/page/catalogue/Hyundai/Forklift Parts/HDF20/HDF25/HDF30-5'
    if not content_list:
        return []

    # pull all instances of a tag within the div
    content_list_items = content_list.find_all('a')

    return content_list_items


def get_items(url, class_, model, column_fill):
    # pull all instances of a tag within the div
    content_list_items = scrap_a_tags(url, class_)

    # store items
    items = []

    # create for loop to collect href and names
    for content in content_list_items:
        url = content.get('href')
        name = content.contents[0].strip()
        new_model = model.copy()
        new_model[column_fill] = name
        items.append((url, new_model))

    return items


def get_parts(url, class_, model, column_fill_1, column_fill_2):
    # pull all instances of a tag within the div
    content_list_items = scrap_a_tags(url, class_)

    # store items
    items = []

    # create for loop to collect href and names
    for content in content_list_items:
        name = content.contents[0].split(' - ')[0].strip()
        category = None
        category_find = content.find_all('span')
        if len(category_find):
            category = category_find[0].contents[0].strip()
        new_model = model.copy()
        new_model[column_fill_1] = name
        new_model[column_fill_2] = category
        items.append(new_model)

    return items


def scrap_manufacturer():
    return get_items(
        'index.cfm/page/catalogue',
        'c_container allmakes',
        model,
        'manufacturer'
    )


def scrap_categories(item):
    return get_items(
        item[0],
        'c_container allmakes allcategories',
        item[1],
        'category'
    )


def scrap_models(item):
    return get_items(
        item[0],
        'c_container allmodels',
        item[1],
        'model'
    )


def scrap_parts(item):
    return get_parts(
        item[0],
        'c_container allparts',
        item[1],
        'part',
        'part_category'
    )


if __name__ == "__main__":
    start_time = time.time()

    # store catalogues
    manufacturers = scrap_manufacturer()

    # store categories
    all_categories = Parallel(
        n_jobs=4,
        verbose=50
    )(delayed(scrap_categories)(manufacturer) for manufacturer in manufacturers)
    all_categories = list(chain.from_iterable(all_categories))

    # store models
    all_models = Parallel(
        n_jobs=4,
        verbose=50
    )(delayed(scrap_models)(category) for category in all_categories)
    # all_models = [scrap_models(category) for category in all_categories]
    all_models = list(chain.from_iterable(all_models))

    # store models
    all_parts = Parallel(
        n_jobs=4,
        verbose=50
    )(delayed(scrap_parts)(model) for model in all_models)
    # all_parts = [scrap_parts(model) for model in all_models]
    all_parts = list(chain.from_iterable(all_parts))

    print("--- %s seconds ---" % (time.time() - start_time))
    print(len(all_parts))

    client = MongoClient('mongodb://mongodb:mongodb@mongodb:27017/')
    base = client['urparts']
    table = base['urparts']

    table.insert_many(all_parts)

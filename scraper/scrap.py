import time
import os
import requests
# import json
from itertools import chain
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from pymongo import MongoClient


# base URL
BASE_URL = 'https://www.urparts.com'


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


def get_items(url, class_):
    # pull all instances of a tag within the div
    content_list_items = scrap_a_tags(url, class_)

    # store items
    items = []

    # create for loop to collect href and names
    for content in content_list_items:
        url = content.get('href')
        name = content.contents[0].strip()
        items.append((url, name))

    return items


def get_parts(item, class_):
    url, manufacturer, category, model = item
    content_list_items = scrap_a_tags(url, class_)

    # store items
    items = []

    # create for loop to collect href and names
    for content in content_list_items:
        name = content.contents[0].split(' - ')[0].strip()
        part_category = None
        part_category_find = content.find_all('span')
        if len(part_category_find):
            part_category = part_category_find[0].contents[0].strip()
        item = {
            "manufacturer": manufacturer,
            "category": category,
            "model": model,
            "part": name,
            "part_category": part_category
        }
        items.append(item)

    return items


def scrap_manufacturer():
    return get_items(
        'index.cfm/page/catalogue',
        'c_container allmakes'
    )


def scrap_categories(item):
    items = get_items(
        item[0],
        'c_container allmakes allcategories'
    )
    items = list(map(lambda x: (x[0], item[1], x[1]), items))
    return items


def scrap_models(item):
    items = get_items(
        item[0],
        'c_container allmodels'
    )
    items = list(map(lambda x: (x[0], item[1], item[2], x[1]), items))
    return items


def scrap_parts(item):
    return get_parts(
        item,
        'c_container allparts'
    )


def urparts_scraper():
    """Initialize web scraping of URParts
    and save results to a MongoDB collection.
    """

    # scrap manufacturers
    manufacturers = scrap_manufacturer()
    print("Total of %s manufacturers" % (len(manufacturers)))
    # 16 manufacturers

    # scrap categories
    items = Parallel(
        n_jobs=8,
        verbose=50
    )(delayed(scrap_categories)(item) for item in manufacturers)
    categories = list(chain.from_iterable(items))
    print("Total of %s categories" % (len(categories)))
    # 42 categories

    # scrap models
    items = Parallel(
        n_jobs=8,
        verbose=50
    )(delayed(scrap_models)(item) for item in categories)
    models = list(chain.from_iterable(items))
    print("Total of %s models" % (len(models)))
    # 1230 models

    # scrap parts
    items = Parallel(
        n_jobs=8,
        verbose=50
    )(delayed(scrap_parts)(item) for item in models)
    parts = list(chain.from_iterable(items))
    print("Total of %s parts" % (len(parts)))
    # 4337412 parts

    # saving json for tests
    # with open('data.json', 'w') as outfile:
    #     json.dump(parts, outfile)

    # connect to a mongodb collection
    client = MongoClient('mongodb://mongodb:mongodb@mongodb:27017/')
    base = client.urparts
    collection = base.urparts

    # insert records
    collection.insert_many(parts)
    print("Inserted %s parts" % (len(parts)))

    # create indexes
    collection.create_index([
        ("manufacturer", "text"),
        ("category", "text"),
        ("model", "text"),
        ("part", "text"),
        ("part_category", "text"),
    ])
    print("Created indexes")


if __name__ == "__main__":
    start_time = time.time()
    urparts_scraper()
    print("--- Script took %s seconds ---" % (time.time() - start_time))

# Declare library
import requests
import pandas as pd
#from time import sleep
#import random
#import json

headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': 'Bearer undefined',
    'origin': 'https://winmart.vn',
    'referer': 'https://winmart.vn/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# Declare variable
category_link = []
product = []

# Dataframe include category, link
response = requests.get('https://api-crownx.winmart.vn/mt/api/web/v1/category', headers = headers)
if response.status_code == 200:
    print('request success')
    for record in response.json().get('data'):
        category_link.append({'category': record['parent'].get('name'), 'link': "https://winmart.vn/" + record['parent'].get('seoName'), 'info': record['parent'].get('seoName')})

df = pd.DataFrame(category_link[4:])

# loop dataframe to give info and link
for i in range(df.shape[0]):
    info = df['info'][i]
    link = df['link'][i]
    params = {
        'orderByDesc': 'true',
        'pageNumber': '1',
        'pageSize': '8',
        'slug': info,
        'storeCode': '1535'
    }

    response = requests.get('https://api-crownx.winmart.vn/it/api/web/v2/item/category', params = params)
    
    #get totalcount, page
    if response.status_code == 200:
        print('request success')
    totalCount = response.json()['paging'].get('totalCount')
    page = response.json()['paging'].get('totalPages')
    print(page)
    
    
    for i in range(page):
        params = {
            'orderByDesc': 'true',
            'pageNumber': str(i+1),
            'pageSize': '8',
            'slug': info,
            'storeCode': '1535'
    }
        print(range(page))
        print(str(i+1))
        print(info)
        response = requests.get('https://api-crownx.winmart.vn/it/api/web/v2/item/category', params = params)

        if response.status_code == 200:
            print('request success')
        count = 0
        for record in response.json().get('data').get('items'):
            product.append({'product name': record.get('name').strip(),
                                'salePrice': record.get('salePrice'),
                                'sell unit': record.get('uomName'),
                                'category_link': link,
                                'url': 'https://winmart.vn/products/' + record.get('seoName')
                                })
            print(count)
            if count == totalCount:
                break
            count=count+1

productt1 = pd.DataFrame(product)



        


# Declare library
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from time import sleep
from datetime import datetime
import random
import math

# Incognito chrome 
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

# Declare browser
driver = webdriver.Chrome(chrome_options=chrome_options ,executable_path='C:/Users/MINH THUAN/Dropbox/My PC (LAPTOP-EPADQ5CQ)/Desktop/workspace/CRAWLING/LazadaCrawler/chromedriver.exe')

# Declare avaiables which present the amount of data crawled and category
data_count = 0
category = []
df = []

# Open URL
driver.get("https://www.bachhoaxanh.com/")

# Sleep few seconds
sleep(random.randint(5,10))

# Dataframe include category, subcategory, link
elems = driver.find_elements(By.CSS_SELECTOR , '.CateItem > .nav-parent')
cat = [elem.text for elem in elems]

for i  in range(len(elems)):
    subs = driver.find_elements(By.XPATH , '//*[@id="colmenuId"]/li['+ str(i+2) +']/div[2]/div/a')   
    for sub in subs:
        category.append({'category': cat[i], 'subcategory': sub.get_attribute('text'), 'link': sub.get_attribute('href')})

cat_frame = pd.DataFrame(category) 
  
# Filter dataframe 
cat_selected = cat_frame[cat_frame['category'] == 'BÁNH KẸO CÁC LOẠI'].copy().reset_index(drop = True)

# Access browers by link from dataframe
for i in range(cat_selected.shape[0]):
    driver.get(cat_selected['link'][i])
    
#TH1: có class .groupcate.temp.top
    try:
        elems = driver.find_elements(By.CSS_SELECTOR , '.groupcate.temp.top > div > ul > li > a')
        subs = [elem.get_attribute("href") for elem in elems]
        
        for sub in subs:
            print(sub)
            driver.get(sub) 
            elem = driver.find_element(By.CSS_SELECTOR , '.nextPaging.product.br-total')
            total_product = int(elem.get_attribute("data-total"))
            print(total_product)
            
            # Add to check data crawl
            data_count = data_count + total_product
            
             # loop each link, count page with each page = 20 products
            page = math.ceil(total_product/20)
            
            #scroll with approximately 5500px, after 2 page, we can see class viewmore, depend on how many page to loop and get data
            
            for i in range(1, 5500, 500):
                driver.execute_script("window.scrollTo(0, {});".format(i))
                sleep(2)
                
            count = 3
            if page > 2:
                while page >= count:
                    try:
                        button = driver.find_element(By.CSS_SELECTOR , '.viewmore')
                        ActionChains(driver).move_to_element(button).click().perform()
                    except NoSuchElementException:
                        #sometime max product in last page more 20 product. So I want check with try except.
                        print('current page = {} < total page = {}'.format(count, page) )
                        break
                    else:
                        count = count + 1
                        sleep(3)
                
            #get data
            elems = driver.find_elements(By.CSS_SELECTOR , '.cate > li')
            sku = [elem.get_attribute("data-product") for elem in elems]
            barcode = [elem.get_attribute("data-sku") for elem in elems]
            price = [elem.get_attribute("data-priceonbill") for elem in elems]
                
            elems = driver.find_elements(By.CSS_SELECTOR , '.cate > li > a:first-child')
            product_name = [elem.get_attribute("title") for elem in elems]
            link_sku = [elem.get_attribute("href") for elem in elems]
            linkcategory = ['https://www.bachhoaxanh.com/mi' for elem in elems]
            DateUpdate = [ datetime.today().strftime('%Y-%m-%d') for elem in elems]
            
            for i in range(len(product_name)):
                df.append({'sku': sku[i], 'product_name': product_name[i], 'barcode': barcode[i], 'price': price[i],'link_sku': link_sku[i], 'linkcategory': linkcategory[i], 'DateUpdate': DateUpdate[i]})
#------------------------------------------------------------ 
    except NoSuchElementException:
        print('Case 2')
#------------------------------------------------------------
#TH2: không có listgroup:   
    else:    
        elem = driver.find_element(By.CSS_SELECTOR , '.nextPaging.product.br-total')
        total_product = int(elem.get_attribute("data-total"))
        print(total_product)
        # add to check data crawl
        data_count = data_count + total_product
        page = math.ceil(total_product/20)
    
    #scroll with approximately 5500px, after 2 page, we can see button to viewmore, depend on how many page to loop and get data
    
        for i in range(1, 5500, 500):
            driver.execute_script("window.scrollTo(0, {});".format(i))
            sleep(2)
        
        count = 3
        if page > 2:
            while page >= count:
                try:
                    button = driver.find_element(By.CSS_SELECTOR , '.viewmore')
                    ActionChains(driver).move_to_element(button).click().perform()
                except NoSuchElementException:
            #sometime max product in last page more 20 product. So I want check with try except.
                    print('current page = {} < total page = {}'.format(count, page) )
                    break
                else:
                    count = count + 1
                    sleep(3)
        
        #get data
        elems = driver.find_elements(By.CSS_SELECTOR , '.cate > li')
        sku = [elem.get_attribute("data-product") for elem in elems]
        barcode = [elem.get_attribute("data-sku") for elem in elems]
        price = [elem.get_attribute("data-priceonbill") for elem in elems]
            
        elems = driver.find_elements(By.CSS_SELECTOR , '.cate > li > a:first-child')
        product_name = [elem.get_attribute("title") for elem in elems]
        link_sku = [elem.get_attribute("href") for elem in elems]
        linkcategory = ['https://www.bachhoaxanh.com/mi' for elem in elems]
        DateUpdate = [ datetime.today().strftime('%Y-%m-%d') for elem in elems]
        for i in range(len(product_name)):
            df.append({'sku': sku[i], 'product_name': product_name[i], 'barcode': barcode[i], 'price': price[i],'link_sku': link_sku[i], 'linkcategory': linkcategory[i], 'DateUpdate': DateUpdate[i]})
data = pd.DataFrame(df)

# Check data count,data dataframe
print('{}={}'.format(data_count, data.shape[0]))       

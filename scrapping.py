import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
from requests_html import HTMLSession
import datetime
import os
import pandas as pd
import mysql.connector
small_wait = 5
big_wait = 5
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
driver_path = os.path.join(os.getcwd(), 'chromedriver')

def find_https(x):
    """
    The function extract the https link from a given string
    """
    i = 0
    start = None
    end = None
    for i in range(0,len(x)):
        if i < (len(x) - 4):
            string = x[i:i+4]
            if string == "http":
                start = i
        if start != None and x[i] == '"':
            end = i
    return x[start:end]
def find_zip_code(x):
    """
    The function extract the zip code <ddddd> from a given string 
    """
    i = 0
    j = 4
    for i in range(1,len(x)-6):
        string = x[i-1:i+6]
        cond = (string[1:-1].isnumeric(), not string[0].isnumeric(), not string[-1].isnumeric())
        if all(cond):
            return x[i:i+5]
def get_urls(search_key = "Roma, Roma", select_key = 0):
    """
    The function takes the urls from the search page of the website
    """
    print(driver_path)
    driver = webdriver.Chrome(driver_path, options=chrome_options)  # Optional argument, if not specified will search path.
    driver.get('https://www.astegiudiziarie.it/Immobili/Risultati')
    time.sleep(small_wait)
    driver.find_element_by_id('filter-category').click()
    time.sleep(small_wait)
    driver.find_element_by_xpath("//ul[@id='categories_filter']/li[@data-option-id='1']").click()
    time.sleep(small_wait)
    driver.find_elements_by_xpath("//div[@class='clefted']/a")[1].click()
    time.sleep(small_wait)
    while True:
        try:
            location = driver.find_element_by_xpath("//span[@id='location-span']/input[@id='location']")
            location.click()
            time.sleep(small_wait)
            location.send_keys(search_key)
            time.sleep(small_wait)
            locatoin_text = driver.find_elements_by_xpath("//ul[@class='ui-menu ui-widget ui-widget-content ui-autocomplete highlight ui-front']/li")[select_key].text
            loc = driver.find_elements_by_xpath("//ul[@class='ui-menu ui-widget ui-widget-content ui-autocomplete highlight ui-front']/li")[select_key].click()
            print("The location is:", locatoin_text)
            l1['text'] = "The location is: " + locatoin_text
            break
        except:
            pass

    n_items = 0
    while True:
        time.sleep(small_wait)
        items = driver.find_elements_by_class_name("listing-item")
        hover = items[-2]
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element(hover).perform()
        time.sleep(big_wait)
        if n_items < len(items):
            n_items = len(items)
        else:
            break

    urls = driver.find_elements_by_xpath("//div[@class='listing-item']/a")
    urls = [url.get_attribute('href') for url in urls]
    urls = set(urls)
    db = mysql.connector.connect(
                user='root', database='astegiudiziarie',
                host='localhost', password='9903', port=3306)
    db.autocommit = True
    cur = db.cursor()
    cur.execute("select url from urls where region='{}'".format(locatoin_text))
    pre_urls = [u[0] for u in cur.fetchall()]
    for url in urls:
        print(url)
        if url not in pre_urls:
            cur.execute('insert into urls(region, url, date) values("{}","{}","{}")'.format(locatoin_text, url, datetime.date.today()))
            print('New url added')
        else:
            print('The url exists')
    cur.close()
    db.close()
    driver.get_screenshot_as_file("capture.png")
    driver.close()
    driver.quit()

def get_list_to_scrap():
    db = mysql.connector.connect(
                user='root', database='astegiudiziarie',
                host='localhost', password='9903', port=3306)
    db.autocommit = True
    cur = db.cursor()
    cur.execute("select url, region from urls")
    data_urls_regions = [(u[0], u[1]) for u in cur.fetchall()]
    urls = [u[0] for u in data_urls_regions]
    regions = [u[1] for u in data_urls_regions]
def get_data(urls, regions):

    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)  # Optional argument, if not specified will search path.
    db = mysql.connector.connect(
                user='root', database='astegiudiziarie',
                host='localhost', password='9903', port=3306)
    db.autocommit = True
    cur = db.cursor()
    cur.execute("select * from data")
    columns = cur.column_names
    columns = list(columns)
    _ = cur.fetchall()
    Data = []
    for u,r in zip(urls,regions):
        data = {}
        data['url'] = u
        try:
            print(u)
            driver.get(u);
            time.sleep(big_wait)
            try:
                driver.find_element_by_xpath("div[@class='col-md-12 text-center']")
                data['page_status'] = 'error'
                continue
            except:
                data['page_status'] = 'OK'
                data['directory'] = "media/{}/".format(r) + u.split('-')[-1]
                try:
                    driver.find_element_by_xpath("//ul[@class='nav nav-tabs']/li/div/a[@href='#pictures']").click()
                    time.sleep(2*small_wait)
                    images_1 = driver.find_elements_by_xpath("//div[@class='property-slider-pictures-nav slick-initialized slick-slider']/div[@aria-live='polite']/div[@class='slick-track']/div[@class='item slide-preview slick-slide slick-cloned']/img")
                    images_2 = driver.find_elements_by_xpath("//div[@class='property-slider-pictures-nav slick-initialized slick-slider']/div[@aria-live='polite']/div[@class='slick-track']/div[@class='item slide-preview slick-slide']/img")
                    images = images_1 + images_2
                    for image in images:
                        img_url = image.get_attribute("src")
                        directory = "media/{}/".format(r) + img_url.split('/')[-1] + "/FOTO"
                        file_name = img_url.split('/')[-2]
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        response = requests.get(img_url)
                        file = open("{}/{}".format(directory, file_name), "wb")
                        file.write(response.content)
                        file.close()
                except:
                    pass

                time.sleep(2*small_wait)
                try:
                    driver.find_element_by_xpath("//ul[@class='nav nav-tabs']/li/div/a[@href='#plants']").click()
                    images = driver.find_elements_by_xpath("//div[@class='property-slider-plants-nav slick-initialized slick-slider']/div[@aria-live='polite']/div[@class='slick-track']/div/img")
                    for image in images:
                        img_url = image.get_attribute("src")
                        directory = "media/{}/".format(r) + img_url.split('/')[-1] + "/PLANIMETRIA"
                        file_name = img_url.split('/')[-2]
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        response = requests.get(img_url)
                        file = open("{}/{}".format(directory, file_name), "wb")
                        file.write(response.content)
                        file.close()
                except:
                    pass
                time.sleep(2*small_wait)


                try:
                    pdfs = [div.find_element_by_xpath('..') for div in driver.find_elements_by_xpath("//div[@class='widget hidden-sm hidden-xs']/h3") if div.text == 'Allegati']
                    for a in pdfs[0].find_elements_by_tag_name('a'):
                        href = a.get_attribute('href')            
                        directory = "media/{}/".format(r) + href.split('/')[-1] + "/pdf"
                        file_name = href.split('/')[-2]
                        print(directory)
                        print(file_name)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        response = requests.get(href)
                        file = open("{}/{}".format(directory, file_name), "wb")
                        file.write(response.content)
                        file.close()

                except:
                    pass
                try:
                    print(driver.find_element_by_xpath("//div[@class='title-bar-auction-left']").text)
                    data['cod'] = driver.find_element_by_xpath("//div[@class='title-bar-auction-left']").text
                except:
                    print("there is no COD.")
                    data['cod'] = None
                try:
                    print(driver.find_element_by_xpath("//div[@class='title-bar-auction-right']").text)
                    data['status'] = driver.find_element_by_xpath("//div[@class='title-bar-auction-right']").text
                except:
                    print("there is no status")
                    data['status'] = None
                try:
                    driver.find_element_by_xpath("//div[@class='property-title']/h2/span").text
                    print(driver.find_element_by_xpath("//div[@class='property-title']/h2").text.replace(" " + driver.find_element_by_xpath("//div[@class='property-title']/h2/span").text,""))
                    print(driver.find_element_by_xpath("//div[@class='property-title']/h2/span").text)
                    data['last_status'] = driver.find_element_by_xpath("//div[@class='property-title']/h2").text.replace(" " + driver.find_element_by_xpath("//div[@class='property-title']/h2/span").text,"")
                    data['last_update'] = driver.find_element_by_xpath("//div[@class='property-title']/h2/span").text
                except:
                    try:
                        print(driver.find_element_by_xpath("//div[@class='property-title']/h2").text)
                        data['last_status'] = driver.find_element_by_xpath("//div[@class='property-title']/h2").text
                        print("-")
                        data['last_update'] = None
                    except:
                        print("-")
                        data['last_status'] = None
                        data['last_update'] = None
                        print("-")
                E = driver.find_elements_by_xpath("//div[@class='property-description']/div[@class='row legal-row']")
                time.sleep(2)
                for e in E:
                    table = e.find_element_by_xpath("div[@class='col-md-12 legal-header']").text
                    print(table,":")
                    if table == 'Dati relativi al lotto':
                        x = e.find_element_by_xpath("div[@class='col-md-12 legal-row-desc']/p").text
                        print(x)
                        data[table + '_' + 'description'] = x
                    if table == 'Dati relativi ai beni':
                        y = e.find_element_by_xpath("div[@class='col-md-12 legal-row-desc']/h4").text
                        x = e.find_element_by_xpath("div[@class='col-md-12 legal-row-desc']/p").text
                        print(y)
                        data[table + '_' + 'tipo'] = y
                        data[table + '_' + 'description'] = x
                        print(x)
                    D = e.find_elements_by_xpath("div[@class='col-md-12 legal-row-desc']/div[@class='row legal-row-detail']")
                    for d in D:
                        for i in d.find_elements_by_xpath('div'):
                            if i.get_attribute('class') != 'clearfix nascondi':
                                y,z = i.find_elements_by_xpath('div')
                                print(y.text,":",z.text)
                                data[table + '_' + y.text] = z.text
                map_url = find_https(driver.find_element_by_xpath("//div[@id='propertyMap-container']/a[@class='popup-gmaps street-view-btn nascondi']").get_attribute('onClick'))
                driver.get(map_url)
                time.sleep(5)
                url = driver.current_url
                try:
                    session = HTMLSession()
                    response = session.get(url)
                    time.sleep(5)
                    lat, log = url[-50:].split("!3d")[1].split("!4d")
                    v = lat + ',' + log
                    x = response.text[response.text.find(v)-60:response.text.find(v)]
                    z = find_zip_code(x)
                    print(z)
                    data['zip'] = z
                    session.close()
                except:
                    print('ridam')
        except:
            pass
        data['get_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cols = []
        values = []
        for col, value in data.items():
            if value not in ["-", "", " ", None]:
                cl = col.replace(" ", "_")
                print(cl, ":", value)       
                if cl == "url":
                    cols.append(cl)
                    values.append('''"{}"'''.format(value))
                elif cl == "Dati_relativi_ai_beni_METRI_QUADRI":
                    cols.append(cl)
                    values.append('''"{}"'''.format(value))
                    try:
                        value = float(value.replace(',', '.'))
                        cols.append(cl + "_MIN")
                        values.append(str(value))
                    except:
                        try:
                            MIN, MAX = value.split("-")
                            MIN = float(MIN)
                            MAX = float(MAX)
                            values.append(str(MIN))
                            values.append(str(MAX))
                            cols.append(cl + "_MIN")
                            cols.append(cl + "_MAX")
                        except:
                            pass
                elif cl in ["Dati_relativi_alla_Vendita_TERMINE_PRESENTAZIONE_OFFERTE", "Dati_relativi_alla_Vendita_DATA_E_ORA_UDIENZA", "Dati_relativi_alla_Vendita_DATA_E_ORA_VENDITA"]:
                    cols.append(cl)
                    x = value.split()
                    d = x[0].split('/')
                    d.reverse()
                    value = "-".join(d) + " " + x[-1]
                    values.append('''"{}"'''.format(value))
                elif cl in ['Dati_relativi_alla_Vendita_PREZZO_BASE', 'Dati_relativi_alla_Vendita_OFFERTA_MINIMA', 'Dati_relativi_alla_Vendita_RIALZO_MINIMO_IN_CASO_DI_GARA']:
                    cols.append(cl)
                    value = float(value.replace("€ ", "").replace(".","").replace(",", "."))
                    values.append(str(value))
                elif cl == "Dettaglio_procedura_e_contatti_RUOLO":
                    cols.append(cl)
                    values.append('''"{}"'''.format(value))
                    try:
                        r1,r2 = value.split("/")
                        r1 = int(r1)
                        r2 = int(r2)
                        values.append(str(r1))
                        values.append(str(r2))
                        cols.append(cl + "_1")
                        cols.append(cl + "_2")
                    except:
                        pass
                elif cl == "zip":
                    cols.append(cl)
                    values.append(value)
                else:
                    if cl not in columns:
                        cur.execute("ALTER TABLE `astegiudiziarie`.`data` ADD COLUMN `{}` VARCHAR(200) NULL;".format(cl))
                        columns.append(cl)
                    cols.append(cl)
                    values.append('''"{}"'''.format(value.replace("'", "").replace('"', "")))

        cols = ",".join(cols)
        values = ",".join(values)
        if len(data.keys()) > 5:
            cur.execute("""REPLACE INTO data({}) VALUES({})""".format(cols, values))
    driver.close()
    driver.quit()


import tkinter as tk
def run_get_urls():
    get_urls(search_key=e1.get(), select_key=int(e2.get()))

def run_get_data():
    get_data()
master = tk.Tk()
master.title("Agha Sadegh")

row = 0
tk.Label(master, 
         text="Text Search").grid(row=row, column=0)
e1 = tk.Entry(master)
e1.grid(row=row, column=1)
tk.Label(master, 
         text="Item to Select").grid(row=row, column=2)
e2 = tk.Entry(master)
e2.grid(row=row, column=3)
tk.Button(master, 
          text='GET URLS', 
          command=run_get_urls).grid(row=row, 
                                    column=4, 
                                    sticky=tk.W, 
                                    pady=4)
row = 1
l1 = tk.Label(master, 
         text="The region is: --")
l1.grid(row=row, column=0)



row = 2
tk.Label(master, 
         text="Date").grid(row=row, column=0)
t1 = tk.Entry(master)
t1.grid(row=row, column=1)
# tk.Label(master, 
#          text="Item to Select").grid(row=row, column=2)
# t2 = tk.Entry(master)
# t2.grid(row=row, column=3)
tk.Button(master, 
          text='GET DATA', 
          command=run_get_urls).grid(row=row, 
                                    column=4, 
                                    sticky=tk.W, 
                                    pady=4)
row = 3
tk.Button(master, 
          text='Exit', command=master.quit).grid(row=row, 
                                                       column=0, 
                                                       sticky=tk.W, 
                                                       pady=4)
tk.mainloop()



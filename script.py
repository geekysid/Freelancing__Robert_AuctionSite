#!/usr/local/bin/python3


# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#   Name: Siddhant Shah                             #
#   Date: 30/01/2021                                #
#   Desc: SCRAPER FOR LENOVO UCTION SITE            #
#   Email: siddhant.shah.1986@gmail.com             #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init
from termcolor import cprint
import time, json, os, sys


# global variables
DATA = {}
CONFIG_DATA = {}
WAIT_TIME = 10
BROWSER = ''

# just fro decoration
def intro_deco():
    print("\n\n")
    print("  ", '#'*40)
    print("  ", "#                                      #")
    print("  ", "#   SCRAPER FOR LENOVO AUCTION SITE    #")
    print("  ", "#           By: SIDDHANT SHAH          #")
    print("  ", "#             Dt: 30-01-2021           #")
    print("  ", "#     siddhant.shah.1986@gmail.com     #")
    print("  ", "#   **Just for Educational Purpose**   #")
    print("  ", "#                                      #")
    print("  ", '#'*40)
    print()


# getting information from config file
def initializer():
    global CONFIG_DATA
    global MODEL_NUMB

    if os.path.exists(f'{os.getcwd()}/config.json'):
        with open (f'{os.getcwd()}/config.json', 'r') as r:
            CONFIG_DATA = json.load(r)


# Setting up webdriver
def get_browser(headless=False):
    global BROWSER

    # linux
    if sys.platform == "linux" or sys.platform == "linux2":
        pass
    # OS X
    elif sys.platform == "darwin":
        pathToChromeDriver = f"{os.getcwd()}/chromedriver"

    # Windows
    elif sys.platform == "win32":
        pathToChromeDriver = f'{os.getcwd()}/chromedriver'

    else:
        pass
        # print(sys.platform)

    chrome_options = Options()

    # giving a higher resolution to headless browser so that click operation works
    if headless:
        chrome_options.headless = headless
    else:
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument("--start-maximized")

    BROWSER = webdriver.Chrome(executable_path = pathToChromeDriver, options=chrome_options)


# getting element from config
def get_element(selector, base=''):

    base = BROWSER if (base == '') else base
    selector_type = list(selector.keys())[0]

    if selector_type == 'class':
        return base.find_element_by_class_name(selector[selector_type])
    elif selector_type == 'id':
        return base.find_element_by_id(selector[selector_type])
    elif selector_type == 'attribute':
        selector_tag =selector[list(selector.keys())[1]]
        return base.find_element_by_xpath(f"//{selector_tag}[{selector[selector_type]}]")
    elif selector_type == 'tag_name':
        return base.find_element_by_tag_name(selector[selector_type])


# getting elements from config
def get_elements(selector, base=''):

    base = BROWSER if (base == '') else base
    selector_type = list(selector.keys())[0]

    if selector_type == 'class':
        return base.find_elements_by_class_name(selector[selector_type])
    if selector_type == 'id':
        return base.find_elements_by_id(selector[selector_type])


# getting laptops that are on auction
def get_laptop_on_sale():
    laptops = set()
    selector = CONFIG_DATA['selectors']
    WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, selector['items_per_page']['id']))).send_keys('100')
    # WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, selector['items_per_page']['id'])))
    time.sleep(5)

    # fetching laptops on auction
    result_container = get_element(selector['auction_search_results_container'])
    total_laptops = get_elements(selector['individual_laptop_url'], result_container)
    for laptop in total_laptops:
        laptop_url = laptop.get_attribute('href')
        if 'lot' in laptop_url:
            laptops.add(laptop_url)

    for laptop_url in laptops:
        BROWSER.get(laptop_url)
        WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[5]/div[2]/div[3]/div/div[1]/div[1]/div[1]/h1')))
        print(get_element(selector['laptop_title']).text)
        print(get_element(selector['lot-closing-countdown']).text)
        print(get_element(selector['current-bid']).text)
        print(get_element(selector['lot-quantity']).text)
        print(get_element(selector['lot-number']).text)
        print(get_element(selector['lot-condition']).text)
        print(get_element(selector['lot-premium']).text)
        print(get_element(selector['lot-gst']).text)
        print(get_element(selector['lot-warranty']).text)
        print(get_element(selector['lot-details']).find_elements_by_tag_name('ul')[1].find_elements_by_tag_name('li')[0].text)
        print(get_element(selector['lot-details']).find_elements_by_tag_name('ul')[1].find_elements_by_tag_name('li')[1].text)

        description = get_element(selector['lot-description']).find_elements_by_tag_name('li')
        for desc in description:
            text = desc.text
            if 'RAM' in text:
                print(f'Memory: {text}')
            elif 'Part Number' in text:
                print(f'Part Number: {text}')
            elif 'GB' in text:
                print(f'Storage: {text}')
            elif 'Core' in text or 'GHz' in text:
                print(f'Processor: {text}')

        bidding_history = get_element(selector['bidding_history'])
        bidding_history.click()
        bidding_rows = get_element(selector['bidding_table']).find_elements_by_tag_name('tr')
        for bidding_row in bidding_rows:
            details = bidding_row.find_element_by_class_name(selector['bidding-details']['class']).text
            time_ = bidding_row.find_element_by_class_name(selector['bid-time']['class']).text
            price = bidding_row.find_element_by_class_name(selector['bid-price']['class']).text
            bid_qty = bidding_row.find_element_by_class_name(selector['bid-qty']['class']).text
            win_qty = bidding_row.find_element_by_class_name(selector['win-qty']['class']).text
            print(details, time_, price, bid_qty, win_qty)





        # print(get_element(selector['lot-number']).text)
        # print(get_element(selector['lot-number']).text)
        # print(get_element(selector['lot-number']).text)
        # print(get_element(selector['lot-number']).text)
        # print(get_element(selector['lot-number']).text)
        # print(get_element(selector['lot-number']).text)
        input('----------------')




# getting required data from website
def get_required_data():
    pass
    get_laptop_on_sale()
    # get_heading_section(browser)
    # get_features_section(browser)
    # get_specifications(browser)


# executing script only if its not imported
if __name__ == '__main__':
    # try:
        init()
        intro_deco()
        initializer()
        get_browser(headless=False)
        for url in CONFIG_DATA['url']:
            # print(url)
            BROWSER.get(url)
            get_required_data()
        BROWSER.quit()
    # except Exception as error:
    #     cprint(f'  [+] EXCEPTION: {str(error)}', 'red', attrs=['bold'])


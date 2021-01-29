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

    browser = webdriver.Chrome(executable_path = pathToChromeDriver, options=chrome_options)

    return browser


# getting elements from config
def get_element(selector, base=BROWSER):
    selector_type = selector.keys()[0]
    if selector_type == 'class':
        return base.find_element_by_class(selector[selector_type])
    if selector_type == 'id':
        return base.find_element_by_class(selector[selector_type])


# getting laptops that are on auction
def get_laptop_on_sale():
    selector = CONFIG_DATA['selectors']
    WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, selector['items_per_page']['id']))).select_by_visible_text('100')
    # WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, selector['items_per_page']['id'])))
    time.sleep(5)

    # fetching laptops on auction
    result_container = get_element(selector['auction_search_results_container'])
    total_laptops = get_element(selector['individual_laptop_column'], result_container)
    input(len(total_laptops))


# getting required data from website
def get_required_data():
    pass
    get_laptop_on_sale()
    # get_heading_section(browser)
    # get_features_section(browser)
    # get_specifications(browser)


# executing script only if its not imported
if __name__ == '__main__':
    try:
        init()
        intro_deco()
        initializer()
        BROWSER = get_browser(headless=False)
        for url in CONFIG_DATA['url']:
            # print(url)
            BROWSER.get(url)
            get_required_data()
        browser.quit()
    except Exception as error:
        cprint(f'  [+] EXCEPTION: {str(error)}', 'red', attrs=['bold'])


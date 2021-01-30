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
WAIT_TIME = 5
BROWSER = ''
INVALID_URL = 0


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

    try:
        if selector_type == 'class':
            return base.find_element_by_class_name(selector[selector_type])
        elif selector_type == 'id':
            return base.find_element_by_id(selector[selector_type])
        elif selector_type == 'attribute':
            selector_tag =selector[list(selector.keys())[1]]
            return base.find_element_by_xpath(f"//{selector_tag}[{selector[selector_type]}]")
        elif selector_type == 'tag_name':
            return base.find_element_by_tag_name(selector[selector_type])
    except Exception as err:
        # cprint(f'    [x] Exeption: Can\'t locate selector. \n{str(err)}', 'red', attrs=['bold'])
        pass


# getting elements from config
def get_elements(selector, base=''):

    base = BROWSER if (base == '') else base
    selector_type = list(selector.keys())[0]

    if selector_type == 'class':
        return base.find_elements_by_class_name(selector[selector_type])
    if selector_type == 'id':
        return base.find_elements_by_id(selector[selector_type])


# checking if any element in array is substring of a string
def check_if_substring_exists(substringArr, bigString):
    for substring in substringArr:
        if substring in bigString:
            return True
    return False


# details of lapt that is being auctioned
def get_autioned_laptop_details(selector):
    description = get_element(selector['lot-description']).find_elements_by_tag_name('li')
    laptop_details = {}

    for desc in description:
        text = desc.text
        if check_if_substring_exists(CONFIG_DATA['Memory'], text):
            laptop_details['Memory'] = text
            cprint(f'          [>>] Memory: {text}', 'cyan', attrs=['bold'])

        if check_if_substring_exists(CONFIG_DATA['Part'], text):
            laptop_details['Part Number'] = text
            cprint(f'          [>>] Part Number: {text}', 'cyan', attrs=['bold'])

        if check_if_substring_exists(CONFIG_DATA['Storage'], text):
            laptop_details['Storage'] = text
            cprint(f'          [>>] Storage: {text}', 'cyan', attrs=['bold'])

        if check_if_substring_exists(CONFIG_DATA['Processor'], text):
            laptop_details['Processor'] = text
            cprint(f'          [>>] Processor: {text}', 'cyan', attrs=['bold'])

    DATA[BROWSER.current_url.rsplit("/", 1)[-1]]['laptop_details'] = laptop_details


# details of bidding for the laptop
def get_bidding_details(selector):
    global DATA

    bidding_history = get_element(selector['bidding_history'])
    bidding_history.click()
    bidding_details = []
    bid_count = 0
    while True:
        bidding_rows = get_element(selector['bidding_table']).find_elements_by_tag_name('tr')
        for bidding_row in bidding_rows:
            try:
                details = bidding_row.find_element_by_class_name(selector['bidding-details']['class']).text
                time_ = bidding_row.find_element_by_class_name(selector['bid-time']['class']).text
                price = bidding_row.find_element_by_class_name(selector['bid-price']['class']).text
                bid_qty = bidding_row.find_element_by_class_name(selector['bid-qty']['class']).text
                win_qty = bidding_row.find_element_by_class_name(selector['win-qty']['class']).text
                bid_count+= 1

                cprint(f'          [>>] Bid # {bid_count}', 'cyan', attrs=['bold'])
                cprint(f'              [>>>] Bidder: {details}', 'cyan', attrs=['bold'])
                cprint(f'              [>>>] Bid Time: {time_}', 'cyan', attrs=['bold'])
                cprint(f'              [>>>] Bid Price: {price}', 'cyan', attrs=['bold'])
                cprint(f'              [>>>] Bid Qty: {bid_qty}', 'cyan', attrs=['bold'])
                cprint(f'              [>>>] Win Qty: {win_qty}', 'cyan', attrs=['bold'])
                bidding_details.append({
                    "Bidder": details,
                    "Bidding Time": time_,
                    "Bidding Price": price,
                    "Bid Quantity": bid_qty,
                    "Win Quantity": win_qty
                })
            except:
                cprint(f'          [>>] No Bids Found', 'red', attrs=['bold'])
        try:
            next_page = get_element(selector['bid_next_page'])
            next_page.click()
        except:
            # cprint(f'          [x] Next Page not found.', '', attrs=['bold'])
            break

    DATA[BROWSER.current_url.rsplit("/", 1)[-1]]['bidding_details'] = bidding_details
    DATA[BROWSER.current_url.rsplit("/", 1)[-1]]['auction_details']['Total Bids'] = len(bidding_details)


# details fo auctioned
def get_auction_details(selector, lot_number):
    global DATA
    global INVALID_URL

    try:
        pageExist = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[5]/div[2]/div[3]/div/div[1]/div[1]/div[1]/h1')))
        # print(pageExist.text)
    except:
        pageExist = False

    if pageExist:
        INVALID_URL = 0
        cprint(f'      [>] Fetching Auction Data', 'yellow', attrs=['bold'])
        DATA[BROWSER.current_url.rsplit("/", 1)[-1]] = {
            "url": BROWSER.current_url
        }

        # checking if auction is closed
        has_closed = False
        try:
            get_element(selector["has_closed"])
            has_closed = True
        except:
            pass
        title = get_element(selector["laptop_title"]).text
        closed_on = get_element(selector["lot-closed-on"]).text if has_closed else 'Auction is Live'
        closing_in = 'Closed' if has_closed else get_element(selector["lot-closing-countdown"]).text
        status = 'Closed' if has_closed else 'On Going'
        winning_bid = get_element(selector["current-bid"]).text
        lot_qty = get_element(selector["lot-quantity"]).text
        lot_number = lot_number
        lot_condition = get_element(selector["lot-condition"]).text
        lot_premium = get_element(selector["lot-premium"]).text
        lot_gst = get_element(selector["lot-gst"]).text
        lot_warranty = get_element(selector["lot-warranty"]).text.replace("Warranty:", "").strip()

        dev_sup_li = get_element(selector["lot-details"]).find_elements_by_tag_name("ul")[1].find_elements_by_tag_name("li")
        lot_delivery = dev_sup_li[0].text.replace("Delivery:", "").strip()
        lot_support = dev_sup_li[1].text.replace("Support:", "").strip()

        cprint(f'          [>>] Auction is {"Closed" if has_closed else "Live"}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Title: {title}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] {"Closed On" if has_closed else "Closing In"}: {closed_on if has_closed else closing_in}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Winning Bid: {winning_bid}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Lot Qnty: {lot_qty}', 'cyan', attrs=['bold'])
        # cprint(f'          [>>] Lot Number:  {get_element(selector["lot-number"]).text}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Lot Number:  {lot_number}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Condition: {lot_condition}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Premium: {lot_premium}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] GST: {lot_gst}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Warranty: {lot_warranty}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Delivery: {lot_delivery}', 'cyan', attrs=['bold'])
        cprint(f'          [>>] Support: {lot_support}', 'cyan', attrs=['bold'])

        DATA[BROWSER.current_url.rsplit("/", 1)[-1]]['auction_details'] = {
            "Lot Number": lot_number,
            "Title": title,
            "Status": closed_on,
            "Winning Bid": winning_bid,
            "Quantity": lot_qty,
            "Lot Condition": lot_condition,
            "Lot Premium": lot_premium,
            "Lot GST": lot_gst,
            "Lot Warranty": lot_warranty,
            "Lot Delivery": lot_delivery,
            "Lot Support": lot_support,
        }

        get_autioned_laptop_details(selector)
        get_bidding_details(selector)
    else:
        DATA[lot_number] = "Page dosen\'t exists"
        cprint(f'      [>] Page dosen\'t exists', 'red', attrs=['bold'])
        INVALID_URL += 1


# Saving data to json file
def save_data_JSON(auction):
    file = f'Data/{auction}.json'
    with open(file, 'w') as f:
        json.dump(DATA, f)


# generating auction url using Lot number and auction  number
def generate_auctionUrl(selector, auction, start, end):
    base_url = 'http://www.grays.com/lot'
    for i in range(start, end+1, 1):
        auction_string = f'{i:04}-{auction}'
        url = f'{base_url}/{auction_string}'

        # # for testing purpose
        # url = 'https://www.grays.com/lot/0017-2182381'

        cprint(f'  [+] Fetching data for auction: {auction} and Lot # {i}', 'blue', attrs=['bold'])
        BROWSER.get(url)

        selector = CONFIG_DATA['selectors']
        get_auction_details(selector, auction_string)
        save_data_JSON(auction)

        if INVALID_URL == 5:
            break

        print('\n----------------\n')


# NOT IN USE getting laptops that are on auction
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
        get_auction_details()
        get_autioned_laptop_details()
        get_bidding_details()


# getting required data from website
def get_required_data():
    selector = CONFIG_DATA['selectors']
    for auction in CONFIG_DATA['auction_and_lot_details']:
        generate_auctionUrl(selector, *auction)
    # get_laptop_on_sale()
    # get_heading_section(browser)
    # get_features_section(browser)
    # get_specifications(browser)


# executing script only if its not imported
if __name__ == '__main__':
    try:
        init()
        intro_deco()
        initializer()
        get_browser(headless=False)
        get_required_data()
        BROWSER.quit()
    except Exception as error:
        input("TTTTTTTTTTTTTTTTTTTTTTT")
        if BROWSER:
            BROWSER.quit()
        cprint(f'  [+] EXCEPTION: {str(error)}', 'red', attrs=['bold'])


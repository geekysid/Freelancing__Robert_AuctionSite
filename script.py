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
import pandas as pd
import xlsxwriter, time, json, os, sys


# global variables
DATA = {}
CONFIG_DATA = {}
WAIT_TIME = 5
BROWSER = ''
INVALID_URL = 0
CURRENT_URL = ''


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

        if os.path.exists(f'{os.getcwd()}/selectors.json'):
            with open (f'{os.getcwd()}/selectors.json', 'r') as r:
                CONFIG_DATA['selectors'] = json.load(r)
                return True
        else:
            cprint(f'\n  [X] SELECTOR CONFIG FILE DOSEN\'T EXISTS. TERMINATIING SCRIPT.', 'red', attrs=['bold'])
            return False
    else:
        cprint(f'\n  [X] CONFIG FILE DOSEN\'T EXISTS. TERMINATIING SCRIPT.', 'red', attrs=['bold'])
        return False


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


# details of bidding for the laptop
def get_bidding_details(selector):
    global DATA

    bidding_history = get_element(selector['bidding_history'])
    bidding_history.click()
    bidding_details = []
    bid_count = 0
    while True:
        # time.sleep(1)
        bidding_rows = get_element(selector['bidding_table']).find_elements_by_tag_name('tr')
        if len(bidding_rows) > 0:
            for bidding_row in bidding_rows[1:]:
                try:
                    details = bidding_row.find_element_by_class_name(selector['bidding-details']['class']).text
                    time_ = bidding_row.find_element_by_class_name(selector['bid-time']['class']).text
                    price = bidding_row.find_element_by_class_name(selector['bid-price']['class']).text
                    bid_qty = bidding_row.find_element_by_class_name(selector['bid-qty']['class']).text
                    win_qty = bidding_row.find_element_by_class_name(selector['win-qty']['class']).text
                    bid_count+= 1

                    # cprint(f'          [>>] Bid # {bid_count}', 'cyan', attrs=['bold'])
                    # cprint(f'              [>>>] Bidder: {details}', 'cyan', attrs=['bold'])
                    # cprint(f'              [>>>] Bid Time: {time_}', 'cyan', attrs=['bold'])
                    # cprint(f'              [>>>] Bid Price: {price}', 'cyan', attrs=['bold'])
                    # cprint(f'              [>>>] Bid Qty: {bid_qty}', 'cyan', attrs=['bold'])
                    # cprint(f'              [>>>] Win Qty: {win_qty}', 'cyan', attrs=['bold'])
                    bidding_details.append({
                        "Bid Count": bid_count,
                        "Bidder": details,
                        "Bidding Time": time_,
                        "Bidding Price": price,
                        "Bid Quantity": bid_qty,
                        "Win Quantity": win_qty
                    })
                except Exception as err:
                    # input(str(err))
                    cprint(f'          [>>] No Bids Found', 'red', attrs=['bold'])
            try:
                next_page = get_element(selector['bid_next_page'])
                next_page.click()
            except:
                # cprint(f'          [x] Next Page not found.', '', attrs=['bold'])
                break

    DATA[BROWSER.current_url.rsplit("/", 1)[-1]]['bidding_details'] = bidding_details
    DATA[BROWSER.current_url.rsplit("/", 1)[-1]]['auction_details']['Total Bids'] = len(bidding_details)
    cprint(f'          [>>] Bid Count # {len(bidding_details)}', 'cyan', attrs=['bold'])


# details of lapt that is being auctioned
def get_autioned_laptop_details(selector):
    description = get_element(selector['lot-description']).find_elements_by_tag_name('li')
    laptop_details = {}
    memory = part = processor = storage = None

    for desc in description:
        text = desc.text
        if check_if_substring_exists(CONFIG_DATA['Memory'], text):
            memory = text

        if check_if_substring_exists(CONFIG_DATA['Part'], text):
            part = text.split(': ')[-1]

        if check_if_substring_exists(CONFIG_DATA['Storage'], text):
            processor = text

        if check_if_substring_exists(CONFIG_DATA['Processor'], text):
            storage = text

    cprint(f'          [>>] Memory: {memory}', 'cyan', attrs=['bold'])
    cprint(f'          [>>] Storage: {processor}', 'cyan', attrs=['bold'])
    cprint(f'          [>>] Processor: {storage}', 'cyan', attrs=['bold'])
    cprint(f'          [>>] Part Number: {part}', 'cyan', attrs=['bold'])

    laptop_details['Memory'] = memory
    laptop_details['Part Number'] = part
    laptop_details['Storage'] = processor
    laptop_details['Processor'] = storage

    DATA[BROWSER.current_url.rsplit("/", 1)[-1]]['laptop_details'] = laptop_details


# details fo auctioned
def get_auction_details(selector, lot_number):
    global DATA
    global INVALID_URL

    try:
        pageExist = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, 'lotDetails')))
            # /html/body/div[1]/div[5]/div[2]/div[3]/div/div[1]/div[1]/div[1]/h1'
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
        status = get_element(selector["lot-closed-on"]).text if has_closed else get_element(selector["lot-closing-countdown"]).text
        # status = 'Closed' if has_closed else 'On Going'
        winning_bid = get_element(selector["current-bid"]).text
        lot_qty = get_element(selector["lot-quantity"]).text
        lot_number = lot_number
        lot_condition = get_element(selector["lot-condition"]).text
        lot_premium = get_element(selector["lot-premium"]).text
        lot_gst = get_element(selector["lot-gst"]).text
        lot_warranty = get_element(selector["lot-warranty"]).text.replace("Warranty:", "").strip()

        dev_sup_li = get_element(selector["lot-details"]).find_elements_by_tag_name("ul")[1].find_elements_by_tag_name("li")
        lot_delivery = dev_sup_li[0].text.replace("Deliver to: ", "").strip()
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
            "url": BROWSER.current_url,
            "Status": status,
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


# Writing data to excel
def write_to_excel(worksheet, data_list, item='bid'):

    # Write headers
    col = 0
    for key in data_list[0].keys():
        # if key == 'Item Name':
        #     worksheet.write(0, col, key)
        #     col += 2
        if key == 'url':
            continue
        else:
            worksheet.write(0, col, key)
            col += 1

    # Write list data
    col = 0
    for row, data_dict in enumerate(data_list, start=1):
        col = 0
        for key in data_dict.keys():
            if key == 'Item Name':
                worksheet.write_url(row, col, data_dict['url'], string=data_dict[key])
            elif key == 'url':
                continue
            else:
                worksheet.write(row, col, data_dict[key])
            col += 1


# function that fetches required auction datapoints from json and generates a csv
def generate_auction_file(workbook):
    auction_list = []

    for key in DATA.keys():
        if DATA[key] == "Page dosen't exists":
            continue
        else:
            auction_details = DATA[key]['auction_details'] 
            auction_list.append({
                "Closed": auction_details['Status'],
                "Auction-Lot": f"{auction_details['Lot Number'].split('-')[-1]}-{auction_details['Lot Number'].split('-')[0]}",
                "Auction": auction_details['Lot Number'].split('-')[-1],
                "Lot": auction_details['Lot Number'].split('-')[0],
                "Part": DATA[key]['laptop_details']['Part Number'].split(" ")[0].strip() if CONFIG_DATA['strip_part_number'] else DATA[key]['laptop_details']['Part Number'],
                "Item Name": auction_details['Title'],
                "url": auction_details['url'],
                "Bid": float(auction_details['Winning Bid'].replace("$", "").replace("AU", "").replace(" ", "").replace(",", '').strip()),
                "Condition": auction_details['Lot Condition'],
                "Buyers Premium": auction_details['Lot Premium'],
                "GST": auction_details['Lot GST'],
                "Warranty": auction_details['Lot Warranty'],
                "Deliver To": auction_details['Lot Delivery'],
                "Processor": DATA[key]['laptop_details']['Processor'],
                "Memory": DATA[key]['laptop_details']['Memory'],
                "Storage": DATA[key]['laptop_details']['Storage']
            })
    if len(auction_list) > 0:
        try:
            if CONFIG_DATA['output'] == 'csv':
                pd.DataFrame(auction_list).to_csv(f"{workbook.split('.')[0]}__auctioncsv", index=False)
            elif CONFIG_DATA['output'] == 'excel':
                worksheet = workbook.add_worksheet('Auction Data')
                write_to_excel(worksheet, auction_list, item='auction')
                cprint(f'          ✅ Saved auction data to Excel file', 'green', attrs=['bold'])
                # cprint(f" Current URl = {CURRENT_URL}")
        except Exception as err:
            cprint(f'          ❌ Exception while trying to save auction data into file.', 'red', attrs=['bold'])
            cprint(f'          ❌ Exception: {str(err)}', 'red', attrs=['bold'])


# function that fetches required bidding datapoints from json and generates a csv
def generate_bidding_file(workbook):
    bidding_list = []
    for key in DATA.keys():
        if DATA[key] == "Page dosen't exists":
            continue
        else:
            if DATA[key]['auction_details']['Total Bids'] > 0:

                auction = DATA[key]['auction_details']['Lot Number'].split('-')[-1]
                lot = DATA[key]['auction_details']['Lot Number'].split('-')[0]

                for bid in DATA[key]['bidding_details']:
                    bidding_list.append({
                        "Auction-Lot": f"{DATA[key]['auction_details']['Lot Number'].split('-')[-1]}-{DATA[key]['auction_details']['Lot Number'].split('-')[0]}",
                        "Auction": auction,
                        "Lot": lot,
                        "Bid": bid['Bid Count'],
                        "Bidding Details": bid['Bidder'],
                        "Bid Time": bid['Bidding Time'],
                        "Bid Price": float(bid['Bidding Price'].replace("$", "").replace("AU", "").replace(" ", "").replace(",", "").strip()),
                        "Bid Qty": int(bid['Bid Quantity'].strip()),
                        "Win Qty": int(bid['Win Quantity'].strip())
                    })

    if len(bidding_list) > 0:
        try:
            if CONFIG_DATA['output'] == 'csv':
                pd.DataFrame(bidding_list).to_csv(f"{workbook.split('.')[0]}__bids.csv", index=False)
            elif CONFIG_DATA['output'] == 'excel':
                worksheet = workbook.add_worksheet('Bidding Data')
                write_to_excel(worksheet, bidding_list)
                cprint(f'          ✅ Saved bidding data to Excel file', 'green', attrs=['bold'])
        except Exception as err:
            cprint(f'          ❌ Exception while trying to save bidding data into file.', 'red', attrs=['bold'])
            cprint(f'          ❌ Exception: {str(err)}', 'red', attrs=['bold'])
        # pd.DataFrame(bidding_list).to_excel(file, sheet_name='Bids', index=False)
        # # pd.DataFrame(bidding_list).to_excel(f"{file.split('.')[0]}.xls", sheet_name='Bids', index=False)


# Saving data to json file
def save_data_JSON(file):
    with open(file, 'w') as f:
        json.dump(DATA, f)


# generating auction url using Lot number and auction  number
def generate_auctionUrl(selector, auction, start, end):
    global CURRENT_URL
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
        save_data_JSON(f'Data/{auction}.json')

        workbook = xlsxwriter.Workbook(f'Data/{auction}.xlsx') if CONFIG_DATA['output'].lower()  == 'excel' else None
        file = workbook if CONFIG_DATA['output'].lower() == 'excel' else f'Data/{auction}.json'

        generate_auction_file(file)
        generate_bidding_file(file)

        if CONFIG_DATA['output'].lower() == 'excel':
            workbook.close()

        if INVALID_URL == 5:
            break

        print('\n----------------\n')


# getting required data from website
def get_required_data():
    selector = CONFIG_DATA['selectors']
    for auction in CONFIG_DATA['auction_and_lot_details']:
        generate_auctionUrl(selector, *auction)


# executing script only if its not imported
if __name__ == '__main__':
    try:
        init()
        intro_deco()
        if initializer():
            get_browser(headless=False)
            get_required_data()
            BROWSER.quit()
    except Exception as error:
        # input("TTTTTTTTTTTTTTTTTTTTTTT")
        if BROWSER:
            BROWSER.quit()
        cprint(f'  [+] EXCEPTION: {str(error)}', 'red', attrs=['bold'])

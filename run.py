"""
run argument
base_airport_code, target_airport_code, start_range_day(yyyy-MM-dd), end_range_day(yyyy-MM-dd), cache(JPY)
"""
import time
import datetime
from selenium import webdriver
import sys

BASE_AIRPORT = 'base_airport'
TARGET_AIRPORT = 'target_airport'
BASE_DEPART = 'base_depart'
TARGET_ARRIVAL = 'target_arrival'
BASE_AIRLINE = 'base_airline'
TARGET_AIRLINE = 'target_airline'
PRICE = 'price'

CONST_CHECK_WORD = '時間'
CONST_ADDRESS = 'http://127.0.0.1:9001/input'


def get_date_string(param):
    """
    param : datetime var for make string
    return : parsed string by param(yyyy-MM-dd)
    """
    year = str(param.year)
    month = str(param.month)
    day = str(param.day)

    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day

    res = year + '-' + month + '-' + day

    return res


'''
origin data
    0 - 20:05 発 22:25 着
    1 - アシアナ航空
    2 - 全日空
    6 - ￥58,510
    
    - base_depart       yyyy/MM/dd hh:mm
    - target_arrival    yyyy/MM/dd hh:mm
    - base_airline      string
    - target_airline    string
    - base_airport      string
    - target_airport    string
    - price             string
'''


def send_request_from_crawl_string_data(data_set, base_airport, target_airport, depart_date_param):
    date_info = str(depart_date_param.year) + "/" + str(depart_date_param.month) + "/" + str(depart_date_param.day)
    date_info_pre = date_info + " "

    for i in range(len(data_set)):
        unit_data = {BASE_AIRPORT: base_airport, TARGET_AIRPORT: target_airport}
        row_data = data_set[i].text.split('\n')
        index = 0

        parts = row_data[index].split(' ')
        unit_data[BASE_DEPART] = date_info_pre + parts[0]
        unit_data[TARGET_ARRIVAL] = date_info_pre + parts[2]

        index += 1
        unit_data[BASE_AIRLINE] = row_data[index]

        index += 1
        if CONST_CHECK_WORD in row_data[index]:
            # same airline
            unit_data[TARGET_AIRLINE] = unit_data[BASE_AIRLINE]
        else:
            # different airline
            unit_data[TARGET_AIRLINE] = row_data[index]
            index += 1

        index += 3
        price = row_data[index].replace('￥', '').replace(',', '')
        unit_data[PRICE] = price

        if not send_get_request(CONST_ADDRESS, unit_data):
            print('fail to update', unit_data[BASE_AIRLINE], unit_data[TARGET_AIRLINE])


def send_get_request(address, param):
    import requests
    r = requests.get(url=address, params=param)
    status = r.status_code
    if status == 200 or status == 204:
        return True
    else:
        return False


# if args are not valid, stop with code 1
arg = sys.argv
if len(arg) != 6:
    sys.exit(1)

# set argument to python var
base_airport_code = arg[1]
target_airport_code = arg[2]
range_start_day = arg[3]
range_end_day = arg[4]
cache = arg[5]

# chrome driver path
path = "./chromeDriver_v63_mac64"
driver = webdriver.Chrome(path)

# base url for google flight search
base_url = "https://www.google.com/flights#flt="

# make array for make datetime var
range_start_elements = range_start_day.split('-')
range_end_elements = range_end_day.split('-')

# make datetime vars for 2 while loop
depart_date = datetime.datetime(int(range_start_elements[0]), int(range_start_elements[1]), int(range_start_elements[2]))
end_range_date = datetime.datetime(int(range_end_elements[0]), int(range_end_elements[1]), int(range_end_elements[2]))
end_range_date_plus_day = end_range_date + datetime.timedelta(days=1)

while depart_date != end_range_date:
    arrival_date = depart_date + datetime.timedelta(days=1)
    while arrival_date != end_range_date_plus_day:

        search_url = base_url
        search_url += base_airport_code + "." + target_airport_code + "."
        search_url += get_date_string(depart_date) + "*" + target_airport_code + "." + base_airport_code + "."
        search_url += get_date_string(arrival_date) + ";c:" + cache + ";e:1;sd:1;t:f"

        driver.get(search_url)
        time.sleep(0.5)
        try:
            best_big_container = driver.find_element_by_class_name("gws-flights-results__best-flights")
            best_container = best_big_container.find_element_by_class_name("gws-flights-results__result-list")

            results = best_container.find_elements_by_class_name("gws-flights-results__collapsed-itinerary")

            send_request_from_crawl_string_data(results, base_airport_code, target_airport_code, depart_date)

        except:
            # if it has exception, skip it
            print("fail at", depart_date, arrival_date, base_airport_code, target_airport_code)

        arrival_date = arrival_date + datetime.timedelta(days=1)
    depart_date = depart_date + datetime.timedelta(days=1)
driver.close()
print("done")

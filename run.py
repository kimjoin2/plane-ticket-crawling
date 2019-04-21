"""
argument
base_airport_code, target_airport_code, start_range_day(yyyy-MM-dd), end_range_day(yyyy-MM-dd), cache(JPY)
"""
import time
import datetime
from selenium import webdriver
import sys


def get_date_string(param):
    year = str(param.year)
    month = str(param.month)
    day = str(param.day)

    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day

    res = year + '-' + month + '-' + day

    return res


arg = sys.argv
if len(arg) != 6:
    sys.exit(1)

base_airport_code = arg[1]
target_airport_code = arg[2]
range_start_day = arg[3]
range_end_day = arg[4]
cache = arg[5]

path = "./chromeDriver_v63_mac64"
driver = webdriver.Chrome(path)

base_url = "https://www.google.com/flights#flt="

range_start_elements = range_start_day.split('-')
range_end_elements = range_end_day.split('-')

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
        time.sleep(3)
        try:
            best_big_container = driver.find_element_by_class_name("gws-flights-results__best-flights")
            best_container = best_big_container.find_element_by_class_name("gws-flights-results__result-list")
            print(best_container.text)
        except:
            print("fail at", depart_date, arrival_date, base_airport_code, target_airport_code)

        arrival_date = arrival_date + datetime.timedelta(days=1)
    depart_date = depart_date + datetime.timedelta(days=1)


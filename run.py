import time
from selenium import webdriver

search_url = "https://www.google.com/flights#flt=HND.GMP.2019-05-07*GMP.HND.2019-05-11;c:JPY;e:1;sd:1;t:f"

path = "chromeDriver_v63_mac64"
driver = webdriver.Chrome(path)
driver.get(search_url)
time.sleep(3)
best_container = driver.find_element_by_class_name("gws-flights-results__best-flights")

print(type(best_container.text))

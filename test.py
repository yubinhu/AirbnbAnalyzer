from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import time
import random


session = HTMLSession()

url = 'https://www.airbnb.com/rooms/23568964?adults=1&check_in=2022-01-21&check_out=2022-01-23&federated_search_id=bd9cd37f-2168-45a3-a4f3-3a9c0a6c7186&source_impression_id=p3_1642317877_xAVnfw1s%2FpSRgxYt&guests=1'

def get_price():
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    h = r.html.html
    result = re.findall(r'>\$(\d+)</span><', h)
    price = (int(result[0])) if result else None
    return price

price = None
ctr = 0
while not price and ctr < 10:
    price = get_price()
    ctr += 1
    print(ctr)
    time.sleep(random.randint(1,5))

print(price, ctr)
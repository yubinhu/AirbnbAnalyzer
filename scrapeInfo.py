from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import re
import time
import random
from datetime import datetime


class PlaceToLive:

    def __init__(self, url):
        try:
            r = session.get(url)
            r.html.render(sleep=1, keep_page=True, scrolldown=1)
            H = r.html
            h = r.html.html
        except:
            H = None
            h = None
        self.HTML = H
        self.html = h

    def get_price(self):
        if not self.html:
            result = re.findall(r'>\$(\d+)</span><', self.html)
            self.price = (int(result[0])) if result else None
        else:
            self.price = None
    
    def get_review(self):
        if not self.html:
            result = re.findall(r'Rated (\d\.\d+) out of 5 from (\d+) reviews.')
            self.rate = result[0]
            self.num_reviews = result[1]
        else:
            self.rate = None
            self.num_reviews = None

    def get_dates(self):
        # get object specifying dates that are available
        available_dates_classes = self.HTML.find('[data-is-day-blocked=false]')
        # get dates in mm/dd/yy format
        available_dates = [d.search('data-testid=\"calendar-day-{}"')[0] for d in available_dates_classes]
        # reformat dates to "January 8, 2022" like format        
        reformated_available_dates = [datetime.strftime(datetime.strptime(d, '%m/%d/%Y'), '%B %d, %Y').replace(' 0', ' ') for d in available_dates]
        # find the objects that specify whether these dates are unavailable, available for check out only, or available for check in
        classes = [r.html.find('[aria-label*="'+d+'"]',first=True) for d in reformated_available_dates]
        checkin_available_dates = []
        checkin_unavailable_dates = []
        for i in range(len(available_dates)):
            print(i, classes[i])
            if classes[i].find('[aria-label*="check out"]'):
                checkin_unavailable_dates.append(available_dates[i])
            else:
                checkin_available_dates.append(available_dates[i])
        self.checkin_unavailable_dates = checkin_unavailable_dates
        self.checkin_available_dates = checkin_available_dates

session = HTMLSession()

url = 'https://www.airbnb.com/rooms/52553164'

'''
p = PlaceToLive(url)

h = None

def get_price():
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    global h
    h = r.html.html
    result = re.findall(r'>\$(\d+)</span><', h)
    price = (int(result[0])) if result else None
    return price

price = None
ctr = 0
while not price and ctr<10:
    price = get_price()
    ctr += 1
    time.sleep(random.randint(1,5))

print(price, ctr)
print(h)
'''

r = session.get(url)
r.html.render(sleep=1, keep_page=True, scrolldown=10)
h = r.html.html
available_dates_classes = r.html.find('[data-is-day-blocked=false]')
available_dates = [d.search('data-testid=\"calendar-day-{}"')[0] for d in available_dates_classes]
print(available_dates)
reformated_available_dates = [datetime.strftime(datetime.strptime(d, '%m/%d/%Y'), '%B %d, %Y').replace(' 0', ' ') for d in available_dates]
print(reformated_available_dates)
print(['[aria-label*="'+d+'"]' for d in reformated_available_dates])
classes = [r.html.find('[aria-label*="'+d+'"]',first=True) for d in reformated_available_dates]
print(classes)
checkin_available_dates = []
checkin_unavailable_dates = []
for i in range(len(available_dates)):
    print(i, classes[i])
    if classes[i].find('[aria-label*="check out"]'):
        checkin_unavailable_dates.append(available_dates[i])
    else:
        checkin_available_dates.append(available_dates[i])

print(checkin_available_dates)
print(checkin_unavailable_dates)



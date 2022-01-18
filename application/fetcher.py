from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import re
import time
import random
from datetime import datetime


class PlaceToLive:

    def __init__(self, url, session):
        self.url = url
        self.HTML = None
        self.html = None
        self.price = None
        self.rate = None
        self.num_reviews = None
        self.checkin_unavailable_dates = None
        self.checkin_available_dates = None
        self.session = session
    
    def get_html(self):
        try:
            r = self.session.get(url)
            r.html.render(sleep=1, keep_page=True, scrolldown=10)
            H = r.html
            h = r.html.html
        except:
            H = None
            h = None
        self.HTML = H
        self.html = h

    def get_price(self):
        if self.html is not None:
            result = re.search(r'>\$(\d+)</span><', self.html).group(1)
            self.price = (int(result)) if result else None
    
    def get_review(self):
        if self.html is not None:
            result = re.search(r'Rated (\d\.\d+) out of 5 from (\d+) reviews.', self.html)
            self.rate = result.group(1)
            self.num_reviews = result.group(2)

    def get_dates(self):
        # get object specifying dates that are available
        available_dates_classes = self.HTML.find('[data-is-day-blocked=false]')
        # get dates in mm/dd/yy format
        available_dates = [d.search('data-testid=\"calendar-day-{}"')[0] for d in available_dates_classes]
        # reformat dates to "January 8, 2022" like format        
        reformated_available_dates = [datetime.strftime(datetime.strptime(d, '%m/%d/%Y'), '%B %d, %Y').replace(' 0', ' ') for d in available_dates]
        # find the objects that specify whether these dates are unavailable, available for check out only, or available for check in
        classes = [self.HTML.find('[aria-label*="'+d+'"]',first=True) for d in reformated_available_dates]
        checkin_available_dates = []
        checkin_unavailable_dates = []
        for i in range(len(available_dates)):
            if classes[i].find('[aria-label*="check out"]'):
                checkin_unavailable_dates.append(available_dates[i])
            else:
                checkin_available_dates.append(available_dates[i])
        self.checkin_unavailable_dates = checkin_unavailable_dates
        self.checkin_available_dates = checkin_available_dates

    def getAllInfo(self):

        if self.HTML is None or self.html is None:
            self.get_html()

        if self.price is None:
            self.get_price()

        if self.rate is None or self.num_reviews is None:
            self.get_review()
        
        if self.checkin_available_dates is None or self.checkin_unavailable_dates is None:
            self.get_dates()
        
    def printAllInfo(self):

        print('Price Per Night: $', self.price)
        print('Rated {rate} out of 5 by {num_reviews} reviews'.format(rate = self.rate, num_reviews = self.num_reviews))
        print('These upcoming dates are available for check-in:\n', self.checkin_available_dates)
        print('These upcoming dates are only available for check out:\n', self.checkin_unavailable_dates)

if __name__ == "__main__":
    start = time.time()

    session = HTMLSession()

    url = 'https://www.airbnb.com/rooms/52553164'

    currAirBnB = PlaceToLive(url, session)
    currAirBnB.getAllInfo()
    currAirBnB.printAllInfo()

    end = time.time()          
    print('Time Elapsed: ', round(end-start, 3), 's')







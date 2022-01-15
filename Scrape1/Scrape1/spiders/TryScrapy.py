import scrapy

class MySpider(scrapy.Spider):
    name = "TestName"
    start_urls = [
        'https://www.zyte.com/blog/scrapinghub-is-now-zyte/'
    ]
    
    def parse(self, response):
        page = 1
        filename = 'Site1.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

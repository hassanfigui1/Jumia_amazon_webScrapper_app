import scrapy
from scrapy.crawler import CrawlerProcess
import json

class Amazon(scrapy.Spider):
    name = "Amazon"
    def start_requests(self):
        with open('data.json', 'w') as f:
            f.write(' ')
        settings = ''
        with open('settings.json', 'r') as f:
            for line in f.read():
                settings += line
        settings.replace(" ","+")
        settings = json.loads(settings)
        yield scrapy.Request('https://www.amazon.com/s?k='+settings['category'].replace(' ','+'), callback=self.profile)
            

    def profile(self, response):
        item = {}
        item['title'] = response.css('.a-size-medium.a-text-normal::text').get()
        item['prix'] = response.css(".a-offscreen::text").get()
        item['url'] = "https://www.amazon.com/"
        item['url'] += response.css(".a-text-normal").xpath("@href").get()
        item['img_url'] = response.css(".s-image").xpath("@src").get()
        
        with open('data.json', 'a') as f:
            f.write(json.dumps(item, indent=4) + '\n')

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Amazon)
    process.start()  
        

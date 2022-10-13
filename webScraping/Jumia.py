import scrapy

from scrapy.crawler import CrawlerProcess

import json

class Jumia(scrapy.Spider):
    name = "Jumia"
    def start_requests(self):
        # with open('data.json', 'w') as f:
        #     f.write(' ')
        settings = ''
        with open('settings.json', 'r') as f:
            for line in f.read():
                settings += line
        settings.replace(" ","+")
        settings = json.loads(settings)
        print('hassan','https://www.jumia.ma/catalog/?q='+settings['category'])
        yield scrapy.Request('https://www.jumia.ma/catalog/?q='+settings['category'], callback=self.profile)
            

    def profile(self, response):
        item = {}
        item['title'] = response.css('.info .name::text').get()
        item['title'].replace("NaN"," ")
        item['prix'] = response.css('.prc::text').get()
        item['url'] = "https://www.jumia.ma/"
        item['url'] += response.css(".core").xpath("@href").get()
        item['img_url'] = response.css(".img").xpath("@data-src").get()
        # item["url"] =response.css("a.s-item__link").xpath("@href").get()
        with open('data.json', 'a') as f:
            f.write(json.dumps(item, indent=2) + '\n')

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Jumia)
    process.start()       
import string
import scrapy
from scrapy import Request
from scrapy.utils.markup import remove_tags

BASE_URL = 'https://theconversation.com/'

class TheConversationSpider(scrapy.Spider):
    name = "TheConversation"
    start_urls = ['https://theconversation.com/au/topics/climate-change-27']


    def parse(self, response):
        xp = "//div[@class='article--header']//h2/a/@href"


        urls = response.xpath(xp).extract()

        for url in urls:
            print(url)
            yield Request(BASE_URL+url, callback = self.parse_list_page)

        #urls = response.xpath(xp).extract() #stored all links in one page

        next_urls = response.xpath("//span[@class='next']//a/@href").extract()
        print(next_urls)

        if next_urls:
            yield Request(BASE_URL+next_urls[0], callback=self.parse)
    #     return (Request(response.urljoin(url), callback=self.parse_list_page) for url in response.xpath(xp).extract())


    def parse_list_page(self, response):
        para = ""
        for sub_block in response.css('div.content-body'):
            for p in sub_block.xpath('.//p'):
                para += remove_tags(p.get().strip())
        yield {
                     "article":  para,
                 }

    #     next_urls = response.xpath("//span[@class='next']//a/@href").extract()
    #     for next_url in next_urls:
    #         yield Request(response.urljoin(next_url), callback=self.parse_list_page)
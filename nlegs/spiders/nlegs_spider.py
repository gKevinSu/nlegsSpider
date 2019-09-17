import scrapy
from nlegs.items import NlegsItem

class NlegsSpider(scrapy.Spider):
    name = "nlegs"
    start_urls=["http://www.nlegs.com/more.html"]

    def parse(self, response):

        model = getattr(self, 'model', None)
        months = int(getattr(self, 'months', 6))
        if model is None:
            return
        level = len(response.xpath("//ul[@class='breadcrumb']//li").extract())
        if level==0:
            for index in response.xpath("//div[@class='col-md-2 col-lg-2']//@href").extract()[:months]:
                index = response.urljoin(index)
                yield scrapy.Request(index, self.parse)
        elif level==3:
            for article in response.xpath('//a[contains(text(),"%s")]' % model):
                title = article.xpath('text()').extract_first()
                url = article.xpath('@href').extract_first()
                url = response.urljoin(url)
                yield scrapy.Request(url, self.parse)
        elif level==4:
            for image in response.xpath("//a[contains(@href,'jpg')]//@href").extract():
                image = response.urljoin(image)
                title = response.css("title::text").extract_first()
                title = title.replace(" | www.nlegs.com\r\n", "")
                title = title.replace("\r\n\t", "")
                item = NlegsItem()
                item['model'] = model
                item['title'] = title
                item['url'] = image
                yield item
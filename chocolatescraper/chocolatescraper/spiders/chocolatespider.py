import scrapy
from chocolatescraper.items import ChocolatescraperItem
from chocolatescraper.itemloaders import ChocolateProductLoader


class ChocolatespiderSpider(scrapy.Spider):
    name = 'chocolatespider'
    allowed_domains = ['chocolate.co.uk']
    start_urls = ['https://www.chocolate.co.uk/collections/all']

    def parse(self, response):
        
     products = response.css('product-item')

     for product in products:
         
         #populate item pipeline + item loader for data cleasing
         chocolate = ChocolateProductLoader(ChocolatescraperItem(), seletor= product),
         chocolate.add_css('title', 'a.product-item-meta__title::text').get(),
         chocolate.add_css('price', 'span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>',''),
         chocolate.add_csss('url', 'div.product-item-meta a').attrib['href']
         yield chocolate.load_item()
        
     next_page = response.css('[rel="next"] ::attr(href)').get()
     if next_page is not None:
        next_page_url = 'https://www.chocolate.co.uk' + next_page
        yield response.follow(next_page_url, callback=self.parse)

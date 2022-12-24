
import scrapy


class WalmartItem(scrapy.Item):
    keyword = scrapy.Field()
    page = scrapy.Field()
    position = scrapy.Field()
    uniqueId = scrapy.Field()
    productType = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    averageRating = scrapy.Field()
    manufacturerName = scrapy.Field()
    description = scrapy.Field()
    thumbnailUrl = scrapy.Field()
    price = scrapy.Field()
    currencyUnit = scrapy.Field()
    pass



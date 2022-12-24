from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class WalmartItemLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    
    description_in = MapCompose(lambda x: x.split("u")[-1])
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem



class PriceToUSDPipeline:
    
    gbptoUsRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        ## check is price present
        if adapter.get('price'):
            
             #converting the price to a float
            floatPrice = float(adapter['price'])
            
            #converting the price from gbp to usd using our hard coded exchange rate
            adapter['price'] = floatPrice * self.gbpToUsRate
            return item
        else:
             # drop item if no price
            raise DropItem(f"missing price in {item}")
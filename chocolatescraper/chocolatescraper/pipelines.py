from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

## Storing to DB
import psycopg2 ## Postgres

class SavingToPostgresPipeline(object):
    
    def __init__(self):
        self.create_connection()


    def create_connection(self):
        self.connection = psycopg2.connect(
            host="",
            database="postgres",
            user="postgres",
            password="")
        
        self.curr = self.connection.cursor()
        
    def close_spider(self, spider):
        self.curr.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.store_db(item)
        #we need to return the item below as scrapy expects us to!
        return item
        

    def store_db(self, item):
        try:
           self.curr.execute("insert into chocolate_products (name, price, url) values(%s,%s,%s)", (
            item["name"],
            str(item["price"]),
            item["url"]
        ))
           self.connection.commit()
        except:
              self.connection.rollback()
              raise
        return item
        
    

        

class PriceToUSDPipeline:

    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):

            #converting the price to a float
            floatPrice = float(adapter['price'])

            #converting the price from gbp to usd using our hard coded exchange rate
            adapter['price'] = floatPrice * self.gbpToUsdRate

            return item
        else:
            raise DropItem(f"Missing price in {item}")


class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item


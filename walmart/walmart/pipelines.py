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
           self.curr.execute("insert into walmart_products (keyword, page, position, uniqueId, productType, name, brand, averageRating, manufacturerName,  description, thumbnailUrl, price, currencyUnit) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
            item["keyword"],
            str(item["page"]),
            str(item["position"]),
            str(item["uniqueId"]),
            item["productType"],
            item["name"], 
            item["brand"], 
            item["averageRating"],
            item["manufacturerName"],
            item["description"],
            item["thumbnailUrl"], 
            str(item["price"]),
            item["currencyUnit"]
        ))
           self.connection.commit()
        except:
              self.connection.rollback()
              raise
        return item
        

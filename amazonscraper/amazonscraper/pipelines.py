
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
           self.curr.execute("insert into amazon_products (name, price, stars, rating_count, feature_bullets, images, variant_data) values(%s,%s,%s,%s,%s,%s,%s)", (
            item["name"],
            str(item["price"]),
            item["stars"],
            item['rating_count'],
            str(item['feature_bullets']),
            str(item['images']), 
            str(item['variant_data'])
        ))
           self.connection.commit()
        except:
              self.connection.rollback()
              raise
        return item
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    #       CREATE TABLE IF NOT EXISTS amazon_products (
    # id SERIAL PRIMARY KEY,
    # name VARCHAR(255),
    # price VARCHAR(255),
    # stars VARCHAR(255),
    # rating_count VARCHAR(255),
    # feature_bullets VARCHAR(255),
    # images VARCHAR(255),
    # variant_data VARCHAR(255)
    # );

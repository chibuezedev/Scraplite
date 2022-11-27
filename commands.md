 Part 1: Building the basic scraping functionality.

- Get the targeted website >> fetch('https://www.chocolate.co.uk/collections/all')
- Check if it was successfull >> response
- Get a targeted div of product is { >> products = response.css('product-item')}
- Get first product-item >> response.css('product-item').get()
- Get the lenght of the returned product >> len(products)
- Get the price of the product from a span >> product.css('span.price').get().replace('<span class="price">\n     <span class="visually-hidden">Sale price</span>','').replace('</span>','')

- Note: this is used when we have a html objects returns from a request instead of the data due to its nested nature.

- pagination  >> response.css('[rel="next"] ::attr(href)').get().


 Part 2: Cleaning Dirty Data & Dealing With Edge Cases

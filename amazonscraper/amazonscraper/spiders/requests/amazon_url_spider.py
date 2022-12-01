import requests
from parsel import Selector
from urllib.parse import urljoin

product_urls = []

keyword_list = ['ipad']

for keyword in keyword_list:
    url_list = [f'https://www.amazon.com/s?k={keyword}&page=1']
    for url in url_list:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                sel = Selector(text=response.text)

                ## Extract Product Page URLs
                search_products = sel.css("div.s-result-item[data-component-type=s-search-result]")
                for product in search_products:
                    relative_url = product.css("h2>a::attr(href)").get()
                    product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
                    product_urls.append(product_url)

                    ## Get All Pages
                if "&page=1" in url:
                    available_pages = sel.xpath(
                        '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
                    ).getall()

                    for page in available_pages:
                        search_url_paginated = f'https://www.amazon.com/s?k={keyword}&page={page}'
                        url_list.append(search_url_paginated)

        except Exception as e:
            print("Error", e)

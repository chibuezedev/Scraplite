import requests
from parsel import Selector
from urllib.parse import urlencode, urljoin

API_KEY = '2bdeae7a-75d6-4dc4-a726-bfbff5c29bed'


def scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country': 'us'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


keyword_list = ['ipad']
product_overview_data = []

for keyword in keyword_list:
    url_list = [f'https://www.amazon.com/s?k={keyword}&page=1']
    for url in url_list:
        try:
            response = requests.get(scrapeops_url(url))

            if response.status_code == 200:
                sel = Selector(text=response.text)

                ## Extract Product Data From Search Page
                search_products = sel.css("div.s-result-item[data-component-type=s-search-result]")
                for product in search_products:
                    relative_url = product.css("h2>a::attr(href)").get()
                    asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
                    product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
                    product_overview_data.append(
                        {
                            "keyword": keyword,
                            "asin": asin,
                            "url": product_url,
                            "ad": True if "/slredirect/" in product_url else False,
                            "title": product.css("h2>a>span::text").get(),
                            "price": product.css(".a-price[data-a-size=xl] .a-offscreen::text").get(),
                            "real_price": product.css(".a-price[data-a-size=b] .a-offscreen::text").get(),
                            "rating": (product.css("span[aria-label~=stars]::attr(aria-label)").re(
                                r"(\d+\.*\d*) out") or [None])[0],
                            "rating_count": product.css("span[aria-label~=stars] + span::attr(aria-label)").get(),
                            "thumbnail_url": product.xpath("//img[has-class('s-image')]/@src").get(),
                        }
                    )

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

print(product_overview_data)

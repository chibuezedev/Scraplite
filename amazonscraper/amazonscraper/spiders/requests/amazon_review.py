import requests
from parsel import Selector
from urllib.parse import urljoin

reviews = []

product_review_url_list = ['https://www.amazon.com/product-reviews/B09G9FPHY6/']

for product_review_url in product_review_url_list:
    try:
        response = requests.get(product_review_url)

        if response.status_code == 200:
            sel = Selector(text=response.text)

            ## Get Next Page Url
            next_page_relative_url = sel.css(".a-pagination .a-last>a::attr(href)").get()
            if next_page_relative_url is not None:
                next_page = urljoin('https://www.amazon.com/', next_page_relative_url)
                product_review_url_list.append(next_page)

            ## Parse Product Reviews
            review_elements = sel.css("#cm_cr-review_list div.review")
            for review_element in review_elements:
                reviews.append({
                    "text": "".join(review_element.css("span[data-hook=review-body] ::text").getall()).strip(),
                    "title": review_element.css("*[data-hook=review-title]>span::text").get(),
                    "location_and_date": review_element.css("span[data-hook=review-date] ::text").get(),
                    "verified": bool(review_element.css("span[data-hook=avp-badge] ::text").get()),
                    "rating": review_element.css("*[data-hook*=review-star-rating] ::text").re(r"(\d+\.*\d*) out")[0],
                })

    except Exception as e:
        print("Error", e)
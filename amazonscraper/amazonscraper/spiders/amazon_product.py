import re
import requests
from parsel import Selector
from urllib.parse import urljoin

product_urls = [
    'https://www.amazon.com/2021-Apple-10-2-inch-iPad-Wi-Fi/dp/B09G9FPHY6/ref=sr_1_1',
]

product_data_list = []

for product_url in product_urls:
    try:
        response = requests.get(product_url)

        if response.status_code == 200:
            sel = Selector(text=response.text)
            image_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0])
            variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
            feature_bullets = [bullet.strip() for bullet in sel.css("#feature-bullets li ::text").getall()]
            price = sel.css('.a-price span[aria-hidden="true"] ::text').get("")
            if not price:
                price = sel.css('.a-price .a-offscreen ::text').get("")
            product_data_list.append({
                "name": sel.css("#productTitle::text").get("").strip(),
                "price": price,
                "stars": sel.css("i[data-hook=average-star-rating] ::text").get("").strip(),
                "rating_count": sel.css("div[data-hook=total-review-count] ::text").get("").strip(),
                "feature_bullets": feature_bullets,
                "images": image_data,
                "variant_data": variant_data,
            })
    except Exception as e:
        print("Error", e)

# Scraplite

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This advanced web scraper is designed for production-scale data extraction. It utilizes the Scrapy framework and is automated using AWS and Celery.

## Features

- Scalable data extraction using Scrapy framework
- Automated task scheduling with Celery
- Distributed computing using AWS infrastructure
- Support for handling JavaScript-rendered websites
- Customizable scraping pipelines for data processing and storage

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/chibuezedev/Scraprite.git
   ```

2. Install the dependencies using pip:

   ```shell
   cd advanced-web-scraper
   pip install -r requirements.txt
   ```

3. Configure the AWS credentials in `settings.py`:

   ```python
   AWS_ACCESS_KEY_ID = '<your-access-key-id>'
   AWS_SECRET_ACCESS_KEY = '<your-secret-access-key>'
   ```

4. Set up the Celery task broker and result backend in `settings.py`:

   ```python
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   ```

5. Start the Celery worker:

   ```shell
   celery -A scraper worker --loglevel=info
   ```

## Usage

1. Create a new spider by defining the scraping rules in `spiders/my_spider.py`. You can refer to the [Scrapy documentation](https://docs.scrapy.org/en/latest/topics/spiders.html) for more information on defining spiders.

2. Customize the data processing and storage pipelines in `pipelines.py` according to your requirements.

3. Run the scraper using the following command:

   ```shell
   scrapy crawl my_spider
   ```

   Replace `my_spider` with the name of your spider.

4. To schedule tasks automatically, use Celery's task scheduling mechanism. Refer to the [Celery documentation](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html) for more information on scheduling tasks.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request. Please make sure to follow the code of conduct.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

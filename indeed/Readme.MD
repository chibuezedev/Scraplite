# indeed-python-scrapy-scraper
Python Scrapy spider that scrapes Jobs data from [Indeed.com](https://www.indeed.com/). There are two versions:

1. **Scrapes Job Summary Data:** The scraper will query the Indeed search page with your query parameters and extract the job data directly from the search results.
2. **Scrapes Full Job Data:** The scraper will crawl the Indeed search pages with your query parameters, then send a request to each individual job page and scrape all the job data from the page.

Both of these scrapers only scrape some of the available data, however, you can easily expand them to scrape other data that is available in the response.

These scrapers extract the following fields from Indeed jobs pages:

- Company Name
- Company Location
- Job Title
- Job Description
- Job Salary
- Job Location
- Etc.


## Running The Scrapers
Make sure Scrapy and the ScrapeOps Monitor is installed:

```

pip install scrapy scrapeops-scrapy

```

To run the Indeed spiders you should first set the Job query parameters you want to search by updating the `keyword_list` and `location_list` lists in the spiders:

```python

def start_requests(self):
    keyword_list = ['software engineer']
    location_list = ['California']
    for keyword in keyword_list:
        for location in location_list:
            indeed_jobs_url = self.get_indeed_search_url(keyword, location)
            yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results, meta={'keyword': keyword, 'location': location, 'offset': 0})

```

Then to run the spiders, enter one of the following commands:

| Spider  |      Command      |
|----------|-------------|
| **Job Summary Data** |  `scrapy crawl indeed_search` | 
| **Full Job Data** |  `scrapy crawl indeed_jobs` | 



### Configuring Job Search
To change the query parameters for the job search just change the keywords and locations in the `keyword_list` and `location_list` lists in each spider.

For example:

```python

def start_requests(self):
    keyword_list = ['software engineer', 'devops engineer', 'product manager']
    location_list = ['California', 'texas']
    for keyword in keyword_list:
        for location in location_list:
            indeed_jobs_url = self.get_indeed_search_url(keyword, location)
            yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results, meta={'keyword': keyword, 'location': location, 'offset': 0})

```

### Extract More/Different Data
The JSON blobs the spiders extract the job data from are pretty big so the spiders are configured to only parse some of the data. 

You can expand or change the data that gets extract by changing the yield statements:

```python

yield {
        'keyword': keyword,
        'location': location,
        'page': round(offset / 10) + 1 if offset > 0 else 1,
        'position': index,
        'company': job.get('company'),
        'companyRating': job.get('companyRating'),
        'companyReviewCount': job.get('companyReviewCount'),
        'companyRating': job.get('companyRating'),
        'highlyRatedEmployer': job.get('highlyRatedEmployer'),
        'jobkey': job.get('jobkey'),
        'jobTitle': job.get('title'),
        'jobLocationCity': job.get('jobLocationCity'),
        'jobLocationPostal': job.get('jobLocationPostal'),
        'jobLocationState': job.get('jobLocationState'),
        'maxSalary': job.get('estimatedSalary').get('max') if job.get('estimatedSalary') is not None else 0,
        'minSalary': job.get('estimatedSalary').get('min') if job.get('estimatedSalary') is not None else 0,
        'salaryType': job.get('estimatedSalary').get('max') if job.get('estimatedSalary') is not None else 'none',
        'pubDate': job.get('pubDate'),
    }

```

### Speeding Up The Crawl
The spiders are set to only use 1 concurrent thread in the settings.py file as the ScrapeOps Free Proxy Plan only gives you 1 concurrent thread.

However, if you upgrade to a paid ScrapeOps Proxy plan you will have more concurrent threads. Then you can increase the concurrency limit in your scraper by updating the `CONCURRENT_REQUESTS` value in your ``settings.py`` file.

```python
# settings.py

CONCURRENT_REQUESTS = 10

```

### Storing Data
The spiders are set to save the scraped data into a CSV file and store it in a data folder using [Scrapy's Feed Export functionality](https://docs.scrapy.org/en/latest/topics/feed-exports.html).

```python

custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

```
```python
# settings.py

# ## Enable ScrapeOps Proxy
# SCRAPEOPS_PROXY_ENABLED = True

# # Add In The ScrapeOps Monitoring Extension
# EXTENSIONS = {
# 'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
# }


# DOWNLOADER_MIDDLEWARES = {

#     ## ScrapeOps Monitor
#     'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
#     ## Proxy Middleware
#     'indeed.middlewares.ScrapeOpsProxyMiddleware': 725,
# }

```

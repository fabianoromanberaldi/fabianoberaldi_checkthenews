# Check the news in NY Times site
## Web Scrapper

### Configurations
* File: Configuration.py
* Attributes:
  *  timezone: set the timezone of the log file, such as "America/Sao_Paulo", "US/Central" for example
  *  filter_text: search phrase
  *  month: number of months for which you need to receive news (if 0, means current month)
  *  timeout_in_seconds: selenium timeout
  *  browser: browser where you want to run the robot. The values must be "chrome", "firefox" or "edge"
  *  download_images: if you want to download the images from the article, set as True, otherwise False

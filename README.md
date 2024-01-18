# Check the news in NY Times site
## Web Scrapper

### Configurations
* File: env.json
* Attributes:
  *  timezone: set the timezone of the log file, such as "America/Sao_Paulo", "US/Central" for example
  *  search phrase: search phrase
  *  month: number of months for which you need to receive news (if 0, means current month)
  *  timeout_in_seconds: selenium timeout
  *  browser: browser where you want to run the robot. The values must be "chrome", "firefox", "edge", "headlesschrome" or "headlessfirefox"
  *  auto_close: if set as 'true' the browser will be closed after the execution, otherwise the browser keeps opened
  *  download_images: if you want to download the images from the article, set as 'true', otherwise as 'false'
  *  attempts: number of attempts
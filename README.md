# Check the news in NY Times site

## Web Scrapper

### Configurations

* Parameters:
  * SEARCH_PHRASE (string): search phrase
  * MONTHS (integer): number of months for which you need to receive news (if 0, means current month)
  * TIMEOUT_IN_SECONDS (integer): selenium timeout
  * BROWSER (string): browser where you want to run the robot. The values must be "chrome", "firefox", "edge", "headlesschrome" or "headlessfirefox"
  * AUTO_CLOSE (bool): if set as 'true' the browser will be closed after the execution, otherwise the browser keeps opened
  * DOWNLOAD_IMAGES (bool): if you want to download the images from the article, set as 'true', otherwise as 'false'
  * ATTEMPTS (integer): number of attempts
  * WORKBOOK_PATH (string): folder path where the workbook (Excel spreadsheet) will be stored
  * SHEET_NAME (string): sheet name where the data is inserted
  * SHEET_COLUMNS (string): name of the columns (list)
  
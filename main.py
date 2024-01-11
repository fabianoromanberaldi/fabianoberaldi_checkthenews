
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import wget
from pytz import timezone

from configurations import Configuration
from nwt_search import NewYorkTimesScraper

config = Configuration()

# create log file
print("TIMEZONE: ", config.timezone)
tz_central = timezone(config.timezone)
dt_now = datetime.now(tz_central)
formated_date = dt_now.strftime("%Y%m%d")

log_file = "automation_log.txt"
log_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'

logging.basicConfig(
    filename=log_file,
    format=log_format
    )

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.basicConfig(filename=log_file)


def run_script():
    logger.info("Running script")
    obj_nwt = NewYorkTimesScraper(
        timeout=config.timeout_in_seconds
    )
    
    list_location = "//ol[@data-testid='search-results']"
    list_items_location = "//li[@data-testid='search-bodega-result']"

    reject_all_button_location = "//button[@data-testid='Reject all-btn']"
    show_more_button_location = "//button[@data-testid='search-show-more-button']"

    open_search = obj_nwt.open_search(
        filter=config.filter_text,
        months=config.months
    )

    if open_search['status'] == "OK":
        logger.info(f"Open browser: {open_search['message']}")
        start_date = open_search['start_date']

        continue_check_dates = True
        page_number = 0
        
        logger.info("Checking dates")
        while continue_check_dates:
            time.sleep(0.5)
            
            check_dates = obj_nwt.check_results_dates(
                list_path=list_location,
                list_items_path=list_items_location,
                close_tracker_button_path=reject_all_button_location,
                show_more_button_path=show_more_button_location,
                start_date=start_date
            )
            page_number += 1
            print("Page number: ", page_number)

            continue_check_dates = check_dates['continue']
            
            if check_dates['status'] == "NOK":
                logger.error(f"Checking dates: {check_dates['message']}")

        logger.info(f"Checking dates finished. Number of pages: {page_number}")
        
        logger.info("Getting the results")
        get_results = obj_nwt.get_results(
            list_path=list_location,
            list_items_path=list_items_location)

        if get_results['status'] == 'OK':
            logger.info("The results has been gotten")
            
            logger.info("Exporting the results to Excel file")
            try:
                df = pd.DataFrame(get_results['results'])

                df_expo = df.loc[df['date'] >= start_date]

                # export the result to excel
                df_expo.to_excel(
                    excel_writer='nyt_news.xlsx',
                    sheet_name='news',
                    index=False
                )
                logger.info("The results has been exported successfully")
            except:         
                logger.error(f"FAILED to export the results to Excel file.")
                
            if config.download_images:
                download_images(
                    excel_file_path="nyt_news.xlsx",
                    folder_to_export_path="images"
                )

        else:
            logger.error(f"Getting results: {get_results['message']}")

    else:
        logger.error(f"Open browser: {open_search['message']}")


def download_images(excel_file_path: str, folder_to_export_path: str) -> dict:
    try:
        logger.info("Starting downloading the pictures")
        # export Excel data to DataFrame
        df = pd.read_excel(excel_file_path).fillna("")
        print(df)
        
        # get links from DataFrame
        for i, item in df.iterrows():
            pic_url = item['picture_link']
            
            # get the name of the image
            if pic_url != "":
                # Parse the URL into a ParseResult object
                result = urlparse(pic_url)

                # Get the path component of the URL
                path = result.path

                # Create a Path object from the path
                p = Path(path)

                # Get the name attribute of the Path object
                picture_name = p.name
                print(picture_name)
                
                time.sleep(1)
                wget.download(
                    url=pic_url,
                    out=f"images\\{picture_name}"
                )
                
                print(f"Picture {picture_name} downloaded")
                
            logger.info("The pictures has been downloaded successfully")
            
    except Exception as ex:
        logger.error(f"FAILED to download the pictures. Error: {ex}")


if __name__ == "__main__":
    logger.info("PROCCESS STARTED")
    run_script()
    logger.info("PROCCESS FINISHED")

import time
from datetime import datetime

from robocorp.tasks import task
import robocorp.log as log
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP

from configurations import (
    DOWNLOAD_IMAGES, MONTHS, ATTEMPTS,
    WORKBOOK_PATH, SHEET_NAME, SHEET_COLUMNS
)

from nwt_search import NewYorkTimesScraper

from article import Article


@task
def run_script():
    log.info("Running script")
    obj_nwt = NewYorkTimesScraper()

    for attempt in range(ATTEMPTS):
        try:
            # get the data range
            date_range = obj_nwt.date_range(MONTHS)

            # open browser
            obj_nwt.open_search()

            continue_check_dates = True
            page_number = 0

            log.info("Checking dates")
            while continue_check_dates:
                time.sleep(0.5)

                check_dates = obj_nwt.check_results_dates(
                    start_date=date_range["start_date"]
                )
                page_number += 1
                print("Page number: ", page_number)

                continue_check_dates = check_dates

            log.info(
                f"Checking dates finished. Number of pages: {page_number}")

            log.info("Getting the results")
            lst_articles = obj_nwt.get_results(
                start_date=date_range["start_date"]
            )

            log.info("The list of articles has been gotten")
            log.info("Exporting the list of articles to Excel file")

            print("DONLOAD IMAGES: *** ", DOWNLOAD_IMAGES, " ***")
            # download images
            if DOWNLOAD_IMAGES:
                log.info("Downloading images...")
                for article in lst_articles:
                    if article.picture_link:
                        dowload_image(article)

            # export articles to excel
            export_to_excel_file(
                results_list=lst_articles,
                start_date=date_range["start_date"]
            )

            # get out of the loop if the execution has been succeeded
            break

        except Exception as ex:
            log.critical(f"FAIL to execute: {attempt + 1}: {str(ex)}")
            time.sleep(3)
            # browser.close_browser()
            if attempt == (ATTEMPTS - 1):
                log.info("The maximum number of attempts has been reached.")
                log.critical("*** THE EXECUTION HAS BEEN STOPPED ***")
                break


def export_to_excel_file(results_list: list[Article],
                         start_date: str
                         ):
    """Creates a workbook and then fill it with the results

    Args:
        results_list (list[dict]): Dict list
    """
    dt_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    columns = SHEET_COLUMNS

    # create a workbook
    excel = Files()
    excel.create_workbook(
        path=WORKBOOK_PATH,
        sheet_name=SHEET_NAME,
        fmt="xlsx"
    )
    excel.save_workbook()

    # insert header at the first row
    worksheet_column = 1
    for column in columns:
        excel.set_cell_value(1, worksheet_column, column)
        worksheet_column += 1

    # insert rows values
    worksheet_row = 2
    for item in results_list:
        worksheet_column = 1
        # check the date

        if datetime.strptime(item.date, "%Y-%m-%d") >= dt_start_date:
            dict_item = item.__dict__
            dict_item['has_money'] = item.has_money
            dict_item['phrase_count'] = item.phrase_count
            for key in list(dict_item.keys()):
                cell_value = dict_item[key]

                excel.set_cell_value(
                    row=worksheet_row,
                    column=worksheet_column,
                    value=cell_value
                )
                worksheet_column += 1
            worksheet_row += 1

    excel.save_workbook()


def dowload_image(article: Article):

    try:
        log.info("Starting downloading the pictures")
        http = HTTP()

        if article.picture_link:
            http.download(
                url=article.picture_link,
                target_file="output",
                overwrite=True
            )

            time.sleep(1)

        log.info("The pictures has been downloaded successfully")

    except Exception as ex:
        error = f"FAILED to download images from '{article.picture_link}'. "
        error += f"Error: {ex}"
        log.critical(error)

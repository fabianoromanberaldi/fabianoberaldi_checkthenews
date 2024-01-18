import logging
import sys
import time
from datetime import datetime

from pytz import timezone
from robocorp.tasks import task
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP

from configurations import Configuration
from nwt_search import NewYorkTimesScraper

config = Configuration()

# create log file
print("TIMEZONE: ", config.timezone)
tz_central = timezone(config.timezone)
dt_now = datetime.now(tz_central)
formated_date = dt_now.strftime("%Y%m%d")

log_file = "./output/automation_log.txt"
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


@task
def run_script():
    logger.info("Running script")
    obj_nwt = NewYorkTimesScraper(
        timeout=config.timeout_in_seconds
    )

    workbook_path = "./output/nyt_news.xlsx"
    sheet_name = "news"

    list_location = "//ol[@data-testid='search-results']"
    list_items_location = "//li[@data-testid='search-bodega-result']"

    reject_all_button_location = "//button[@data-testid='Reject all-btn']"
    show_more_button_location = (
        "//button[@data-testid='search-show-more-button']"
    )

    open_search = obj_nwt.open_search()

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

            attempts = 0
            if check_dates['status'] == "NOK":
                time.sleep(2)
                logger.error(f"Checking dates: {check_dates['message']}")
                attempts += 1
                if attempts >= config.attempts:
                    break
                else:
                    continue

        logger.info(f"Checking dates finished. Number of pages: {page_number}")

        logger.info("Getting the results")
        get_results = obj_nwt.get_results(
            start_date=start_date,
            list_path=list_location,
            list_items_path=list_items_location)

        if get_results['status'] == 'OK':
            logger.info("The results has been gotten")
            logger.info("Exporting the results to Excel file")

            try:
                lst_results = get_results['results']

                export_to_excel_file(
                    results_list=lst_results,
                    workbook_path=workbook_path,
                    sheet_name=sheet_name,
                    start_date=start_date
                )
                logger.info("The results has been exported successfully")

            except Exception as ex:
                logger.error(
                    f"FAILED to export the results to Excel file. Error: {ex}")

            if config.download_images:
                download_images(
                    excel_file_path=workbook_path,
                    sheet_name=sheet_name
                )

        else:
            logger.error(f"Getting results: {get_results['message']}")

    else:
        logger.error(f"Open browser: {open_search['message']}")


def export_to_excel_file(results_list: list[dict],
                         workbook_path: str,
                         sheet_name: str,
                         start_date: str
                         ):
    """Creates a workbook and then fill it with the results

    Args:
        results_list (list[dict]): Dict list
    """
    dt_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    total_count = len(results_list)

    # create a workbook
    excel = Files()
    excel.create_workbook(
        path=workbook_path,
        sheet_name=sheet_name,
        fmt="xlsx"
    )
    excel.save_workbook()

    # insert header at the first row
    worksheet_column = 1
    for key in results_list[0]:
        excel.set_cell_value(1, worksheet_column, key)
        worksheet_column += 1

    # insert rows values
    worksheet_row = 2
    for item in results_list:
        worksheet_column = 1
        # check the date

        if datetime.strptime(item['date'], "%Y-%m-%d") >= dt_start_date:
            for key in item.keys():
                if key == "total_count":
                    cell_value = total_count
                else:
                    cell_value = item[key]

                excel.set_cell_value(
                    row=worksheet_row,
                    column=worksheet_column,
                    value=cell_value
                )
                worksheet_column += 1
            worksheet_row += 1

    excel.save_workbook()


def download_images(excel_file_path: str, sheet_name: str):
    """Open excel file, and dowload images from \
        links ('picture_link' column)
    """
    try:
        logger.info("Starting downloading the pictures")
        http = HTTP()
        excel = Files()

        # open excel file
        excel.open_workbook(
            path=excel_file_path
        )

        # read excel worksheet
        worksheet = excel.read_worksheet_as_table(
            name=sheet_name,
            header=True
        )

        # close workbook
        excel.close_workbook()

        # get pictures links from the DataFrame
        for row in worksheet:
            pic_url = row['picture_link']

            # get the name of the image
            if pic_url:
                http.download(
                    url=pic_url,
                    target_file="output",
                    overwrite=True
                )

                time.sleep(1)

        logger.info("The pictures has been downloaded successfully")

    except Exception as ex:
        logger.error(f"FAILED to download the pictures. Error: {ex}")

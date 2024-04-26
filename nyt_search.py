import re
import time
from datetime import datetime, timedelta

import robocorp.log as log
from dateutil.relativedelta import relativedelta
from RPA.Browser.Selenium import Selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from article import Article
from date_converter import DateConverter

from assets import (
    list_location,
    list_items_location,
    reject_all_button_location,
    show_more_button_location,
    date_text_class_name,
    title_text_class_name,
    description_text_class_name
)

from configuration import (
    SEARCH_PHRASE,
    MONTHS,
    BROWSER,
    AUTO_CLOSE,
    TIMEOUT_IN_SECONDS
)


class NewYorkTimesScraper():
    def __init__(self) -> None:
        self.browser = Selenium()
        self.browser.set_selenium_timeout(
            value=timedelta(seconds=TIMEOUT_IN_SECONDS)
        )
        self.browser.auto_close = AUTO_CLOSE

    def _url_builder(self, filter: str, months: int) -> str:
        """Build the url, based on text filter and quantity of months

        Args:
            filter (str): Search phrase
            months (int): Number of months for which you need to receive news \
                (if 0, means current month)

        Returns:
            str: str
        """
        if not isinstance(months, int):
            months = int(months)

        # get the data range
        date_range = self.date_range(months)
        url = f"https://www.nytimes.com/search?dropmab=false&query={filter}&"
        url += f"sort=newest&startDate={date_range['start_date']}&"
        url += f"endDate={date_range['end_date']}&types=article"

        return url

    def date_range(self, months: int) -> dict:
        """Return the 'Start Date' and 'End Date' depending on the given month

        Args:
            months (int): Number of months

        Returns:
            dict: dictionary
        """
        if not isinstance(months, int):
            months = int(months)

        dt_end_date = datetime.today()

        if months == 0:
            # current month
            dt_start_date = datetime(
                year=dt_end_date.year,
                month=dt_end_date.month,
                day=1
            )
        else:
            dt_start_date = dt_end_date - relativedelta(months=months)

        start_date = dt_start_date.strftime("%Y-%m-%d")
        end_date = dt_end_date.strftime("%Y-%m-%d")

        log.info(f"Date Range: {start_date} to {end_date}")

        return {
            "start_date": start_date,
            "end_date": end_date
        }

    def open_search(self):
        """Open search
        """
        try:
            url = self._url_builder(
                filter=SEARCH_PHRASE,
                months=MONTHS
            )

            log.info(f"URL: {url}")

            # "headlessfirefox"
            self.browser.open_browser(
                url=url,
                browser=BROWSER
            )

            self.browser.maximize_browser_window()
            log.info("The browser has been opened successfully.")

        except Exception as ex:
            error = f"FAILED to open the browser. Error: {ex}"
            log.critical(error)
            raise Exception(error)

    def check_results_dates(self, start_date: str) -> bool:
        """Check the dates of the results

        Args:
            start_date (str): "Start date" to be checked

        Returns:
            _type_: bool
        """
        try:
            converter = DateConverter()
            dt_start_date = datetime.strptime(start_date, "%Y-%m-%d")

            # if "Your tracker settings" window is open, then close it
            time.sleep(2)
            if self.browser.click_element_if_visible(
                locator=reject_all_button_location
            ):
                self.browser.scroll_element_into_view(
                    locator=reject_all_button_location
                )
                self.browser.click_button(
                    locator=reject_all_button_location
                )

            time.sleep(2)

            # check if the button "Show more" exists
            # if button exists, click the button
            if self.browser.does_page_contain_button(
                locator=show_more_button_location
            ):
                time.sleep(2)

                if not self.browser.is_element_focused(
                    locator=show_more_button_location
                ):
                    self.browser.set_focus_to_element(
                        locator=show_more_button_location
                    )
                    time.sleep(1)

                self.browser.click_button(
                    locator=show_more_button_location
                )

            # check if result list is visble
            if self.browser.is_element_visible(
                locator=list_location
            ):
                # find items
                items = self.browser.find_elements(
                    locator=list_items_location
                )

                lst_dates = []
                # check items date
                for item in items:
                    if item.find_element(
                        By.CLASS_NAME,
                        date_text_class_name
                    ).is_enabled():

                        # get the date
                        date_text = item.find_element(
                            By.CLASS_NAME,
                            date_text_class_name
                        ).text

                        dt_today = datetime.today()
                        # check if date string contains 'ago', like '8h ago'
                        if 'ago' in date_text:
                            date_str = dt_today.strftime("%Y-%m-%d")
                        else:
                            date_str = (
                                converter.convert_text_to_formatted_date(
                                    date_text=date_text
                                ))

                        dt_result_start_date = datetime.strptime(
                            date_str,
                            "%Y-%m-%d"
                        )

                        if dt_result_start_date not in lst_dates:
                            lst_dates.append(dt_result_start_date)

            if not self.browser.does_page_contain_button(
                locator=show_more_button_location
            ):
                return False
            else:
                if min(lst_dates) <= dt_start_date:
                    return False
                else:
                    return True

        except Exception as ex:
            error = f"FAILED to check results dates. Error: {ex}"
            log.critical(error)
            raise Exception(error)

    def get_results(self,
                    start_date: str
                    ) -> list[Article]:
        """Get all loaded results

        Args:
             start_date (str): "Start date" to be checked

        Returns:
            _type_: list[Article]
        """
        date_converter = DateConverter()
        lst_results = []

        try:
            time.sleep(3)
            if self.browser.is_element_visible(
                locator=list_location
            ):

                # find items
                items = self.browser.find_elements(
                    locator=list_items_location
                )

                for item in items:
                    if item.find_element(
                            By.CLASS_NAME,
                            date_text_class_name
                    ).is_enabled():

                        # get the date
                        date_text = item.find_element(
                            By.CLASS_NAME,
                            date_text_class_name
                        ).text

                        # check if date string contains 'ago', like '8h ago'
                        if 'ago' in date_text:
                            dt_today = datetime.today()
                            date = dt_today.strftime("%Y-%m-%d")
                        else:
                            # date = self.convert_text_to_formatted_date(
                            #     date_text=date_text
                            # )
                            date = (
                                date_converter.convert_text_to_formatted_date(
                                    date_text
                                ))

                        # get the title
                        if item.find_element(
                                By.CLASS_NAME,
                                title_text_class_name).is_enabled():

                            title = item.find_element(
                                By.CLASS_NAME,
                                title_text_class_name).text
                        else:
                            title = ""

                        # get the description if available
                        try:
                            description = item.find_element(
                                By.CLASS_NAME,
                                description_text_class_name
                            ).text
                        except NoSuchElementException:
                            description = ""

                        # get the picture filename
                        try:
                            picture_tag = item.find_element(
                                By.TAG_NAME, 'figure'
                            )

                            pic_innerHtml = picture_tag.get_attribute(
                                'innerHTML'
                            )

                            picture_filename = re.search(
                                r'\/([^\/]+\.(?:jpg|jpeg|png|gif))',
                                pic_innerHtml
                            ).group(1)

                        except NoSuchElementException:
                            picture_filename = ""

                        # get the picture link
                        try:
                            picture_tag = item.find_element(
                                By.TAG_NAME, 'figure'

                            )
                            pic_innerHtml = picture_tag.get_attribute(
                                'innerHTML'
                            )

                            picture_link = re.search(
                                r'src="(.*?)"',
                                pic_innerHtml
                            ).group(1)

                        except NoSuchElementException:
                            picture_link = ""

                    if (
                        datetime.strptime(date, "%Y-%m-%d")
                        >= datetime.strptime(start_date, "%Y-%m-%d")
                    ):
                        article = Article(
                            date=date,
                            search_phrase=SEARCH_PHRASE,
                            title=title,
                            description=description,
                            picture_filename=picture_filename,
                            picture_link=picture_link
                        )

                        lst_results.append(article)

            return lst_results

        except Exception as ex:
            error = f"FAILED to get the results. Error: {ex}"
            log.critical(error)
            raise Exception(error)

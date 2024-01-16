import re
import time
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from RPA.Browser.Selenium import Selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
#from selenium.webdriver.firefox.options import Options


class NewYorkTimesScraper():
    def __init__(self, timeout: int) -> None:
        self.browser = Selenium()
        self.timeout = timeout
        self.browser.set_selenium_timeout(
            value=timedelta(seconds=self.timeout)
        )
        self.browser.auto_close = True

    def _date_range(self, months: int) -> dict:
        """Return the 'Start Date' and 'End Date' depending on the given month

        Args:
            months (int): _description_

        Returns:
            dict: _description_
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

        return {
            "start_date": start_date,
            "end_date": end_date
        }

    def _url_builder(self, filter: str, months: int) -> str:
        """Build the url, based on text filter and quantity of months

        Args:
            filter (str): Search phrase
            months (int): Number of months for which you need to receive news (if 0, means current month)

        Returns:
            str: str
        """
        if not isinstance(months, int):
            months = int(months)

        # get the data range
        date_range = self._date_range(months)
        url = f"https://www.nytimes.com/search?dropmab=false&query={filter}&sort=newest&startDate={date_range['start_date']}&endDate={date_range['end_date']}&types=article"

        return {
            "filter": filter,
            "start_date": date_range['start_date'],
            "end_date": date_range['end_date'],
            "url": url
        }

    def _find_element(self, element_path: str, timeout: int) -> bool:
        """Check if element exists or not

        Args:
            element_path (str): Element locator
            timeout (int): Timeout (waiting time)

        Returns:
            bool: True or False
        """
        try:
            self.browser.wait_until_element_is_visible(
                locator=element_path,
                timeout=timeout
            )
            self.browser.find_element(element_path)
            return True
        except Exception as ex:
            print("ERROR : ", ex)
            return False

    def _convert_text_to_formatted_date(self,
                                        date_text: str,
                                        format="%Y-%m-%d") -> str:
        # Try to convert the text to a date object using the format "%b. %d, %Y"
        try:
            current_year = datetime.today().year
            date = datetime.strptime(date_text, "%b. %d, %Y").date()

        except ValueError:
            date_text = date_text + ", " + str(current_year)
            date = datetime.strptime(date_text, "%b. %d, %Y").date()

        formated_date = date.strftime(format)
        return formated_date

    def open_search(self, filter: str,
                    months: int = 0
                    ) -> dict:
        """Open search

        Args:
            filter (str): Search phrase
            months (int): Number of months for which you need to receive news
                          (if 0, means current month)

        Returns:
            _type_: dict
        """
        try:
            if not isinstance(months, int):
                months = int(months)

            url_builder = self._url_builder(filter, months)

            self.browser.open_browser(
                url=url_builder['url'],
                browser="headlessfirefox"
            )

            self.browser.maximize_browser_window()

            return {
                    "status": "OK",
                    "start_date": url_builder['start_date'],
                    "end_date": url_builder['end_date'],
                    "url": url_builder['url'],
                    "message": "The browser was opened successfully"
                }
        except Exception as ex:
            return {
                "status": "NOK",
                "start_date": url_builder['start_date'],
                "end_date": url_builder['end_date'],
                "url": url_builder['url'],
                "message": f"FAILED to open the browser. Error: {ex}"
            }

    def click_on_element(self, element_path: str):

        try: 
            if self.browser.is_element_visible(
                locator=element_path
            ):
                self.browser.click_element(
                    locator=element_path
                )
                return {
                    "status": "OK",
                    "result": True,
                    "message": "Element clicked"
                }
            else:
                return {
                    "status": "OK",
                    "result": False,
                    "message": "Element is not visible"
                }

        except Exception as ex:
            return {
                "status": "NOK",
                "result": False,
                "message": f"FAILED to click on element. Error: {ex}"
            }

    def check_results_dates(self,
                            list_path: str,
                            list_items_path: str,
                            close_tracker_button_path: str,
                            show_more_button_path: str,
                            start_date: str
                            ):
        """Check the dates of the results

        Args:
            list_path (str): List element location
            list_items_path (str): List items elements location
            close_tracker_button_path (str): 'Close Tracker' button location
            show_more_button_path (str): 'Show more' button location
            start_date (str): "Start date" to be checked

        Returns:
            _type_: dict
        """
        try:
            dt_start_date = datetime.strptime(start_date, "%Y-%m-%d")

            # if "Your tracker settings" window is open, then close it
            time.sleep(2)
            if self.browser.click_element_if_visible(
                locator=close_tracker_button_path
            ):
                self.browser.click_button(
                    locator=close_tracker_button_path
                )

            # check if the button "Show more" exists
            if self.browser.does_page_contain_button(
                locator=show_more_button_path
            ):
                self.browser.scroll_element_into_view(
                    locator=show_more_button_path
                )
                self.browser.click_button(
                    locator=show_more_button_path
                )

            if self._find_element(                
                element_path=list_path,
                timeout=5
            ):
                # find items
                items = self.browser.find_elements(
                    list_items_path
                )

                lst_dates = []
                # check items date
                for item in items:
                    if item.find_element(
                        By.CLASS_NAME,
                        'css-17ubb9w'
                    ).is_enabled():

                        # get the date
                        date_text = item.find_element(
                            By.CLASS_NAME,
                            'css-17ubb9w').text

                        # check if date string contains 'h', like '8h ago'
                        if 'h' in date_text:
                            dt_today = datetime.today()
                            date_str = dt_today.strftime("%Y-%m-%d")
                        else:
                            date_str = self._convert_text_to_formatted_date(
                                date_text=date_text
                            )

                        dt_result_start_date = datetime.strptime(
                            date_str,
                            "%Y-%m-%d"
                        )

                        if dt_result_start_date not in lst_dates:
                            lst_dates.append(dt_result_start_date)

                if min(lst_dates) < dt_start_date:
                    print("DATES ============================")
                    print(lst_dates)
                    return {
                        "status": "OK",
                        "continue": False,
                        "message": ""
                    }
                else:
                    return {
                        "status": "OK",
                        "continue": True,
                        "message": ""                   
                    }

        except Exception as ex:
            return {
                "status": "NOK",
                "continue": False,
                "message": f"FAILED to check results dates. Error: {ex}"
            }

    def get_results(self, list_path: str, list_items_path: str) -> list[dict]:
        """Get all loaded results

        Args:
            list_path (str): List element location
            list_items_path (str): List items location

        Returns:
            list[dict]: list
        """

        lst_results = []

        try:
            if self._find_element(
                element_path=list_path,
                timeout=5
            ):

                # find items
                items = self.browser.find_elements(
                    list_items_path
                )

                for item in items:
                    if item.find_element(
                            By.CLASS_NAME,
                            'css-17ubb9w').is_enabled():

                        # get the date
                        date_text = item.find_element(
                            By.CLASS_NAME,
                            'css-17ubb9w').text

                        # check if date string contains 'h', like '8h ago'
                        if 'h' in date_text:
                            dt_today = datetime.today()
                            date = dt_today.strftime("%Y-%m-%d")
                        else:
                            date = self._convert_text_to_formatted_date(
                                date_text=date_text
                            )

                        # get the title
                        if item.find_element(
                                By.CLASS_NAME,
                                'css-2fgx4k').is_enabled():
                            
                            title = item.find_element(
                                By.CLASS_NAME,
                                'css-2fgx4k').text
                        else:
                            title = ""

                        # get the description if available
                        try:
                            description = item.find_element(
                                By.CLASS_NAME,
                                'css-16nhkrn').text
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

                        # check if description or title has currency characters
                        money_pattern = r"\$[\d,]+(\.\d+)?|\d+ dollars|\d+ USD"
                        has_money = bool(
                            re.search(
                                money_pattern,
                                title + description)
                        )

                    dict_result = {
                        "date": date,
                        "title": title,
                        "description": description,
                        "picture_filename": picture_filename,
                        "picture_link": picture_link,
                        "has_money": has_money
                    }

                    lst_results.append(dict_result)

                return {
                    "status": "OK",
                    "results": lst_results,
                    "results_quantity": len(lst_results),
                    "message": "The results has been gotten succesfuly"
                }

        except Exception as ex:
            return {
                "status": "NOK",
                "results": "",
                "results_quantity": 0,
                "message": f"FAILED to get the results. Error: {ex}"
            }

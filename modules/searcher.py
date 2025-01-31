import os

from contextlib import contextmanager

from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from modules import objects
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from modules.types import Filter

DEFAULT_GUI_WAITING_TIME: int = 10


class Searcher:
    def __init__(self) -> None:
        self.__driver_path: str = rf"{os.environ['DRIVER_PATH']}"
        self.__driver = None
        self.__wait = None

    def __setup_driver(self) -> None:
        """
        Set up Selenium Web driver for Chrome and Options
        """
        service: Service = Service(self.__driver_path)
        options = webdriver.ChromeOptions()

        # Chrome exe
        chrome_path = os.environ['CHROME_PATH']
        options.add_argument(f"chrome.exe={chrome_path}")

        # Run the browser in headless mode
        options.headless = True
        self.__driver: WebDriver = webdriver.Chrome(service=service, options=options)

    @contextmanager
    def start(self):
        try:
            self.__setup_driver()

            # Define max time to find elements
            self.__wait: WebDriverWait = WebDriverWait(self.__driver, DEFAULT_GUI_WAITING_TIME)
            yield
        finally:
            self.__close_driver()

    def __close_driver(self):
        if self.__driver:
            self.__driver.quit()

    def search_wgs(self, link: str, filters: dict[str, str]) -> None:
        """
        Starts a new search from the WG-Gesucht website

        :param filters: dictionary to filter the search
        :param link: URL to the website
        """
        # Open link from the browser
        self.__driver.get(link)
        # Cleans the screen from cookies request
        self.__click_by_xpath("save-cookies")

        self.__apply_filters(filters)

    def __apply_filters(self, filters: dict[str, str]) -> None:
        """
        Apply filters to the search

        :param filters: dictionary to filter the search
        """
        # Open all filters view
        self.__click_by_xpath("more-options")

        for k, v in filters.items():
            if k == Filter.RentType.value:
                self.__try_filter(
                    self.__check_from_dropdown_menu,
                    label=k,
                    options=v.split(','),
                )
            elif k == Filter.EarliestMove.value:
                self.__click_by_xpath(k)
                self.__try_filter(
                    self.__select_date,
                    date_str=v,
                )
            elif k == Filter.Searched.value:
                self.__try_filter(
                    self.__check_from_dropdown_menu,
                    label=k,
                    options=v.split(','),
                )
        # Enable filters
        self.__click_by_xpath("apply-filters")

    def __check_from_dropdown_menu(self, label: str, options: list[str]) -> None:
        """
        Select the desired rent types to the filters

        :param str label: Label of the dropdown menu
        :param list[str] options: All options to check from the dropdown menu
        """
        self.__click_by_xpath(label)
        dropdown_menu = self.__wait.until(ec.presence_of_element_located((By.XPATH, objects.xpaths["dropdown-menu"])))
        for option in options:
            xpath = f"//a[contains(., '{option}')]"
            # Find the element containing the rent type
            rent_type_checkbox = dropdown_menu.find_element(By.XPATH, xpath)
            rent_type_checkbox.click()

    def __select_date(self, date_str: str) -> None:
        """
        Selects a date in a date calendar.

        :param date_str: The format of the date string should be "day.month_name.year" (e.g. 1.April.2025)
        """
        date: list[str] = date_str.split(".")

        try:
            self.__select_calendar_dropdown("select-year", date[2])
            self.__select_calendar_dropdown("select-month", date[1])
            self.__select_calendar_day(int(date[0]))  # Remove any 0 on the left
        except NoSuchElementException:
            raise RuntimeError(
                "Could not select date. Please check that the string is in the correct format (e.g. '1.January.2000)'")

    def __select_calendar_dropdown(self, label: str, option: str) -> None:
        """
        Select a given Month/Year from a calendar view

        :param label: "select-year" or "select-month"
        :param option: The name of the desired option in the dropdown (e.g. "2000" if it's a year or "January" if it's
        a month)
        """
        dropdown_xpath: str = objects.xpaths[label]
        dropdown: WebElement = self.__wait.until(ec.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        dropdown.click()

        option_xpath = f"//option[contains(., '{option}')]"
        select_option: WebElement = dropdown.find_element(By.XPATH, option_xpath)
        select_option.click()

    def __select_calendar_day(self, day: int) -> None:
        """
        Select a given day from a calendar view

        :param int day: Number of the desired day to select
        """
        calendar_xpath: str = objects.xpaths["date-calendar"]
        calendar = self.__wait.until(ec.element_to_be_clickable((By.XPATH, calendar_xpath)))
        day_xpath: str = f"//td[contains(., '{day}')]"
        day_in_calendar = calendar.find_element(By.XPATH, day_xpath)
        day_in_calendar.click()

    def __click_by_xpath(self, xpath_key: str) -> None:
        """
        Find and click an object by its xpath key within the xpaths dictionary

        :param xpath_key: xpath key to retrieve the identifier from the xpaths dictionary
        """
        # Get the xpath identifier
        element: str = objects.xpaths[xpath_key]

        clickable_element = self.__wait.until(ec.element_to_be_clickable((By.XPATH, element)))
        clickable_element.click()

    @staticmethod
    def __try_filter(filter_func: callable, *args, **kwargs):
        """
        Skips the filter if something fails

        :param filter_func: method that should act to meet the filter
        """
        try:
            filter_func(*args, **kwargs)
        except Exception as e:
            print(f"Could not apply filter: {e}")
            return

    def get_source(self) -> str:
        return self.__driver.page_source

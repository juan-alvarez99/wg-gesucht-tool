import os

from contextlib import contextmanager
from modules import objects
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

DEFAULT_GUI_WAITING_TIME: int = 10


class Searcher:
    def __init__(self) -> None:
        self.__driver_path: str = rf"{os.environ['DRIVER_PATH']}"
        self.__driver: WebDriver | None = None
        self.__wait: WebDriverWait | None = None

    def __setup_driver(self) -> None:
        """
        Set up Selenium Web driver for Chrome and Options
        """
        service: Service = Service(self.__driver_path)
        options = webdriver.ChromeOptions()

        # Chrome exe
        chrome_path = os.environ['CHROME_PATH']
        options.add_argument(f"chrome.exe={chrome_path}")

        # Keep the browser open if the script crashes.
        options.add_experimental_option("detach", True)
        options.add_argument("--start-maximized")
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

    def apply_filters(self, filters: dict[str, str]) -> None:
        """
        Apply filters to the search

        :param filters: dictionary to filter the search
        """
        # Open all filters view
        self.click_by_xpath("more-options")

        for k, v in filters.items():
            if k == "rent-type":
                self.check_rent_types(v.split(','))

        # Apply filters
        self.click_by_xpath("apply-filters")

    def search_wgs(self, link: str, filters: dict[str, str]) -> None:
        """
        Starts a new search from the WG-Gesucht website

        :param filters: dictionary to filter the search
        :param link: URL to the website
        """
        # Open link from the browser
        self.__driver.get(link)
        # Cleans the screen from cookies request
        self.click_by_xpath("save-cookies")

        self.apply_filters(filters)

    # def get_all_offers(self):
    #     offer_xpath = objects.xpaths['wg-card']
    #     offers = self.__wait.until(ec.presence_of_all_elements_located((By.XPATH, offer_xpath)))
    #
    #     for offer in offers:
    #         print(type(offer))
    #
    #         pass

    def check_rent_types(self, rent_types: list[str]) -> None:
        """
        Select the desired rent types to the filters

        :param rent_types: list of rent types for the filter
        """
        self.click_by_xpath("rent-type")
        dropdown_menu = self.__wait.until(ec.presence_of_element_located((By.XPATH, objects.xpaths["dropdown-menu"])))
        for rent_type in rent_types:
            xpath = f"//a[contains(., '{rent_type}')]"
            # Find the element containing the rent type
            rent_type_checkbox = dropdown_menu.find_element(By.XPATH, xpath)
            rent_type_checkbox.click()

    def click_by_xpath(self, xpath_key: str) -> None:
        """
        Find and click an object by its xpath key within the xpaths dictionary

        :param xpath_key: xpath key to retrieve the identifier from the xpaths dictionary
        """
        # Get the xpath identifier
        element: str = objects.xpaths[xpath_key]

        clickable_element = self.__wait.until(ec.element_to_be_clickable((By.XPATH, element)))
        clickable_element.click()

    def get_source(self) -> str:
        return self.__driver.page_source

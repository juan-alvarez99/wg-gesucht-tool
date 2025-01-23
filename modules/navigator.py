import os

from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.ie.webdriver import WebDriver


class Navigator:
    def __init__(self) -> None:
        self.__driver_path: str = rf"{os.environ['DRIVER_PATH']}"
        self.__driver = None

    def __setup_driver(self) -> None:
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
            yield self.__driver
        finally:
            self.__close_driver()

    def __close_driver(self):
        if self.__driver:
            self.__driver.quit()
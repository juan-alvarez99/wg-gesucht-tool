import re
import time

import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from modules.wg import WG


class WgTracker:
    def __init__(self, link):
        self.soup: BeautifulSoup = self.get_soup(link)
        self.list_of_properties: list = []

    def get_all_offers(self) -> ResultSet:
        # Extract the links to the properties into a list with only the links (href)
        return self.soup.find_all("div", {"class": ["wgg_card","offer_list_item"]})

    @staticmethod
    def get_soup(link) -> BeautifulSoup:
        # Scrap the web to get the html text
        response = requests.get(link)
        code = response.text
        return BeautifulSoup(code, 'html.parser')

    @staticmethod
    def get_room_data(wgg_card_tag: Tag):
        middle_row = wgg_card_tag.find('div', {'class': ['row', 'noprint', 'middle']})
        text_in_row = middle_row.find_all('b')

        room_data: dict[str, str] = {}
        for data in text_in_row:
            if "€" in data.text:
                room_data["rent"] = data.text
            elif "m" in data.text:
                room_data["size"] = data.text

        return room_data

    @staticmethod
    def get_title(wgg_card_tag: Tag) -> str:
        title = wgg_card_tag.find('h3', {'class': ['truncate_title', 'no_print']})
        return title.get("title")

    def parse_data(self, offer_list: list):
        for offer in offer_list:
            title: str = self.get_title(offer)
            room_data: dict = self.get_room_data(offer)
            self.list_of_properties.append(WG(title=title, rent=room_data["rent"], size=room_data["size"]))

        # # Extract the prices into a list with the format "$x,xxx" ignoring the rest (strings like: "/month", "+ bd"...)
        # price_tag_list = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")
        # clean_prices = [re.compile(r'\$\d+(?:,\d+)?').search(price.getText()).group() for price in price_tag_list]
        #
        # # Extract the address of the properties in a regular format
        # addresses_tag_list = soup.find_all("address")
        # clean_addresses = [re.sub(r'[\s|]+', ' ', address.getText().strip()) for address in addresses_tag_list]
        #
        # # Creates the dictionary
        # for i in range(len(clean_addresses)):
        #     property_dict = {
        #         "address": clean_addresses[i],
        #         "price": clean_prices[i],
        #         "link": clean_links[i]
        #     }
        #     self.list_of_properties.append(property_dict)

    def fill_form(self, driver):
        pass
        # The time to wait until an element is placed before throwing an exception
        # wait = WebDriverWait(driver, 10)
        # for property_data in self.list_of_properties:
        #     # Fills all the fields of the form with the data extracted
        #     address_field = wait.until(ec.element_to_be_clickable((By.XPATH, xpaths.ADDRESS_TEXTFIELD)))
        #     address_field.click()
        #     address_field.send_keys(property_data["address"])
        #
        #     price_field = wait.until(ec.element_to_be_clickable((By.XPATH, xpaths.PRICE_TEXTFIELD)))
        #     price_field.click()
        #     price_field.send_keys(property_data["price"])
        #
        #     link_field = wait.until(ec.element_to_be_clickable((By.XPATH, xpaths.LINK_TEXTFIELD)))
        #     link_field.click()
        #     link_field.send_keys(property_data["link"])
        #     time.sleep(1)
        #
        #     # Sends the filled form
        #     send_button = wait.until(ec.element_to_be_clickable((By.XPATH, xpaths.SEND_BUTTON)))
        #     send_button.click()
        #
        #     # Goes to the next form to fill it with the data from the next element
        #     repeat_form = wait.until(ec.element_to_be_clickable((By.XPATH, xpaths.REPEAT_BUTTON)))
        #     repeat_form.click()
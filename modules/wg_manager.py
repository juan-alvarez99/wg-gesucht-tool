import re

from bs4 import BeautifulSoup, ResultSet, Tag
from modules.links import links
from modules.wg import WG


class WgManager:
    def __init__(self, html):
        self.__soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        self.__all_offers: list[WG] = []

    def __find_all_offers(self) -> ResultSet:
        """
        Get a list of all offers found in the search

        :return: Set of all the rent offers found
        """
        # Extract the links to the properties into a list with only the links (href)
        return self.__soup.find_all("div", {"class": ["wgg_card", "offer_list_item"]})

    def __get_room_data(self, wgg_card_tag: Tag) -> dict:
        """
        Parse data from the offer attributes such as the title, rent price or room size

        :param wgg_card_tag: Object containing the WG information
        :return: Dictionary containing Rent Price and Room Size
        """
        title_tag: Tag = self.__get_title(wgg_card_tag)
        link_tag: Tag = self.__get_link_from_title(title_tag)

        room_data: dict = {
            "title": title_tag.get("title"),
            "link": links["LINK-BASE"] + link_tag.get("href"),
        }

        middle_row = wgg_card_tag.find('div', {'class': ['row', 'noprint', 'middle']})
        text_in_row = middle_row.find_all('b')

        for data in text_in_row:
            if "€" in data.text:
                room_data["rent"] = self.__extract_number(data.text)
            elif "m" in data.text:
                room_data["size"] = self.__extract_number(data.text)

        return room_data

    def __parse_data(self) -> None:
        """
        Extract the main data from html and parse the data into WG objects
        """
        offers = self.__find_all_offers()
        for offer in offers:
            room_data: dict = self.__get_room_data(offer)
            self.__all_offers.append(
                WG(
                    title=room_data["title"],
                    rent=room_data["rent"],
                    size=room_data["size"],
                    link=room_data["link"],
                )
            )

    def get_all_offers(self):
        self.__parse_data()
        return self.__all_offers

    @staticmethod
    def __get_title(wgg_card_tag: Tag) -> Tag:
        """
        Extract the title of the offer

        :param wgg_card_tag: Object containing the WG information
        :return: tag containing the title
        """
        title: Tag = wgg_card_tag.find('h3', {'class': ['truncate_title', 'no_print']})
        return title

    @staticmethod
    def __get_link_from_title(title_tag: Tag) -> Tag:
        """
        Extract the link to the offer from the offer title

        :param title_tag: Object containing the link
        :return: tag containing the link to the offer
        """
        link: Tag = title_tag.find('a')
        return link

    @staticmethod
    def __extract_number(string: str) -> int:
        """Extracts the first integer number from a given string

        :param string: The input string

        :return: The extracted integer number, or None if no number is found
        """
        match = re.search(r'\d+', string)
        if match:
            return int(match.group())
        else:
            return 0

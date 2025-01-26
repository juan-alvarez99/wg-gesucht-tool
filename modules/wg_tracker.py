import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from modules.wg import WG


class WgTracker:
    def __init__(self, link):
        self.soup: BeautifulSoup = self.get_soup(link)
        self.list_of_properties: list[WG] = []

    def get_all_offers(self) -> ResultSet:
        """
        Get a list of all offers found in the search

        :return: Set of all the rent offers found
        """
        # Extract the links to the properties into a list with only the links (href)
        return self.soup.find_all("div", {"class": ["wgg_card","offer_list_item"]})

    @staticmethod
    def get_soup(link) -> BeautifulSoup:
        """
        Get the HTML Code from a website

        :param link: URL of the website to scrap
        :return: HTML code as a bs4 object
        """
        # Scrap the web to get the html text
        response = requests.get(link)
        code = response.text
        return BeautifulSoup(code, 'html.parser')

    @staticmethod
    def get_room_data(wgg_card_tag: Tag) -> dict[str, str]:
        """
        Parse the rest of the offer attributes such as rent price and room size

        :param wgg_card_tag: Object containing the WG information
        :return: Dictionary containing Rent Price and Room Size
        """
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
        """
        Extract the title of the offer

        :param wgg_card_tag: Object containing the WG information
        :return: Title as a string
        """
        title = wgg_card_tag.find('h3', {'class': ['truncate_title', 'no_print']})
        return title.get("title")

    def parse_data(self, offer_list: list[Tag]) -> None:
        """
        Extract the main data from a set of offers such as the rent price or the size of the room

        :param offer_list: All offers containing the data
        """
        for offer in offer_list:
            title: str = self.get_title(offer)
            room_data: dict = self.get_room_data(offer)
            self.list_of_properties.append(WG(title=title, rent=room_data["rent"], size=room_data["size"]))

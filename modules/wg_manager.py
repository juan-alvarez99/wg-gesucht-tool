from bs4 import BeautifulSoup, ResultSet, Tag
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

    @staticmethod
    def __get_room_data(wgg_card_tag: Tag) -> dict[str, str]:
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
    def __get_title(wgg_card_tag: Tag) -> str:
        """
        Extract the title of the offer

        :param wgg_card_tag: Object containing the WG information
        :return: Title as a string
        """
        title = wgg_card_tag.find('h3', {'class': ['truncate_title', 'no_print']})
        return title.get("title")

    def __parse_data(self) -> None:
        """
        Extract the main data from html and parse the data into WG objects
        """
        offers = self.__find_all_offers()
        for offer in offers:
            title: str = self.__get_title(offer)
            room_data: dict = self.__get_room_data(offer)
            self.__all_offers.append(WG(title=title, rent=room_data["rent"], size=room_data["size"]))


    def get_all_offers(self):
        self.__parse_data()
        return self.__all_offers
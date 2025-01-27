import os
import requests

from modules.wg import WG


class SheetManager:
    def __init__(self):
        self.__sheet_url: str = os.environ["SHEETY_ENDPOINT"]
        self.__headers: dict[str, str] = {"Authorization": os.environ["HEADER"]}
        self.__registered_wgs: list[WG] = self.__get_known_offers()

    def __post_new_offers(self, new_entry: dict) -> None:
        response = requests.post(self.__sheet_url, headers=self.__headers, json=new_entry)

        if response.status_code != 200:
            raise Exception(f"Could not post new wg in Google Sheet: {response.status_code}")

    def __get_known_offers(self) -> list[WG]:
        response = requests.get(self.__sheet_url, headers=self.__headers)

        if response.status_code == 200:
            offers_list: list[dict[str, str]] = response.json()["overview"]
            known_wgs = [
                WG(
                    title=offer["title"],
                    rent=int(offer["rent"]),
                    size=int(offer["size"]),
                    link=offer["link"],
                ) for offer in offers_list
            ]
            return known_wgs

        else:
            raise Exception(f"Could not connect to Google Sheet: {response.status_code}")

    def post_offers(self, wg_list: list[WG]) -> None:
        for wg in wg_list:
            self.__post_new_offers(self.__wg_to_json(wg))

    def get_registered_wgs(self) -> list[WG]:
        return self.__registered_wgs

    @staticmethod
    def __wg_to_json(wg: WG) -> dict:
        return {
            "overview": {
                "title": wg.title,
                "rent": wg.rent,
                "size": wg.size,
                "link": wg.link
            }
        }

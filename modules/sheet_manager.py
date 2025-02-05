import os
import requests
from datetime import datetime

from modules.wg import WG
from modules.types import LogStatus


class SheetManager:
    def __init__(self):
        self.__base_url: str = os.environ["SHEETY_ENDPOINT"]
        self.__headers: dict[str, str] = {"Authorization": os.environ["HEADER"]}
        self.__registered_wgs: list[WG] = self.__get_known_offers()
        self.__warnings: list[str] = []

    def __post(self, sheet_name: str, new_entry: dict) -> None:
        """
        Create a POST request to the Google Sheet using the Sheety endpoint.

        :param str sheet_name: name of the sheet to post the data
        :param new_entry: dictionary with the data to post. It has to have the following structure:
            {
                "column_1": "entry_1",
                "column_2": "entry_2",
                "column_n": "entry_n",
            }
        :type new_entry: dict[str, str]
        """
        url: str = f"{self.__base_url}/{sheet_name}"
        body: dict = {
            sheet_name: new_entry,
        }
        response = requests.post(url, headers=self.__headers, json=body)

        if response.status_code != 200:
            raise Exception(f"Could not post new WG in Google Sheet: {response.status_code}")

    def __get_known_offers(self) -> list[WG]:
        url: str = f"{self.__base_url}/overview"
        response = requests.get(url, headers=self.__headers)

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
        """
        Post all new offers on Google Sheets

        :param wg_list: list of new WG objects found
        :type wg_list: list[WG]
        """
        for wg in wg_list:
            self.__post("overview", wg.to_dict())
    
    def post_log(self, status: LogStatus, log: str):
        """
        Post the result of the search on Google Sheets

        :param LogStatus status: status of the execution
        :param str log: details to add to the log
        """
        body: dict[str, str] = {
            "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "result": status.value,
            "log": log,
        }
        self.__post("log", body)

    def add_warning(self, warning: str) -> None:
        """
        Add warnings for the report

        :param str warning: informatoin about the warning
        """
        self.__warnings.append(warning)

    def get_registered_wgs(self) -> list[WG]:
        return self.__registered_wgs

    def get_warnings(self) -> list[str]:
        return self.__warnings
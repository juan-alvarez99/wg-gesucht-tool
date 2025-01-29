import os
import sys

from modules import objects
from modules.notification_manager import NotificationManager
from modules.searcher import Searcher
from modules.links import links
from modules.sheet_manager import SheetManager
from modules.wg import WG
from modules.wg_manager import WgManager

if __name__ == '__main__':
    # Set up Chrome Driver
    searcher: Searcher = Searcher()
    with searcher.start():
        url = links["WG-GESUCHT"]
        filters: dict = objects.filters

        try:
            # Run a new search
            searcher.search_wgs(url, filters)
        except Exception as e:
            # Exits if the search can not be run
            sys.exit(1)

        # Gather the data from the search
        tracker: WgManager = WgManager(searcher.get_source())
        found_wgs: list[WG] = tracker.get_all_offers()

    # Get data from the Google Sheet
    sheet_manager: SheetManager = SheetManager()
    saved_wgs: list[WG] = sheet_manager.get_registered_wgs()

    # Send notification when a new WG is found
    email = os.environ["EMAIL"]
    password: str = os.environ["PASSWORD"]
    notification_manager: NotificationManager = NotificationManager(email, password)

    new_wgs: list[WG] = [wg for wg in found_wgs if wg not in saved_wgs]
    if new_wgs:
        notification_manager.send_email(new_wgs)
        sheet_manager.post_offers(new_wgs)

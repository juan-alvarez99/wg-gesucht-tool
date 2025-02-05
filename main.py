import os
import sys

from modules import objects
from modules.notification_manager import NotificationManager
from modules.searcher import Searcher
from modules.links import links
from modules.sheet_manager import SheetManager
from modules.types import LogStatus
from modules.wg import WG
from modules.wg_manager import WgManager


if __name__ == '__main__':
    # Set up Chrome Driver
    searcher: Searcher = Searcher()

    # Google Sheet manager
    sheet_manager: SheetManager = SheetManager()

    with searcher.start():
        url = links["WG-GESUCHT"]
        filters: dict = objects.filters

        try:
            # Run a new search
            searcher.search_wgs(url, filters)

            unapplied_filters: list[str] = searcher.get_unapplied_filters()
            if unapplied_filters:
                # Report if the search could be run with errors
                sheet_manager.add_warning(f"Could not apply all filters: {unapplied_filters}")

            # Gather the data from the search
            tracker: WgManager = WgManager(searcher.get_source())
            found_wgs: list[WG] = tracker.get_all_offers()

        except Exception as e:
            # Exit if the search could not be run
            sheet_manager.post_log(LogStatus.Error, f"Error while searching WGs: {e}")
            sys.exit(1)


    # Get data from the Google Sheet
    saved_wgs: list[WG] = sheet_manager.get_registered_wgs()

    # Send an email notification when new WGs are found
    email = os.environ["EMAIL"]
    password: str = os.environ["PASSWORD"]
    notification_manager: NotificationManager = NotificationManager(email, password)

    new_wgs: list[WG] = [wg for wg in found_wgs if wg not in saved_wgs]
    if new_wgs:
        try:
            notification_manager.send_email(new_wgs)
        except Exception as e:
            sheet_manager.post_log(LogStatus.Error, f"Could not send email: {e}")

        sheet_manager.post_offers(new_wgs)

    # Post status of the execution
    warnings = sheet_manager.get_warnings()
    log_status: LogStatus = LogStatus.Success
    log_msg: str = f"Total WGs found={len(found_wgs)}, new WGs found={len(new_wgs)}."
    if warnings:
        log_status = LogStatus.Warning
        log_msg += " ".join(warnings)

    sheet_manager.post_log(
            log_status,
            log_msg,
        )

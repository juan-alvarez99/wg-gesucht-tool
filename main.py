from modules import objects
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
        # Opens WG-Gesucht and apply filters
        searcher.search_wgs(url, filters)

        tracker: WgManager = WgManager(searcher.get_source())
        wgs: list[WG] = tracker.get_all_offers()

        sheet_manager: SheetManager = SheetManager()
        sheet_manager.post_offers(wgs)

from modules import objects
from modules.searcher import Searcher
from modules.links import links
from modules.wg_manager import WgManager

if __name__ == '__main__':
    # Set up Chrome Driver
    searcher: Searcher = Searcher()
    with searcher.start():
        url = links["WG-GESUCHT"]
        filters = objects.filters
        # Opens WG-Gesucht and apply filters
        searcher.search_wgs(url, filters)

        tracker = WgManager(searcher.get_source())
        wgs = tracker.get_all_offers()

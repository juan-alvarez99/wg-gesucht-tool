from modules.navigator import Navigator
from modules.links import links
from modules.wg_tracker import WgTracker

if __name__ == '__main__':
    tracker = WgTracker(links["WG-GESUCHT"])
    offers = tracker.get_all_offers()
    tracker.parse_data(offers)
    # Fills the Google form with the data found
    navigator: Navigator = Navigator()
    with navigator.start() as nav:
        nav.get(links["WG-GESUCHT"])
        pass



from modules.navigator import Navigator
from modules.links import links


if __name__ == '__main__':
    # Fills the Google form with the data found
    navigator: Navigator = Navigator()
    with navigator.start() as nav:
        nav.get(links["WG-GESUCHT"])
        pass



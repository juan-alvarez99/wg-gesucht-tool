from modules.navigator import Navigator
from modules.links import links

if __name__ == '__main__':
    # Set up Chrome Driver
    navigator: Navigator = Navigator()
    with navigator.start():
        # Opens WG-Gesucht and apply filters
        navigator.search_wg(links["WG-GESUCHT"])

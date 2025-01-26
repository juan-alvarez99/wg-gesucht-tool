import json

class WG:
    def __init__(self, title: str, size: int, rent: int, link: str):
        self.title: str = title
        self.size: int = size
        self.rent: int = rent
        self.link: str = link

    def get_data_as_json(self) -> json:
        return json.dumps({
            "title": self.title,
            "size": self.title,
            "rent": self.rent,
            "link": self.link,
        })

class WG:
    def __init__(self, title: str, size: int, rent: int, link: str):
        self.title: str = title
        self.size: int = size
        self.rent: int = rent
        self.link: str = link

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, WG):
            return self.link == other.link
        return False

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

    def __str__(self):
        return f"{self.title} \t {self.rent}€ \t {self.size}m2 \t {self.link}"
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "size": self.size,
            "rent": self.rent,
            "link": self.link,
        }

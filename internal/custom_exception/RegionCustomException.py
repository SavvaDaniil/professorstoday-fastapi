

class RegionNotFoundException(Exception):
    def __init__(self):
        super().__init__("Region not found")
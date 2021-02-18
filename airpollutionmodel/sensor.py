class Sensor:
    def __init__(self, latitude, longitude, dist_from_road):
        self.latitude = latitude
        self.longitude = longitude
        self.dist_from_road = dist_from_road
        self.readings = dict()
    
    def as_JSON:
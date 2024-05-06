class EdgeStreet:
    def __init__(self, origin, destiny, capacity, min_percent_time, num_vehicle=0):
        self.origin = origin
        self.destiny = destiny
        self.capacity = capacity
        self.min_percent_time = min_percent_time
        self.num_vehicle = num_vehicle


    def to_dict(self):
        return {
            "origin": self.origin,
            "destiny": self.destiny,
            "capacity": self.capacity,
            "min_percent_time": self.min_percent_time,
            "num_vehicle": self.num_vehicle
        }

    @classmethod
    def from_dict(cls, data):
        edge: EdgeStreet = cls(data["origin"], data["destiny"], data["capacity"], data["min_percent_time"], data["num_vehicle"])
        return edge

    def __str__(self):
        return f"Origin: {self.origin}, Destination: {self.destiny}, Capacity: {self.capacity}, MinPercentTime: {self.min_percent_time}"
class EdgeStreetGene(object):

    def __init__(self, origin, destiny, capacity, min_percent_time, num_vehicle=0):
        self.origin = origin
        self.destiny = destiny
        self.capacity = capacity
        self.min_percent_time = min_percent_time
        self.num_vehicle = num_vehicle  # NUMEOR DE VEHICULOS ESTO ES PARA LAS ENTRADAS
        self.current_percentage = 0.0   # % DE TIEMPO ACTUAL, EL QUE SE LE ASIGNO A ESTA CALLE
        self.arrivals = 0   # LLEGADAS
        self.departures = 0     # SALIDAS
        self.in_line = 0    # EN COLA

    def add_in_line(self, num_vehicle):
        self.in_line += num_vehicle

    def reset_data(self):
        self.arrivals = 0  # LLEGADAS
        self.departures = 0  # SALIDAS
        self.in_line = 0  # EN COLA

    def __str__(self):
        return f"Origin: {self.origin}, Destination: {self.destiny}, Capacity: {self.capacity}, min_percent_time: {self.min_percent_time}, current percentage: {self.current_percentage}, in_line: {self.in_line}"

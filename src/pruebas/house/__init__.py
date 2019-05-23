
class House:

    num_vents = 0
    square_meters = 0

    def __init__(self, num=0, metros=0):
        self.num_vents = num
        self.square_meters = metros

    def get_num_vents(self):
        return self.num_vents

    def get_square_meters(self):
        return self.square_meters


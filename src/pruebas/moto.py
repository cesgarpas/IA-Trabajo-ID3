

class Moto():

    wheels = None
    speed = None

    def __init__(self, wheels=2, speed=60):
        self.wheels=wheels
        self.speed=speed

    def get_wheels(self):
        return self.wheels

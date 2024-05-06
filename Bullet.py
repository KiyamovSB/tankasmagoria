class Bullet:
    def __init__(self, pos_x, pos_y, size_x, size_у, color, face, name):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.face = face
        self.size_x = size_x
        self.size_y = size_у
        self.speed = 20
        self.name = name
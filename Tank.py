import random
import Bullet


class Tank:
    def __init__(self, pos_x, pos_y, size_x, size_у, color, face, name, instruction_name):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.face = face
        self.size_x = size_x
        self.size_y = size_у
        self.health = 1
        self.speed = 1
        self.shot_speed = 10
        self.name = name
        self.instruction_name = instruction_name
        self.instructions = []

    def play_w_instruction(self, field):
        if len(self.instructions) == 0:
            self.instructions = self.read_instructions()
        self.run_instruction(self.instructions[0], field)
        self.instructions.pop(0)


    def read_instructions(self):
        instruction_name = self.instruction_name
        with open(instruction_name, 'r',  encoding="utf-8") as file:
            instruction = file.read()

        instruction = instruction.replace("если", "if")
        instruction = instruction.replace("иначе", "else")
        instruction = instruction.replace("вижу_танк", "self.is_tank_ahead(field)")
        instruction = instruction.replace("стрелять", "self.shot(field)")
        instruction = instruction.replace("стена", "self.is_wall(field)")
        instruction = instruction.replace("вперед", "self.go_ahead(field)")
        instruction = instruction.replace("направо", "self.go_right()")
        instruction = instruction.replace("налево", "self.go_left()")
        instruction = instruction.replace("случайно", "self.go_random()")

        instructions = [line for line in instruction.split('\n') if '#' not in line]

        return instructions

    def run_instruction(self, instruction, field):
        exec(instruction)

    def is_tank_ahead(self, field):
        flag = False
        for tank in field.tanks:
            if self.face == 'south':
                if self.pos_x <= (tank.pos_x + tank.size_x) and (self.pos_x + self.size_x) >= tank.pos_x and (self.pos_y + self.size_y) <= tank.pos_y:
                    flag = True
                    break
            elif self.face == 'north':
                if self.pos_x <= (tank.pos_x + tank.size_x) and (self.pos_x + self.size_x) >= tank.pos_x and self.pos_y >= (tank.pos_y + tank.size_y):
                    flag = True
                    break
            elif self.face == 'east':
                if self.pos_y <= (tank.pos_y + tank.size_y) and (self.pos_y + self.size_y) >= tank.pos_y and (self.pos_x + self.size_x) <= tank.pos_x:
                    flag = True
                    break
            elif self.face == 'west':
                if self.pos_y <= (tank.pos_y + tank.size_y) and (self.pos_y + self.size_y) >= tank.pos_y and self.pos_x >= tank.pos_x + tank.size_x:
                    flag = True
                    break
        return flag

    def shot(self, field):
        bullet = Bullet.Bullet(pos_x = self.pos_x + self.size_x/2,
                               pos_y = self.pos_y + self.size_y/2,
                               size_x = field.pixel,
                               size_у = field.pixel,
                               color = field.ORANGE,
                               face = self.face,
                               name = self.name)
        field.bullets.append(bullet)
        field.sound_shot.play()

    def is_wall(self, field):
        flag = False
        if self.face == 'south':
            if self.pos_y + self.size_y >= field.big_y:
                flag = True
        elif self.face == 'north':
            if self.pos_y <= 0:
                flag = True
        elif self.face == 'east':
            if self.pos_x + self.size_x >= field.big_x:
                flag = True
        elif self.face == 'west':
            if self.pos_x <= 0:
                flag = True
        return flag

    def go_ahead(self, field):
        if not self.is_wall(field):
            if self.face == 'south':
                self.pos_y += field.pixel
            elif self.face == 'north':
                self.pos_y -= field.pixel
            elif self.face == 'east':
                self.pos_x += field.pixel
            elif self.face == 'west':
                self.pos_x -= field.pixel

    def go_right(self):
        if self.face == 'south':
            self.face = 'east'
        elif self.face == 'north':
            self.face = 'west'
        elif self.face == 'east':
            self.face = 'north'
        elif self.face == 'west':
            self.face = 'south'

    def go_left(self):
        if self.face == 'south':
            self.face = 'west'
        elif self.face == 'north':
            self.face = 'east'
        elif self.face == 'east':
            self.face = 'south'
        elif self.face == 'west':
            self.face = 'north'

    def go_random(self):
        if random.choice([True, False]):
            self.go_left()
        else:
            self.go_right()


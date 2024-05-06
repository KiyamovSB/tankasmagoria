import pygame
import sys
import time
import Field
import Tank
import yaml


def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def create_tanks():
    data = read_yaml_file('tanks.yml')
    for tank in data['tanks']:
        new_tank = Tank.Tank( name = tank['name'],
                              face = tank['face'],
                              color = tank['color'],
                              pos_x = field.small_x * tank['pos_x'],
                              pos_y = field.small_y * tank['pos_y'],
                              instruction_name = tank['instruction_name'],
                              size_x = field.small_x,
                              size_у = field.small_y)

        field.tanks.append(new_tank)


def draw_tanks(tanks):
    for tank in tanks:
        pygame.draw.rect(screen, tank.color, (tank.pos_x, tank.pos_y, tank.size_x, tank.size_y))


def draw_lines():
    num_lines = 10
    for i in range(num_lines):
        x = i * field.small_x
        pygame.draw.line(screen, field.GREEN, (x, 0), (x, field.big_x), 1)
        pygame.draw.line(screen, field.GREEN, (0, x), (field.big_y, x), 1)


def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, bullet.color, (bullet.pos_x, bullet.pos_y, bullet.size_x, bullet.size_y))


def draw_faces(tanks):
    for tank in tanks:
        if tank.face == 'south':
            pygame.draw.rect(screen, field.WHITE, (tank.pos_x + field.pixel * 5, tank.pos_y + field.pixel * 5, field.pixel, field.pixel * 7))
        elif tank.face == 'east':
            pygame.draw.rect(screen, field.WHITE, (tank.pos_x + field.pixel * 5, tank.pos_y + field.pixel * 5, field.pixel * 7, field.pixel))
        elif tank.face == 'north':
            pygame.draw.rect(screen, field.WHITE, (tank.pos_x + field.pixel * 5, tank.pos_y - field.pixel * 3, field.pixel,  field.pixel * 7))
        elif tank.face == 'west':
            pygame.draw.rect(screen, field.WHITE, (tank.pos_x - field.pixel * 3, tank.pos_y + field.pixel * 5, field.pixel * 7, field.pixel))


def run_bullets(bullets):
    for bullet in bullets:
        if bullet.face == 'south':
            bullet.pos_y += bullet.speed
        elif bullet.face == 'east':
            bullet.pos_x += bullet.speed
        elif bullet.face == 'north':
            bullet.pos_y -= bullet.speed
        elif bullet.face == 'west':
            bullet.pos_x -= bullet.speed


def check_shots(tanks, bullets, explode_color):
    for tank in tanks:
        for bullet in bullets:
            if (bullet.name != tank.name
                and bullet.pos_y >= tank.pos_y
                and bullet.pos_y <= tank.pos_y + tank.size_y
                and bullet.pos_x >= tank.pos_x
                and bullet.pos_x <= tank.pos_x + tank.size_x):
                    explode(tank, bullet, explode_color)


def play_w_instructions(tanks):
    for tank in tanks:
        tank.play_w_instruction(field)


def explode(tank, bullet, explode_color):
    pygame.draw.rect(screen, field.ORANGE, (tank.pos_x, tank.pos_y, tank.size_x, tank.size_y))
    #delete tank
    field.tanks = [t for t in field.tanks if t.name != tank.name]
    field.sound_explode.play()


# Инициализация Pygame
pygame.init()
field = Field.Field(pygame)

# Установка размеров окна
pygame.display.set_caption("1en")
screen = pygame.display.set_mode((field.big_x, field.big_y))

create_tanks()

# Главный игровой цикл
running = True
is_sound_win_played = False
while running:
    screen.fill(field.BLACK)
    draw_lines()

    if len(field.tanks) == 1:
        winner_name = field.tanks[0].name
        font = pygame.font.Font(None, 56)
        text = font.render(winner_name + " wins!", True, field.ORANGE)
        screen.blit(text, (field.big_x // 2 - text.get_width() // 2, field.big_y // 2 - text.get_height() // 2))
        pygame.display.flip()

        if not is_sound_win_played:
            field.sound_win.play()
            is_sound_win_played = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_tanks(field.tanks)
    draw_faces(field.tanks)

    play_w_instructions(field.tanks)
    run_bullets(field.bullets)
    draw_bullets(field.bullets)
    check_shots(tanks = field.tanks, bullets = field.bullets, explode_color = field.ORANGE)

    pygame.display.flip()
    time.sleep(0.1)


pygame.quit()
sys.exit()

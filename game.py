import pygame as pg
from random import randint as rnd
"""Основной код игры"""

SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600
BACKGROUN_COLOR = (0, 0, 0)
FPS = 60

DEFAULT_PLAYER_POS = (SCREEN_WIDTH // 2, 550)
PLAYER_COLOR = (0, 200, 64)

BULLET_SPEED = 15
BULLET_COLOR = (255, 0, 0)

ENEMY_COLOR = (210, 105, 30)
ENEMY_SIZE = 40
ENEMY_MIN_SPEED = 1
ENEMY_MAX_SPEED = 5

pg.init()
window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH), 0, 32)
pg.display.set_caption('Игрушка')
clock = pg.time.Clock()
pg.mouse.set_visible(False)

bullets = []
enemies = []


class Player:
    def __init__(self,
                 position=DEFAULT_PLAYER_POS,
                 body_color=PLAYER_COLOR):
        self.px, self.py = position
        self.body_color = body_color
        self.shot_speed = 15

    def update(self, position):
        self.shot_speed += 1
        mx, _ = position
        if (mx - self.px) != 0:
            self.px += int((mx - self.px) * 0.05)
        if self.px < 30:
            self.px = 30
        elif self.px > 770:
            self.px = 770

    def draw(self, surf):
        pg.draw.circle(surf,
                       self.body_color,
                       (self.px, self.py),
                       30)
        pg.draw.line(surf,
                     self.body_color,
                     (self.px, self.py),
                     (self.px, self.py - 45),
                     15)

    def shot(self):
        if self.shot_speed % FPS > 15:
            self.shot_speed = 0
            Bullet((self.px, self.py - 45))


class Bullet:
    def __init__(self,
                 position,
                 bullet_color=BULLET_COLOR,
                 speed=BULLET_SPEED):
        bullets.append(self)
        self.px, self.py = position
        self.body_color = bullet_color
        self.speed = speed

    def update(self):
        self.py -= self.speed
        if self.py < 0:
            bullets.remove(self)

    def draw(self, surf):
        pg.draw.circle(surf, self.body_color, (self.px, self.py), 3)


class Enemy:
    def __init__(self, body_color=ENEMY_COLOR):
        self.px, self.py = rnd(30, 770), -100
        self.speed = rnd(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.color = body_color
        self.rect = pg.Rect(self.px, self.py, ENEMY_SIZE, ENEMY_SIZE)
        enemies.append(self)

    def update(self):
        self.py += self.speed
        if self.py > SCREEN_HEIGTH:
            enemies.remove(self)
        for bullet in bullets:
            if (self.px <= bullet.px <= (self.px + ENEMY_SIZE) and
                self.py <= bullet.py <= (self.py + ENEMY_SIZE)):
                enemies.remove(self)
                bullets.remove(bullet)

    def draw(self, surf):
        pg.draw.rect(surf, self.color, (self.px, self.py, 40, 40))


def run():
    play = True
    timer = 0
    player = Player()
    while play:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                play = False
                pg.quit()
                raise SystemExit

        window.fill(BACKGROUN_COLOR)
        pg.draw.rect(window, (224, 255, 255), (0, 550, 800, 150))
        
        timer += 1
        if timer % 60 == 0:
            Enemy()
        for enemy in enemies:
            enemy.update()
            enemy.draw(window)

        player.update(pg.mouse.get_pos())
        player.draw(window)
        if pg.mouse.get_pressed()[0]:
            player.shot()

        for bullet in bullets:
            bullet.update()
            bullet.draw(window)

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    run()

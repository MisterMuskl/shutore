#Создай собственный Шутер!

from pygame import *
from random import randint
import os
import time as tm

win_widht = 700
win_hight = 500
window = display.set_mode((win_widht, win_hight))
display.set_caption('Maze')
backgr = transform.scale(image.load('galaxy.jpg'),(win_widht, win_hight))

mixer.init()

reolad_time = 2
schet = 0
monsters = sprite.Group()
bullets = sprite.Group()
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, p_x, p_y, s_w, s_h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (s_w, s_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('asteroid.png', self.rect.centerx, self.rect.top, 30, 30, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            global schet 
            schet += 1
            self.rect.y = -100
            self.rect.x = randint(0, 600)
            self.speed = randint(1,2)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

avtomat = Player('bullet.png', 310, 400, 100, 80, 10)
for _ in range(5):
    musor = Enemy('rocket.png', randint(0,600), -100, 100, 100, randint(1,2))
    monsters.add(musor)


finish = False
game = True
clock = time.Clock()
font.init()
font2 = font.SysFont('Arial', 50)
shot = 0
vistrel = 0
reloads = False
start_time = tm.time()

while game:
    end_time = tm.time()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not reloads:
                avtomat.fire()  
                vistrel += 1
    if not finish:
        window.blit(backgr, (0,0))
        avtomat.update()
        avtomat.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        text_lose = font2.render('Пропущено:' + str(schet), 1, (255,255,255))
        window.blit(text_lose, (10,10))
        text_shot = font2.render('Счёт:' + str(shot), 1, (255,255,255))
        window.blit(text_shot, (10,50))
        if sprite.spritecollide(avtomat, monsters, False):
            finish = True
            l = font2.render('hihihiha', 1, (255,255,255))
            window.blit(l, (250,300))
        if sprite.groupcollide(monsters, bullets, True, True):
            musor = Enemy('rocket.png', randint(0,600), -100, 100, 100, randint(1,2))
            monsters.add(musor)
            shot += 1
        if schet >= 3:
            finish = True
            l = font2.render('hihihiha', 1, (255,255,255))
            window.blit(l, (250,300))
        if shot >= 10:
            finish = True
            w = font2.render('You win', 1, (255,255,255))
            window.blit(w, (250,300))
        if vistrel == 5 and not reloads:
            reloads = True
            start_time = tm.time()
        if reloads:
            end_time = tm.time()
            if end_time - start_time > reolad_time:
                reloads = False
                vistrel = 0

    display.update()
    clock.tick(60)  
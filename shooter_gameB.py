#Створи власний Шутер!
import time
from random import randint

from pygame import *
font.init()
font1=font.Font(None,80)
win = font1.render("YOU WIN",True,(255,255,255))
lose = font1.render("YOU LOSE",True,(180,0,0))
font2=font.Font(None,36)

window = display.set_mode((700,500))

display.set_caption("Shuter")
backgoround = transform.scale(image.load("galaxy.jpg"), size = (700,500))
img_monster = "ufo.png"
img_hero = "rocket.png"
fire1 = "bullet.png"
asteroid = "asteroid.png"
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image , dest=(self.rect.x , self.rect.y))

win_width = 700
win_height = 500

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <win_width -80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(fire1, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80 )
            self.rect.y = 0
            lost = lost+1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

monsterts = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_monster,randint(80,win_width - 80), -40,80,50,randint(1,1))
    monsterts.add(monster)

asteroids = sprite.Group()
for a in range(1,2):
    asteroidd =Enemy(asteroid,randint(80,win_width - 80), -40,80,50,randint(1,1))
    asteroids.add(asteroidd)


ship = Player(img_hero , 5 , win_height - 100 , 80 ,100, 10)
finish = False

FPS = 60

game = True
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load("space.ogg")
#mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

max_lost = 10
goal =2
score = 0
lost = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type ==KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:

        window.blit(backgoround, dest =(0,0))
        text = font2.render("Рахунок" + str(score), 1 ,(255,255,255))
        text_lose = font2.render("Пропущено:" + str(lost) , 1 ,(255,255,255))
        window.blit(text_lose,(10,50))
        window.blit(text, (10, 20))
        ship.reset()
        ship.update()

        monsterts.draw(window)
        monsterts.update()

        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()

        collides = sprite.groupcollide(monsterts,bullets,True,True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_monster, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))

            monsterts.add(monster)
        if sprite.spritecollide(ship,monsterts,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            window.blit(window,(200,200))

        if sprite.spritecollide(ship,asteroids,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))



        display.update()
    clock.tick(FPS)
    
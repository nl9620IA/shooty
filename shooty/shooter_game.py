from pygame import *
from random import randint

score = 0
lost = 0

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN! :)', True, (255, 255, 255))
lose = font1.render('YOU LOSE! ;(', True, (180, 40, 0))

font.init()
font2 = font.Font(None, 36)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = '1569315189_content_700x455.jpg'
img_hero = '73455677_0_3eeac_259bc4d5_XL.png'
img_enemy = 'image_processing20221201-29574-bb9q1h.png'
img_bullet = '2_50.png'
score = 0
goal = 11
lost = 0
max_lost = 5

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

win_width = 700
win_height = 800
display.set_caption("тут игра")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("1569315189_content_700x455.jpg"), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 65, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 50, randint(1, 4))
    monsters.add(monster)

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:         
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background,(0,0))

        text = font2.render('Убито: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 90))

        text_lose = font2.render('Пропущено черьвей: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


    time.delay(20)
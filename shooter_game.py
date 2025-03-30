from pygame import*
from random import randint

img_back = 'planet.jpg'
img_hero = 'rocket.jpg'
img_enemy = 'ufo.png'

window = display.set_mode((700,500))
display.set_caption('Расфигачить зелёных псин')

background = transform.scale(image.load('planet.jpg'), (700,500))
width = 700
height = 500

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 30)

font2 = font.SysFont('Arial', 60)

win = font2.render('Ты победил!', True, (178, 56, 239))
lose = font2.render('Ты проиграл!', True, (178, 56, 239))
bullets = sprite.Group()

max_enemy = 10
max_collide = 5     

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()                                                                                                                  
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def go(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x  < width - 60:
            self.rect.x += self.speed
    def attack(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet) 

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


hero = Player('rocket.png', 10, height - 100, 40, 80, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

FPS = 60
clock = time.Clock()
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                hero.attack()
    if not finish:
        window.blit(background, (0,0))
        text = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        hero.go()
        monsters.update()
        hero.reset()
        bullets.draw(window)
        monsters.draw(window)
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(hero, monsters, False) or lost >= 3:
            finish = True
            window.blit(lose, (200,200))

        if score >= max_enemy:
            finish = True
            window.blit(win, (200,200))

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
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

    clock.tick(FPS)
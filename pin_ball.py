import pygame, sys, random, math
from pygame.locals import *

# Инициализация
pygame.init()
W, H = 800, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("PinBall")

# Загрузка изображений
try: bg = pygame.transform.scale(pygame.image.load('istockphoto-904853290-612x612.jpg'), (W, H))
except: bg = pygame.Surface((W, H)); bg.fill((50, 50, 100))
ball_img = pygame.transform.scale(pygame.image.load('toy-tennis-ball-icon-isolated_24877-83065.png'), (30, 30))
paddle_img = pygame.transform.scale(pygame.image.load('Безымянный-Photoroom.png'), (15, 100))

# Классы
class Paddle:
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.speed = 5
    def move(self, dy):
        self.rect.y = max(0, min(H - self.rect.height, self.rect.y + dy * self.speed))

class Ball:
    def __init__(self):
        self.img = ball_img
        self.rect = self.img.get_rect(center=(W//2, H//2))
        self.dx, self.dy = random.choice([-4,-3,3,4]), random.choice([-4,-3,3,4])
    def move(self):
        self.rect.x += self.dx; self.rect.y += self.dy
        if self.rect.top <= 0 or self.rect.bottom >= H: self.dy *= -1
        if self.rect.right < 0 or self.rect.left > W: return True
        return False
    def collide(self, paddle):
        if self.rect.colliderect(paddle.rect):
            bounce = (paddle.rect.centery - self.rect.centery) / (paddle.rect.height/2)
            self.dx *= -1; self.dy = -5 * -math.sin(bounce * (5*math.pi/12))

# Объекты
left = Paddle(30, H//2-50, paddle_img)
right = Paddle(W-45, H//2-50, pygame.transform.flip(paddle_img, True, False))
ball = Ball()
font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()
game_over = False

# Главный цикл
while True:
    for e in pygame.event.get():
        if e.type == QUIT: pygame.quit(); sys.exit()
        if e.type == KEYDOWN and e.key == K_r and game_over: ball = Ball(); game_over = False
    
    if not game_over:
        keys = pygame.key.get_pressed()
        left.move(keys[K_s] - keys[K_w])
        right.move(keys[K_DOWN] - keys[K_UP])
        game_over = ball.move()
        ball.collide(left); ball.collide(right)
    
    screen.blit(bg, (0, 0))
    screen.blit(left.img, left.rect); screen.blit(right.img, right.rect); screen.blit(ball.img, ball.rect)
    if game_over:
        screen.blit(font.render("GAME OVER", 1, (255,0,0)), (W//2-150, H//2-50))
        screen.blit(font.render("Press R to restart", 1, (0,195,255)), (W//2-180, H//2+50))
    
    pygame.display.flip()
    clock.tick(60)
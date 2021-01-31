import pygame
import os
import sys
import random

pygame.init()

HIGH_SCORES = []
bg_x_pos = 0
bg_y_pos = 380

HEIGHT = 600
WIDTH = 1100
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

RUNNING = [pygame.image.load(os.path.join('Assets','Dino','DinoRun1.png')),pygame.image.load(os.path.join('Assets','Dino','DinoRun2.png'))]
JUMP = [pygame.image.load(os.path.join('Assets','Dino','DinoJump.png'))]
DUCKING = [pygame.image.load(os.path.join('Assets','Dino','DinoDuck1.png')),pygame.image.load(os.path.join('Assets','Dino','DinoDuck2.png'))]

S_CACTUS = [pygame.image.load(os.path.join('Assets','Cactus','SmallCactus1.png')),
            pygame.image.load(os.path.join('Assets', 'Cactus','SmallCactus2.png')),
            pygame.image.load(os.path.join('Assets','Cactus','SmallCactus3.png'))]
L_CACTUS = [pygame.image.load(os.path.join('Assets','Cactus','LargeCactus1.png')),
            pygame.image.load(os.path.join('Assets', 'Cactus', 'LargeCactus2.png')),
            pygame.image.load(os.path.join('Assets','Cactus','LargeCactus3.png'))]

FLYING_DINO = [pygame.image.load(os.path.join('Assets','Flying','Flying1.png')),pygame.image.load(os.path.join('Assets','Flying','Flying2.png'))]

CLOUD = pygame.image.load(os.path.join('Assets','Other','Cloud.png'))

BACKGROUND = pygame.image.load((os.path.join('Assets','Other','Track.png')))

class Dinosaur:
    x_pos = 80
    y_pos = 310
    y_duck_pos = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMP

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.jump_vel = self.JUMP_VEL

        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect() # get rect around the image
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos

    def update(self,keys_pressed):
        if self.dino_duck:
            self.duck()
        if self.dino_jump:
            self.jump()
        if self.dino_run:
            self.run()

        if self.step_index >= 10:
            self.step_index = 0

        if keys_pressed[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_jump = True
            self.dino_run = False
        if keys_pressed[pygame.K_DOWN] and not self.dino_jump:
            self.dino_jump = False
            self.dino_duck = True
            self.dino_run = False
        elif not (self.dino_jump or keys_pressed[pygame.K_DOWN]) :
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_duck_pos
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index// 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img[0]
        if self.dino_jump:        # good jump function
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self,WIN):
        WIN.blit(self.image,(self.dino_rect.x,self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(800,1000)
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.Width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < - self.Width:
            self.x = WIDTH + random.randint(800,1000)
            self.y = random.randint(50,100)

    def draw(self,WIN):
        WIN.blit(self.image,(self.x,self.y))

class Obstacle:
    def __init__(self,image,type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            Obstacles.pop()

    def draw(self,WIN):
        WIN.blit(self.image[self.type],self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class FlyingDino(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self,WIN):
        if self.index >= 9:
            self.index = 0
        WIN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():

    global game_speed,points,Obstacles
    game_speed = 14
    points = 0
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    points = 0
    Obstacles = []
    death_count = 0

    font = pygame.font.Font('freesansbold.ttf',20)

    def score():
        global points ,game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points),1,(0,0,0))
        textrect = text.get_rect()
        textrect.center = (1000,40)
        WIN.blit(text,textrect)

    def background():
        global bg_x_pos,bg_y_pos
        image_width = BACKGROUND.get_width()
        WIN.blit(BACKGROUND,(bg_x_pos,bg_y_pos))
        WIN.blit(BACKGROUND,(image_width + bg_x_pos,bg_y_pos))
        if bg_x_pos <= -image_width:
            WIN.blit(BACKGROUND,(image_width + bg_x_pos,bg_y_pos))
            bg_x_pos = 0
        bg_x_pos -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        WIN.fill((255,255,255))
        cloud.draw(WIN)
        cloud.update()
        background()
        score()

        if len(Obstacles) == 0:
            if random.randint(0,2) == 0:
                Obstacles.append(SmallCactus(S_CACTUS))
            if random.randint(0, 2) == 1:
                Obstacles.append(LargeCactus(L_CACTUS))
            if random.randint(0, 3) == 2:
                Obstacles.append(FlyingDino(FLYING_DINO))

        for obstacle in Obstacles:
            obstacle.draw(WIN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        keys_pressed = pygame.key.get_pressed()
        player.draw(WIN)
        player.update(keys_pressed)

        clock.tick(40)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        WIN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            HIGH_SCORES.append(points)
            h_score = font.render("Highest Score: " + str(max(HIGH_SCORES)), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (WIDTH // 2, HEIGHT // 2 + 50)
            h_scoreRect = h_score.get_rect()
            h_scoreRect.center = (WIDTH // 2, HEIGHT // 2 + 150)
            WIN.blit(score, scoreRect)
            WIN.blit(h_score,h_scoreRect)
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        WIN.blit(text, textRect)
        WIN.blit(RUNNING[0], (WIDTH // 2 - 20, HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)

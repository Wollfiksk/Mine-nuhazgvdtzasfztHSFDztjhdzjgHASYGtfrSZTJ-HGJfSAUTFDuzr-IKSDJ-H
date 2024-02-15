import pygame
import sys
import random

pygame.init()
pygame.font.init()

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)

# Player variables
playerx = 20
playery = 440
velikostx = 40
velikosty = 50
gravity = 5
jump_count = 10
is_jumping = False

# Obstacle variables
speed_increase_interval = 5  # Increase speed every 5 obstacles

class Obstacle:
    def __init__(self, skore):
        self.reset(skore)

    def reset(self, skore):
        self.width = 50
        self.height = random.randint(50, 200)
        self.x = 800
        self.y = (550 - self.height)
        self.speed = 0.3 + skore // speed_increase_interval * 0.1  # Increase speed over time

    def update(self, player_x, player_y, skore):
        self.x -= self.speed
        if self.x < -self.width:
            self.reset(skore)
            return False

obstacles = [Obstacle(0) for _ in range(5)]

# Other variables
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 40)
esc = False
skore = 0

# Main game loop
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_ESCAPE:
                esc = not esc

    if not esc:
        stisknute_klavesy = pygame.key.get_pressed()
        okno.fill((0, 0, 0))

        pygame.draw.rect(okno, (255, 255, 255), (playerx, playery, velikostx, velikosty))

        for obstacle in obstacles:
            if obstacle.update(playerx, playery, skore):
                print("Game Over!")
                obstacles = [Obstacle(skore) for _ in range(5)]
                skore = 0

        fps = str(int(clock.get_fps()))
        fps_t = font.render(fps, 1, pygame.Color("RED"))
        okno.blit(fps_t, (0, 0))

        clock.tick(100)
        skore += 0.01
        if playery < 440:
            on_ground = False
        else:
            on_ground = True
            playery = 440

        if stisknute_klavesy[pygame.K_SPACE]:
            if not is_jumping and on_ground:
                is_jumping = True

        if is_jumping:
            if jump_count >= -15:
                neg = 1
                if jump_count < 0:
                    neg = -1
                playery -= 12
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 15

        playery += gravity

        for obstacle in obstacles:
            pygame.draw.rect(okno, (255, 0, 0), (obstacle.x, obstacle.y, obstacle.width, obstacle.height))

        txtimg = font2.render("Skore: " + str(skore), True, (0, 0, 0))
        okno.blit(txtimg, (600, 0))

        pygame.display.update()

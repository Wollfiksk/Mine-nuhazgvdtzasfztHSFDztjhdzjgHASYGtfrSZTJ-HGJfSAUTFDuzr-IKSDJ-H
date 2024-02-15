import pygame
import sys
import random

pygame.init()
pygame.font.init()

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)

randoms = random.randint(50, 500)
pozice_micku_y = randoms
pozice_micku_x = 400
velikost_micku = 50
randoms2 = random.randint(1, 2)
if randoms2 == 1:
    rychlost_micku_x = 0.3
if randoms2 == 2:
    rychlost_micku_x = -0.3
rychlost_micku_y = 0.3

velikost_hrace_vyska = 150
velikost_hrace_sirka = 50

pozice_hrace_x = 10
pozice_hrace_y = 300
rychlost_hrace = 0.6

velikost_hrace_vyska2 = 150
velikost_hrace_sirka2 = 50

clock = pygame.time.Clock()

playerx = 20
playery = 440
velikostx = 40
velikosty = 50

gravity = 5  # Reduced gravity

button_rect2 = pygame.Rect(300, 200, 200, 100)
button_rect = pygame.Rect(300, 330, 200, 100)
button_color = (100, 100, 100)
click_color = (100, 100, 100)

jump_count = 10
is_jumping = False

font = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 40)
esc = False

skore = 0

jo = False
jo2 = False
fps = str(int(clock.get_fps()))

spawn_time = 0
spawn_interval = 1.0  # Initial spawn interval (in seconds)
speed_increase_interval = 10  # Increase speed every 10 obstacles

class Obstacle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 800
        self.y = random.randint(0, 600 - 50)
        self.width = 50
        self.height = 50
        self.speed = 0.3 + skore // speed_increase_interval * 0.1  # Increase speed over time

    def update(self, player_x, player_y):
        self.x -= self.speed
        if self.x < -self.width:
            self.reset()
            return False
        if (
            self.x < player_x
            and self.x + self.width > player_x
            and self.y < player_y
            and self.y + self.height > player_y
        ):
            return True
        return False

obstacles = []
for i in range(5):
    obstacles.append(Obstacle())

while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_ESCAPE:
                esc = not esc
        elif udalost.type == pygame.MOUSEBUTTONDOWN:
            if udalost.button == 1:
                if button_rect.collidepoint(udalost.pos):
                    print("reset")
                    obstacles = []
                    for i in range(5):
                        obstacles.append(Obstacle())
                    skore = 0
        elif udalost.type == pygame.MOUSEBUTTONDOWN:
            if udalost.button == 1:
                if button_rect2.collidepoint(udalost.pos):
                    print("Quited")
                    soubor2 = open("Save.txt", "w", encoding="utf-8")
                    soubor2.write(str(skore))
                    soubor2.close()
                    pygame.quit()
                    sys.exit()

    if not esc:
        stisknute_klavesy = pygame.key.get_pressed()
        okno.fill((0, 0, 0))

        direction = pygame.Vector2(playerx, playery)
        pygame.draw.rect(okno, (255, 255, 255), (playerx, playery, velikostx, velikosty))

        for obstacle in obstacles:
            if obstacle.update(playerx, playery):
                print("Game Over!")
                obstacles = []
                for i in range(5):
                    obstacles.append(Obstacle())
                skore = 0

        fps = str(int(clock.get_fps()))
        fps_t = font.render(fps, 1, pygame.Color("RED"))
        okno.blit(fps_t, (0, 0))

        clock.tick(100)

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

        spawn_time += clock.get_rawtime() / 1000.0  # Convert raw time to seconds
        if spawn_time > spawn_interval:
            obstacles.append(Obstacle())
            spawn_time = 0

        for obstacle in obstacles:
            pygame.draw.rect(okno, (255, 0, 0), (obstacle.x, obstacle.y, obstacle.width, obstacle.height))

        txtimg = font2.render("Skore: " + str(skore), True, (0, 0, 0))
        okno.blit(txtimg, (600, 0))

        pygame.display.update()

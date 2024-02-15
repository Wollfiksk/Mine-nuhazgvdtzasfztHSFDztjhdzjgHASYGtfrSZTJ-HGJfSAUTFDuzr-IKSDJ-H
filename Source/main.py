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
jump_count = 15
is_jumping = False

# Other variables
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 40)
esc = False

skore = 0

button_rect2 = pygame.Rect(300, 200, 200, 100)
button_rect = pygame.Rect(300, 330, 200, 100)
button_color = (100, 100, 100)
click_color = (100, 100, 100)

def draw_button(rect, color, text):
    pygame.draw.rect(okno, color, rect)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    okno.blit(text_surface, text_rect)

def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps, 1, pygame.Color("RED"))
    okno.blit(fps_t, (0, 0))

def reset_game():
    global skore
    skore = 0

class Obstacle:
    def __init__(self, skore):
        self.reset(skore)

    def reset(self, skore):
        self.width = 50
        self.height = random.randint(50, 200)
        self.x = 800
        self.y = (550 - self.height)
        self.speed = 0.3 + skore / 5  # Increase speed over time
        self.acceleration = 0.01  # Acceleration factor

    def update(self, player_x, player_y, skore):
        self.x -= self.speed
        self.speed += self.acceleration  # Increase speed over time

        if self.x < -self.width:
            self.reset(skore)
            return False

        # Check for collision with player
        if (
            player_x < self.x + self.width
            and player_x + velikostx > self.x
            and player_y < self.y + self.height
            and player_y + velikosty > self.y
        ):
            return True

        return False

obstacles = [Obstacle(0) for _ in range(5)]

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
                    reset_game()
        elif udalost.type == pygame.MOUSEBUTTONDOWN:
            if udalost.button == 1:
                if button_rect2.collidepoint(udalost.pos):
                    print("Quited")
                    soubor2 = open("Save.txt", "w", encoding="utf-8")
                    soubor2.write(str(skore))
                    soubor2.close()
                    pygame.quit()
                    sys.exit()

    if esc:
        is_hovered = button_rect.collidepoint(pygame.mouse.get_pos())
        is_hovered2 = button_rect2.collidepoint(pygame.mouse.get_pos())

        pygame.draw.rect(okno, (0, 0, 0), (100, 100, 600, 400))
        if is_hovered:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
                draw_button(button_rect, click_color, "Reseted")
            else:
                draw_button(button_rect, button_color, "Reset")
        else:
            draw_button(button_rect, button_color, "Reset")

        if is_hovered2:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
                draw_button(button_rect2, click_color, "Quited and Saved")

                soubor2 = open("Save.txt", 'w', encoding='utf-8')
                soubor2.write(str(skore))
                soubor2.close()

                pygame.quit()
                sys.exit()
            else:
                draw_button(button_rect2, button_color, "Quit and Save")
        else:
            draw_button(button_rect2, button_color, "Quit and Save")

        pygame.display.flip()

    if not esc:
        stisknute_klavesy = pygame.key.get_pressed()
        okno.fill((0, 0, 0))

        pygame.draw.rect(okno, (255, 255, 255), (playerx, playery, velikostx, velikosty))

        for obstacle in obstacles:
            if obstacle.update(playerx, playery, skore):
                print("Game Over!")
                obstacles = [Obstacle(skore) for _ in range(5)]
                skore = 0

        fps_counter()
        clock.tick(100)  # Limit FPS to 60

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

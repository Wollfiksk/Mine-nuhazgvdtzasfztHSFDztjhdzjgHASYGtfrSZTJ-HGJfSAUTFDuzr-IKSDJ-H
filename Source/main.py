import sys
import pygame
import random
import time
import os  

pygame.init()
pygame.font.init()

with open("Save.txt", "r", encoding="utf-8") as file:
    money = int(file.readline().strip())
    skin = tuple(map(int, file.readline().strip().split(',')))

print(skin)

rozliseni_okna = (800, 600)
okno = pygame.display.set_mode(rozliseni_okna)

current_dir = os.path.dirname(__file__)  
image_path = os.path.join(current_dir, "obrazky", "images-removebg-preview.png")
 
try:
    image = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit()

file.close()

image_rect = image.get_rect()
image_rect.center = (rozliseni_okna[0] // 2, rozliseni_okna[1] // 2)
 
playerx = 20
playery = 440
velikostx = 40
velikosty = 50
gravity = 5
jump_count = 15
is_jumping = False
player_rect = pygame.Rect(playerx, playery, velikostx, velikosty) 
lives = 3

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 40)
esc = False

skore = 0

button_rect4 = pygame.Rect(300, 70, 200, 100)
button_rect3 = pygame.Rect(300, 460, 200, 100)
button_rect2 = pygame.Rect(300, 200, 200, 100)
button_rect = pygame.Rect(300, 330, 200, 100)
button_color = (100, 100, 100)
click_color = (100, 100, 100)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = pygame.math.Vector2(0, 0)
        self.radius = 5

    def move(self):
        self.x += self.speed.x
        self.y += self.speed.y

    def draw(self):
        pygame.draw.circle(okno, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

class Obstacle:
    def __init__(self, skore):
        self.reset(skore)

    def reset(self, skore):
        self.width = 50
        self.height = random.randint(50, 200)
        self.rect = pygame.Rect(800, 550 - self.height, self.width, self.height)
        self.speed = 0.3
        self.acceleration = 0.01

    def update(self, skore):
        global playerx, playery, is_jumping, jump_count
        self.rect.x -= self.speed
        self.speed += self.acceleration

        if self.rect.colliderect(player_rect):
            if not is_jumping:  
                playerx = self.rect.x - self.rect.width  
            else:
                playery = self.rect.y + velikosty
                playerx = self.rect.x + velikosty
                jump_count = 0
                is_jumping = False

        if self.rect.x < -self.width:
            self.reset(skore)
            return False

        return False

class Enemy:
    def __init__(self, skore):
        self.reset(skore)

    def reset(self, skore):
        self.width = 50
        self.height = 70
        self.rect = pygame.Rect(850, 550 - self.height, self.width, self.height)
        self.speed = 0.3
        self.acceleration = 0.01

    def update(self, skore):
        global playerx, playery, is_jumping, jump_count
        self.rect.x -= self.speed
        self.speed += self.acceleration

        if self.rect.x < (-self.width - 300):
            self.reset(skore)
            return False

        return False

bullets = []
enemies = [Enemy(0) for _ in range(5)]
obstacles = [Obstacle(0) for _ in range(5)]

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
    global skore, is_jumping
    skore = 0
    is_jumping = False

def increase_money(amount):
    global money
    money += amount

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc = not esc
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Create bullet at player position
                bullet = Bullet(playerx + velikostx // 2, playery + velikosty // 2)
                
                # Calculate bullet direction towards cursor position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = pygame.math.Vector2(mouse_x - bullet.x, mouse_y - bullet.y).normalize()
                
                # Set bullet speed based on direction
                bullet.speed = direction * 10
                
                # Add bullet to bullets list
                bullets.append(bullet)

    if esc:
        is_hovered = button_rect.collidepoint(pygame.mouse.get_pos())
        is_hovered2 = button_rect2.collidepoint(pygame.mouse.get_pos())
        is_hovered3 = button_rect3.collidepoint(pygame.mouse.get_pos())
        is_hovered4 = button_rect4.collidepoint(pygame.mouse.get_pos())

        pygame.draw.rect(okno, (0, 0, 0), (100, 100, 600, 400))

        if is_hovered:
            if pygame.mouse.get_pressed()[0]:
                draw_button(button_rect, click_color, "Reseted")
            else:
                draw_button(button_rect, button_color, "Reset")
        else:
            draw_button(button_rect, button_color, "Reset")

        if is_hovered2:
            if pygame.mouse.get_pressed()[0]:
                draw_button(button_rect2, click_color, "Quited and Saved")

                with open("soubor.txt", "w", encoding="utf-8") as file:
                    file.write(str(money) + "\n")
                    file.write(",".join(map(str, skin)) + "\n")
                    file.close()
                pygame.quit()
                sys.exit()
            else:
                draw_button(button_rect2, button_color, "Quit and Save")
        else:
            draw_button(button_rect2, button_color, "Quit and Save")   
            
        if is_hovered3:
            if pygame.mouse.get_pressed()[0]:
                draw_button(button_rect3, click_color, "Skin 1")

                skin = (255, 0, 0)

                with open("soubor.txt", "w", encoding="utf-8") as file:
                    file.write(str(money) + "\n")
                    file.write(",".join(map(str, skin)) + "\n")
                    file.close()
            else:
                draw_button(button_rect3, button_color, "Skin 1")
        else:
            draw_button(button_rect3, button_color, "Skin 1")

        if is_hovered4:
            if pygame.mouse.get_pressed()[0]:
                draw_button(button_rect4, click_color, "Skin 2")

                skin = (0, 0, 255)

                with open("soubor.txt", "w", encoding="utf-8") as file:
                    file.write(str(money) + "\n")
                    file.write(",".join(map(str, skin)) + "\n")
                    file.close()
            else:
                draw_button(button_rect4, button_color, "Skin 2")
        else:
            draw_button(button_rect4, button_color, "Skin 2")

        pygame.display.flip()

    if not esc:
        stisknute_klavesy = pygame.key.get_pressed()
        if skore > 5000 and skore < 10000:
            okno.fill((255, 0, 0))
        elif skore > 10000 and skore < 15000:
            okno.fill((0, 255, 255))
        else:
            okno.fill((0, 0, 0))

        pygame.draw.rect(okno, skin, (playerx, playery, velikostx, velikosty))
        player_rect = pygame.Rect(playerx, playery, velikostx, velikosty)
        okno.blit(image, image_rect)

        for obstacle in obstacles:
            if obstacle.update(skore):
                print("Game Over!")

        for enemy in enemies:
            if enemy.update(skore):
                print("Game Over!")
            pygame.draw.rect(okno, (255, 255, 255), (enemy.rect.x + 300, enemy.rect.y, enemy.width, enemy.height))

        for bullet in bullets:
            bullet.move()
            bullet.draw()

            # Check collision with enemies
            for enemy in enemies:
                if enemy.rect.colliderect(pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius,
                                                      bullet.radius * 2, bullet.radius * 2)):
                    enemies.remove(enemy)
                    increase_money(10)  # Increase money when enemy is hit
                    bullets.remove(bullet)
                    break
            
            # Check collision with obstacles
            for obstacle in obstacles:
                if obstacle.rect.colliderect(pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius,
                                                         bullet.radius * 2, bullet.radius * 2)):
                    bullets.remove(bullet)
                    break

            # Remove bullet if it goes out of screen
            if bullet.x < 0 or bullet.x > rozliseni_okna[0] or bullet.y < 0 or bullet.y > rozliseni_okna[1]:
                bullets.remove(bullet)

        fps_counter()
        clock.tick(100)

        
        if playerx < -80: 
            print("you died")
            lives -= 1
            if lives == 0:
                print("you lost")
                print("you lost")
                print("you lost")
                print("you lost")
                time.sleep(2)
                quit()
            playerx = 20
            playery = 200
            

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
        skore += 1
        for obstacle in obstacles:
            pygame.draw.rect(okno, (255, 0, 0), (obstacle.rect.x, obstacle.rect.y, obstacle.width, obstacle.height))
        
        for enemy in enemies:
            pygame.draw.rect(okno, (255, 255, 255), (enemy.rect.x + 300, enemy.rect.y, enemy.width, enemy.height))

        txtimg = font2.render("Skore: " + str(skore), True, (255, 255, 255))
        money_text = font2.render("Money: " + str(money), True, (255, 255, 255))
        okno.blit(money_text, (600, 40))
        okno.blit(txtimg, (600, 0))

        pygame.display.update()

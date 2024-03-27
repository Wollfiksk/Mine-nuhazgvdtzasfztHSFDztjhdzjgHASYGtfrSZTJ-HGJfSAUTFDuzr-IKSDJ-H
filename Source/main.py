import sys
import pygame
import random
import time
import os

pygame.init()
pygame.font.init()

file_path = os.path.join(os.path.dirname(__file__), "uloz.txt")

rozliseni_okna = (800, 600)
okno = pygame.display.set_mode(rozliseni_okna)

with open(file_path, "r", encoding="utf-8") as file:
    money = int(file.readline().strip())
    print("Money:", money)
    skin = int(file.readline().strip())
    print("Skin:", skin)

print(skin)

file.close()

playerx = 20
playery = 440
velikostx = 40
velikosty = 50
gravity = 5
jump_count = 15
is_jumping = False
player_rect = pygame.Rect(playerx, playery, velikostx, velikosty)
lives = 3
jump_counterds = 0
upgrade = 0
count = 1
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 40)
esc = False

skin3_bought = False
skin2_bought = False
skore = 0
kill_count = 0
button_rect = pygame.Rect(250, 260, 300, 60)
button_rect2 = pygame.Rect(250, 330, 300, 60)
button_rect3 = pygame.Rect(250, 400, 300, 60)
button_rect4 = pygame.Rect(250, 470, 300, 60)
button_rect_upgrade = pygame.Rect(250, 540, 300, 60)
button_color = (100, 100, 100)
click_color = (100, 100, 100)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = pygame.math.Vector2(0, 0)

    def update(self):
        self.rect.move_ip(self.speed)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, skore):
        super().__init__()
        self.reset(skore)

    def reset(self, skore):
        self.image = pygame.Surface((50, random.randint(50, 200)))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(800, 550 - self.image.get_height()))
        self.speed = 0.3
        self.acceleration = 0.01

    def update(self, skore):
        global is_jumping, playerx, playery, jump_count
        self.rect.x -= self.speed
        self.speed += self.acceleration

        if self.rect.colliderect(player_rect):
            if not is_jumping:
                playerx = self.rect.x - player_rect.width
            else:
                if player_rect.bottom <= self.rect.top + 5:  
                    playery = self.rect.top - player_rect.height
                    playerx = self.rect.x - player_rect.width  
                    jump_count = 0
                    is_jumping = False

        if self.rect.x < -self.rect.width:
            self.reset(skore)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, skore):
        super().__init__()
        self.active = False 
        self.reset(skore)

    def reset(self, skore):
        if not self.active:  
            self.image = pygame.Surface((50, 70))
            self.image.fill((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(1000, 1500)
            self.rect.y = 550 - self.image.get_height()
            self.speed = 4
            self.active = True  

    def update(self, skore):
        if self.active:  
            self.rect.x -= self.speed

            if self.rect.x < 0:
                self.rect.x = random.randint(1000, 1500)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemies = pygame.sprite.Group()

for _ in range(50):
    obstacles.add(Obstacle(0))
enemies.add(Enemy(0))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30)) 
        self.image.fill((255, 255, 0)) 
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, rozliseni_okna[0] - 30) 
        self.rect.y = random.randint(0, rozliseni_okna[1] - 30) 

powerups = pygame.sprite.Group()  
last_powerup_spawn = pygame.time.get_ticks()  
spawn_interval = random.randint(30000, 60000)

def spawn_powerup():
    global last_powerup_spawn, spawn_interval
    current_time = pygame.time.get_ticks()

    if current_time - last_powerup_spawn > spawn_interval:
        powerup = PowerUp()
        powerups.add(powerup)

        last_powerup_spawn = current_time
        spawn_interval = random.randint(400, 500)

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

achievements = {
    "Jump 50 times": {"condition": lambda: jump_counterds >= 50, "reward": 100},
    "Jump 100 times": {"condition": lambda: jump_counterds >= 100, "reward": 200},
    "kill 10 enemies ": {"condition": lambda: kill_count >= 10, "reward": 300},
}

def buy_upgrade():
    global money, upgrade
    if money >= 50:
        money -= 50
        upgrade += 0.3

earned_achievements = set()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc = not esc
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet = Bullet(playerx + velikostx // 2, playery + velikosty // 2)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = pygame.math.Vector2(mouse_x - bullet.rect.centerx, mouse_y - bullet.rect.centery).normalize()
                bullet.speed = direction * 10
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif event.button == 3:
                if button_rect_upgrade.collidepoint(event.pos):
                    buy_upgrade()

    if esc:
        is_hovered = button_rect.collidepoint(pygame.mouse.get_pos())
        is_hovered2 = button_rect2.collidepoint(pygame.mouse.get_pos())
        is_hovered3 = button_rect3.collidepoint(pygame.mouse.get_pos())
        is_hovered4 = button_rect4.collidepoint(pygame.mouse.get_pos())

        pygame.draw.rect(okno, (0, 0, 0), (100, 100, 600, 400))

        if is_hovered:
            if pygame.mouse.get_pressed()[0]:
                draw_button(button_rect, click_color, "default")
                skin = 1

                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(str(money) + "\n")
                    file.write(str(skin) + "\n")
                    file.close()
            else:
                draw_button(button_rect, button_color, "default")
        else:
            draw_button(button_rect, button_color, "default")

        is_hovered_upgrade = button_rect_upgrade.collidepoint(pygame.mouse.get_pos())
        if is_hovered_upgrade:
            if pygame.mouse.get_pressed()[0]:
                draw_button(button_rect_upgrade, click_color, "Buy Upgrade")
                buy_upgrade()  # Buy upgrade when clicked
            else:
                draw_button(button_rect_upgrade, button_color, "Buy Upgrade")
        else:
            draw_button(button_rect_upgrade, button_color, "Buy Upgrade")

        pygame.display.flip()
        
        if is_hovered2:
            if pygame.mouse.get_pressed()[0]:
                    draw_button(button_rect2, click_color, "Quited and Saved")

                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(str(money) + "\n")
                        file.write(str(skin) + "\n")
                        file.close()
                    pygame.quit()
                    sys.exit()
            else:
                draw_button(button_rect2, button_color, "Quit and Save")
        else:
            draw_button(button_rect2, button_color, "Quit and Save")

        if is_hovered3:
            if pygame.mouse.get_pressed()[0]:
                if money >= 500 or skin2_bought:
                    draw_button(button_rect3, click_color, "eqiped")
                    money = 0
                    skin = 2
                    skin2_bought = True
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(str(money) + "\n")
                        file.write(str(skin) + "\n")
                        file.close()
                else:
                    draw_button(button_rect3, (255, 0, 0), "Not enough money!")
            else:
                draw_button(button_rect3, button_color, "Skin 1 jump + 10 cost:500")
        else:
            draw_button(button_rect3, button_color, "Skin 1 jump + 10 cost:500")

        if is_hovered4:
            if pygame.mouse.get_pressed()[0]:
                if money >= 1000 or skin3_bought:
                    draw_button(button_rect4, click_color, "eqiped")
                    money = 0
                    skin = 3
                    skin3_bought = True
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(str(money) + "\n")
                        file.write(str(skin) + "\n")
                        file.close()
                else:
                    draw_button(button_rect4, (255, 0, 0), "Not enough money!")
            else:
                draw_button(button_rect4, button_color, "Skin 2 jump + 15 cost:1000")
        else:
            draw_button(button_rect4, button_color, "Skin 2 jump + 15 cost:1000")

        pygame.display.flip()

    if not esc:
        stisknute_klavesy = pygame.key.get_pressed()
        if skore > 2000 and skore < 5000:
            okno.fill((255, 255, 0))
        elif skore > 5000:
            okno.fill((0, 255, 255))
        else:
            okno.fill((0, 0, 0))

        if skin == 1:
            pygame.draw.rect(okno, (255,255,255), (playerx, playery, velikostx, velikosty))
            skin_text = font.render("+0", True, (255, 255, 255))
            okno.blit(skin_text, (playerx + 5, playery + velikosty))
        elif skin == 2:
            pygame.draw.rect(okno, (255,0,0), (playerx, playery, velikostx, velikosty))
            skin2_text = font.render("+10", True, (255, 255, 255))
            okno.blit(skin2_text, (playerx + 5, playery + velikosty))
        elif skin == 3:
            pygame.draw.rect(okno, (0,0,255), (playerx, playery, velikostx, velikosty))
            skin3_text = font.render("+15", True, (255, 255, 255))
            okno.blit(skin3_text, (playerx + 5, playery + velikosty))

        player_rect = pygame.Rect(playerx, playery, velikostx, velikosty)

        for obstacle in obstacles:
            if obstacle.update(skore):
                print("Game Over!")

        for enemy in enemies:
            if enemy.update(skore):
                print("Game Over!")

        all_sprites.update()
        bullets_hit_enemies = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for enemy in bullets_hit_enemies.values():
            increase_money(50 * len((enemy)))
            kill_count += 1
            enemies.add(Enemy(0))
            for e in enemy:
                if e in enemies:
                    enemies.add(e)
                e.reset(skore)

        all_sprites.draw(okno)
        for obstacle in obstacles:
            okno.blit(obstacle.image, obstacle.rect)
        for enemy in enemies:
            okno.blit(enemy.image, enemy.rect)

        bullets_hit_obstacles = pygame.sprite.groupcollide(bullets, obstacles, True, False)
        for bullet, _ in bullets_hit_obstacles.items():
            bullet.kill()

        for achievement_name, achievement in achievements.items():
            if achievement_name not in earned_achievements and achievement['condition']():
                increase_money(achievement['reward'])
                earned_achievements.add(achievement_name)
                print(f"Achievement Unlocked: {achievement_name}")
                jump_counter = 0
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
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(str(money) + "\n")
                    file.write(str(skin) + "\n")
                    file.close()

                time.sleep(2)
                quit()
            playerx = 20
            playery = 200

        if playery < 440:
            on_ground = False
        else:
            on_ground = True
            playery = 440

        achive1_text = font.render("Jump 50 times", True, (255, 255, 255))
        okno.blit(achive1_text, (5, 30))
        achive2_text = font.render("Jump 100 times", True, (255, 255, 255))
        okno.blit(achive2_text, (5, 60))
        achive3_text = font.render("kill 10 enemies", True, (255, 255, 255))
        okno.blit(achive3_text, (5, 90))

        if stisknute_klavesy[pygame.K_SPACE]:
            if not is_jumping and on_ground:
                is_jumping = True

        if is_jumping:
            if jump_count >= -15:
                neg = 1
                if jump_count < 0:
                    neg = -1
                if skin == 1:
                    if count > 0:
                        jump_counterds += 1
                        count = 0
                    playery -= 12 + upgrade
                if skin == 2:
                    if count > 0:
                        jump_counterds += 1
                        count = 0
                    playery -= 14 + upgrade
                if skin == 3:
                    if count > 0:
                        jump_counterds += 1
                        count = 0
                    playery -= 15 + upgrade
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 15
                count = 1

        playery += gravity
        skore += 1

        spawn_powerup()

        txtimg = font2.render("Skore: " + str(skore), True, (255, 255, 255))
        money_text = font2.render("Money: " + str(money), True, (255, 255, 255))
        okno.blit(money_text, (600, 40))
        okno.blit(txtimg, (600, 0))

        pygame.display.update()


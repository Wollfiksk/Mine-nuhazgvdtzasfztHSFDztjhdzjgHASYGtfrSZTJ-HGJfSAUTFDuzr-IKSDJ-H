import pygame
import sys
import random

pygame.init()
pygame.font.init()

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)

clock = pygame.time.Clock()

playerx = 20
playery = 440
velikostx = 40
velikosty = 50

gravity = 4

button_rect2 = pygame.Rect(300, 200, 200, 100)
button_rect = pygame.Rect(300, 330, 200, 100)
button_color = (100, 100, 100)
click_color = (100, 100, 100)

jump_count = 10

font = pygame.font.SysFont(None , 40)
font2 = pygame.font.SysFont(None , 40)
esc = False

jo = False
jo2 = False 
fps = str(int(clock.get_fps()))

def draw_button(rect, color, text):
    pygame.draw.rect(okno, color, rect)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    okno.blit(text_surface, text_rect)
    
def draw_text(x, y):
    txtimg = font2.render("Skore: " + str(skore), True, (0, 0, 0))
    okno.blit(txtimg, (x, y))

def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    okno.blit(fps_t,(0,0))

def reset_game():     
    global pozice_micku_x, pozice_micku_y, skore
    pozice_micku_x = 400
    pozice_micku_y = 300
    skore = 0
    
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
                    quit()
        
    
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
                
                quit()
            else:
                draw_button(button_rect2, button_color, "Quit and Save")
        else:
            draw_button(button_rect2, button_color, "Quit and Save")
            
        pygame.display.flip()
        


    if not esc:            
        stisknute_klavesy = pygame.key.get_pressed()
        okno.fill((0, 0, 0))
        
        direction = pygame.Vector2(playerx, playery)
        pygame.draw.rect(okno, (255, 255, 255), (playerx, playery, velikostx, velikosty))

        playery += gravity

        fps_counter()
        clock.tick(100)
                
        #jump

        if playery < 440:
            on_ground = False
        else:
            on_ground = True
            playery = 440

        if stisknute_klavesy[pygame.K_SPACE]:
            if jump_count > 0:
                playery -= 7
                jump_count -= 0.1
        if jump_count <= 10 and on_ground:  # Reset jump_count only when on the ground
            jump_count = 10
     
        pygame.display.update()     
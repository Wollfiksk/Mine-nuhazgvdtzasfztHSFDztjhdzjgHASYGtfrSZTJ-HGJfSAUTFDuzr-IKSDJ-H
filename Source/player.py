import pygame
import sys

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)

def player(playerx, playery, velikostx, velikosty):
    direction = pygame.Vector2(playerx, playery)


    pygame.draw.rect(okno, (255, 255, 255), (playerx, playery, velikostx, velikosty))
    return(playerx, playery)
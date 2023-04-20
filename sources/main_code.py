import pygame
import sys
import fusion
pygame.init()


WIDTH = 1920
HEIGHT = 1080

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

menu_img = pygame.image.load("images/menu_pyng_pong.jpg").convert()
menu_img = pygame.transform.scale(menu_img, (WIDTH, HEIGHT))


def menu():
    """
    affiche le menu du jeu
    """
    while True:
        WIN.blit(menu_img, (0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        elif keys[pygame.K_RETURN]:
            fusion.main()
        pygame.event.pump()
        pygame.display.update()


if __name__ == '__main__':
    menu()

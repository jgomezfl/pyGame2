import pygame
import sys
# from main import main

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def Game_Over(window):
    # pygame.init()
    # window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Over")
    
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render("Game Over", True, BLANCO)
    texto_rect = texto.get_rect()
    
    run = True
    while run:
        window.fill(NEGRO)
        window.blit(texto, [window.get_width() / 2 - texto_rect.width / 2, window.get_height() / 2 - texto_rect.height / 2])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        pygame.display.flip()
    sys.exit()

if __name__ == "__main__":
    Game_Over(window)
import pygame
import sys
# from main import main

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def Congratulations(window):
    pygame.display.set_caption("Congratulations")
    
    fondo = pygame.image.load("assets/background/Congratulations.jpg")
    fondo_rect = fondo.get_rect()
    
    fuente = pygame.font.Font(None, 36)
    # texto = fuente.render("Presiona la tecla enter para volver al menú de inicio", True, BLANCO)
    texto1 = fuente.render("Presiona la tecla scape para terminar el juega", True, BLANCO)
    # texto_rect = texto.get_rect()
    texto1_rect = texto1.get_rect()
    
    run = True
    while run:
        window.fill(NEGRO)
        window.blit(fondo, [window.get_width() / 2 - fondo_rect.width / 2, window.get_height() / 2 - fondo_rect.height / 2 - 50])
        # window.blit(texto, [window.get_width() / 2 - texto_rect.width / 2, window.get_height() / 2 + fondo_rect.height / 2])
        window.blit(texto1, [window.get_width() / 2 - texto1_rect.width / 2, window.get_height() / 2 + fondo_rect.height / 2 + 30])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        pygame.display.flip()
    sys.exit()
    
if __name__ == "__main__":
    Congratulations(window)
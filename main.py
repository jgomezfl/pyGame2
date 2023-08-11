import os, random, math, pygame
from os import listdir
from os.path import isfile, join
import sys
from Level1 import level1
from Level2 import level2

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

WIDTH, HEIGHT = 1000, 800

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    
    return tiles, image

# def dibujar_texto(window, texto, contenedor_imagen, contenedor_rec, fuente_render, color):
#     text = fuente_render.render(texto, 1, color)
#     centro = text.get_rect()
#     diferencia_x = contenedor_imagen.center[0] - centro.center[0]
#     diferencia_y = contenedor_imagen.center[1] - centro.center[1]
#     window.blit(text, [contenedor_rec.left + diferencia_x, contenedor_rec.top + diferencia_y])

def dibujar_texto(pantalla, texto, contenedor_imagen, contenedor_rec, fuente_render, color):
    text = fuente_render.render(texto, 1, color)
    centro = text.get_rect()
    diferencia_x = contenedor_imagen.center[0] - centro.center[0]
    diferencia_y = contenedor_imagen.center[1] - centro.center[1]
    pantalla.blit(text, [contenedor_rec[0] + diferencia_x, contenedor_rec[1] + diferencia_y])

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main Menú")
    
    # background
    background, bg_image = get_background("Blue.png")
    for tile in background:
        screen.blit(bg_image, tile)
    
    #Fuente Titulo
    FuenteTitulo = pygame.font.Font("assets/Fonts/Roboto-Bold.ttf", 80)
    text = FuenteTitulo.render("Bienvenido", True, NEGRO)
    text_rect = text.get_rect()
    
    # imagenes de los botones
    imagen_boton = pygame.image.load("assets/Botones/button.png")
    imagen_boton_rect = imagen_boton.get_rect()
    imagen_boton_pressed = pygame.image.load("assets/Botones/buttonPressed.png")
    fuente_botones = pygame.font.SysFont('Courier', 20)
    
    #botones
    botonLevel1 = {'text': "Nivel 1", 'image': imagen_boton, 'image_pressed': imagen_boton_pressed, 'rect': [screen.get_width() / 2 - imagen_boton_rect.width / 2, 450], 'on_click': False}
    boton1Rect = pygame.Rect(botonLevel1['rect'][0], botonLevel1['rect'][1], botonLevel1['image'].get_rect()[2], botonLevel1['image'].get_rect()[3])
    botonLevel2 = {'text': "Nivel 2", 'image': imagen_boton, 'image_pressed': imagen_boton_pressed, 'rect': [screen.get_width() / 2 - imagen_boton_rect.width / 2, 450 + imagen_boton_rect.height + 20], 'on_click': False}
    boton2Rect = pygame.Rect(botonLevel2['rect'][0], botonLevel2['rect'][1], botonLevel2['image'].get_rect()[2], botonLevel2['image'].get_rect()[3])
    
    run = True
    while run:
        screen.blit(text, (screen.get_width() / 2 - text_rect.width / 2, 100))
        if botonLevel1["on_click"]:
            screen.blit(botonLevel1['image_pressed'], botonLevel1['rect'])
        else:
            screen.blit(botonLevel1['image'], botonLevel1['rect'])
        dibujar_texto(screen, botonLevel1['text'], botonLevel1['image'].get_rect(), botonLevel1['rect'], fuente_botones, BLANCO)
        if botonLevel2["on_click"]:
            screen.blit(botonLevel2['image_pressed'], botonLevel2['rect'])
        else:
            screen.blit(botonLevel2['image'], botonLevel2['rect'])
        dibujar_texto(screen, botonLevel2['text'], botonLevel2['image'].get_rect(), botonLevel2['rect'], fuente_botones, BLANCO)
        # print(botonLevel1["on_click"])
        # print(botonLevel2["on_click"])
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE:
                    level1(screen)
                # if event.key == pygame.K_0:
                #     Congratulations(screen)
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                botonLevel1['on_click'] = False
                if boton1Rect.collidepoint( mouse ):
                    level1(screen)
                if boton2Rect.collidepoint( mouse ):
                    level2(screen)
                botonLevel2['on_click'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                botonLevel1['on_click'] = boton1Rect.collidepoint( mouse )
                botonLevel2['on_click'] = boton2Rect.collidepoint( mouse )
    sys.exit()
    
if __name__ == "__main__":
    main()
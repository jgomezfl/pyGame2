import os, random, math, pygame
from os import listdir
from os.path import isfile, join

# from pygame.sprite import _Group
pygame.init()

pygame.display.set_caption("Plataformer")

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 2.5
PLAYER_POINTS = 0

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip (sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, width, height, direction=False):
    path = join("assets", dir1)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    
    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
            
        if direction:
            all_sprites[image.replace(".png", ""+ "_right")] = sprites
            all_sprites[image.replace(".png", ""+ "_left")] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
            
    return all_sprites

def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

# backgroud
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    
    return tiles, image

# class shoots
class shoot(pygame.sprite.Sprite):
    Shoot_vel = 5
    # SPRITES = load_sprite_sheets("Shoot", 10, 10, True)
    # ANIMATION_DELAY = 3
    
    def __init__(self, x, y, timeShooted, direction):
        super().__init__()
        self.rect = pygame.Rect(x, y, 1, 1)
        self.image = pygame.image.load(join("assets", "Shoot", "shoot1.png"))
        self.direction = direction
        if self.direction == "left":
            self.image = pygame.image.load(join("assets", "Shoot", "shoot2.png"))
        
        #Sprite mask 
        self.rect.y = y + 25
        self.rect.x = x
        
        self.cadencia = 750
        self.timeShooted = timeShooted
    
    def update(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.timeShooted > self.cadencia:
            self.kill()
        
        if self.direction == "left":
            self.rect.x -= self.Shoot_vel
        else:
            self.rect.x += self.Shoot_vel
        
    # def draw(self, win, offset_x):
    #     win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

#Player class
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacter", 32, 32, True)
    ANIMATION_DELAY = 10
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        
        #Velocity vector
        self.x_vel = 0
        self.y_vel = 1
        
        #Sprite mask 
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        
        #jump and double jump
        self.jump_count = 2
        self. isFalling = True
        
        #atacking
        self.attack = False
        self.cadencia = 750
        self.last_shoot = pygame.time.get_ticks()
        
        #List of blocks
        self.BlocksLevel = None
        
    def update(self, offset_x):
        
        self.calc_grav()
        
        self.rect.x += self.x_vel
        list_blocks_collided = pygame.sprite.spritecollide(self, self.BlocksLevel, False)
        for block in list_blocks_collided:
            if self.x_vel > 0:
                self.rect.right = block.rect.left
            elif self.x_vel < 0:
                self.rect.left = block.rect.right
        
        self.rect.y += self.y_vel
        list_blocks_collided = pygame.sprite.spritecollide(self, self.BlocksLevel, False)
        for block in list_blocks_collided:
            if self.y_vel > 0:
                self.rect.bottom = block.rect.top
                self.jump_count = 0
                self.y_vel = 0
            elif self.y_vel < 0:
                self.rect.top = block.rect.bottom
                self.y_vel = 1
        
        if self.rect.left < offset_x:
            self.rect.x = offset_x

        
        self.update_sprite()
    
    def calc_grav(self):
        if self.y_vel == 0:
            self.y_vel = 1
        else:
            self.y_vel += .35
            
    def jump(self):
        self.jump_count += 1
        if self.jump_count == 1:
            self.y_vel = -11
        elif self.jump_count == 2:
            self.y_vel = -7
        self.cadencia = 750
        self.animation_count = 0
            
    def attacking(self):
        ahora = pygame.time.get_ticks()
        self.animation_count = 0
        if ahora - self.last_shoot > self.cadencia:
            self.attack = True
            self.last_shoot = ahora
            bullet = shoot(self.rect.x, self.rect.y, self.last_shoot, self.direction)
            bullets.add(bullet)
        
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        
    
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    def update_sprite(self):
        sprite_sheet = "idle"
        ahora = pygame.time.get_ticks()
        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.attack:
            sprite_sheet = "attack"
            if ahora - self.last_shoot > self.cadencia:
                self.attack = False
        elif self.y_vel > 0:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "walking"
        
        sprite_sheet_name = sprite_sheet+"_"+self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

#Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        
        # block = get_block(size)
        # self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # self.image.blit(block, (0, 0))
        # self.mask = pygame.mask.from_surface(self.image)
        # self.width = size
        # self.height = size

#class block
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.rect = pygame.Rect(x, y, size, size)
        block = get_block(size)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = size
        self.height = size
    
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

#class level
class Level():
    
    def __init__(self, player):
        self.block_list = pygame.sprite.Group()
        self.player = player
        
        #Move around the level
        self.scroll_stage = 0
        
    def update(self):
        self.block_list.update()
        
    def draw(self, window, offset_x):
        for obj in self.block_list:
            obj.draw(window, offset_x)
        
    # def scrolling_stage(self, scroll_x):
    #     self.scroll_stage -= scroll_x
        
    #     for block in self.block_list:
    #         block.rect.x -= scroll_x
            
#Lever 1
class Level1(Level):
    
    MAPA = [
        "",
        "",
        "",
        "",
        " , , , , , , , , , , , , ,X",
        " , , ,X",
        "X, , ,X, , , ,X, , , ,X",
        "X,X,X,X,X,X,X,X,X,X",
    ]
    
    def __init__(self, player, block_size):
        Level.__init__(self, player)
        
        level_blocks = [] 
        cont = 8       
        for i in self.MAPA:
            blocks = i.split(",")
            if(blocks[0] != ''):
                cont1 = 0
                for block in blocks:
                    if block == "X":
                        # print(cont1, " ", cont)
                        # Block((block_size * cont1), HEIGHT - (block_size*cont), block_size)
                        level_blocks.append(Block((block_size * cont1), HEIGHT - (block_size*cont), block_size))
                    cont1 += 1
            cont -= 1
                        
        
        floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(10)]
        walls1 = [Block(0, HEIGHT - (block_size * (i+2)), block_size) for i in range(7)]
        walls = [*walls1, *floor, Block(250, 450, block_size)]
        
        for wall in level_blocks:
            block = wall
            self.block_list.add(block)
        
        

#draw method
def draw(window, background, bg_image, player, offset_x, level, bullets):
    for tile in background:
        window.blit(bg_image, tile)
    bullets.draw(window)
    for bullet in bullets:
        bullet.update()
    
    level.draw(window, offset_x)
    player.draw(window, offset_x)
        
    pygame.display.update()

bullets = pygame.sprite.Group()

def main(window):
    background, bg_image = get_background("Green.png")
    
    block_size = 96
    
    player = Player(100, 100, 70, 70)
    level = Level1(player, block_size)  
    player.BlocksLevel = level.block_list
    
    offset_x = 0
    scroll_area_width = 200
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left(PLAYER_VEL)
                if event.key == pygame.K_RIGHT:
                    player.move_right(PLAYER_VEL)
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    player.attacking()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.x_vel < 0: 
                    player.x_vel = 0
                if event.key == pygame.K_RIGHT and player.x_vel > 0:
                    player.x_vel = 0
            
        player.update(offset_x)
        draw(window, background, bg_image, player, offset_x, level, bullets)
        
        if(player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0):
            offset_x += player.x_vel
            
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main(window)
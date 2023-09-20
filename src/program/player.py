import pygame
import time
from PIL import ImageOps, Image

import pygame.image

class Player(pygame.sprite.Sprite):

    def __init__(self, x,y):
        
        super().__init__()

        self.x = x
        self.y = y

        self.sprites_run = []
        self.sprites_run.append(pygame.image.load('../tiled/warrior/deplacement/Run1.png'))
        self.sprites_run.append(pygame.image.load('../tiled/warrior/deplacement/Run2.png'))
        self.sprites_run.append(pygame.image.load('../tiled/warrior/deplacement/Run3.png'))

        self.sprites_attack_1 = []
        self.sprites_attack_1.append(pygame.image.load('../tiled/warrior/attack/animation_1/Attack1.1.png'))
        self.sprites_attack_1.append(pygame.image.load('../tiled/warrior/attack/animation_1/Attack1.3.png'))
        self.sprites_attack_1.append(pygame.image.load('../tiled/warrior/attack/animation_1/Attack1.4.png'))

        self.sprites_attack_2 = []
        self.sprites_attack_2.append(pygame.image.load('../tiled/warrior/attack/animation_2/Attack_1-.png'))
        self.sprites_attack_2.append(pygame.image.load('../tiled/warrior/attack/animation_2/Attack_2-.png'))
        self.sprites_attack_2.append(pygame.image.load('../tiled/warrior/attack/animation_2/Attack_4-.png'))

        self.current_sprite = 0

        self.sprite_sheet_run     = pygame.image.load('../tiled/warrior/deplacement/run2.png').convert_alpha()
        self.sprite_sheet_default = pygame.image.load('../tiled/warrior/warrior.png').convert_alpha()


        self.image = self.sprite_sheet_default
        self.rect = self.image.get_rect()
        self.health = 100
        self.max_health = 100
        self.attack_dmg = 4
        self.position = [x,y]
        self.speed = 3
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_pos = self.position.copy()
        self.hitbox = [x + 15, y + 2, 60]


    # Sauvegarde la position
    def save_loc(self):self.old_pos = self.position.copy()

    # Va à droite
    def move_right(self) : self.position[0] += self.speed ; self.image = self.run_update()

    # Va à gauche
    def move_left(self): self.position[0] -= self.speed ; self.image = self.run_update()
    # Va en haut
    def move_up(self)    : self.position[1] -= self.speed ; self.image = self.run_update()

    # Va en bas
    def move_down(self)  : self.position[1] += self.speed ; self.image = self.run_update()

    # Attaque
    def attack(self, monsters)     :                        self.image = self.attack1_update(); self.get_hit(monsters)

    # Attaque 2
    def attack2(self, monsters)     :                       self.image = self.attack2_update(); self.get_hit(monsters)

    # Touche l'ennemi
    def get_hit(self, monsters_list):
        for monster in monsters_list:
            if self.rect.colliderect(monster.rect):
                monster.health -= self.attack_dmg
                if monster.health <= 0:
                    monster.kill()
                    del monster

    #Image par defaut
    def default_img(self): self.image = self.get_image(0, 0, self.sprite_sheet_default)

    # Perd
    def game_over(self): print("You lost (noob)"); pygame.quit(); exit()

    # Update la position
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    # Reviens en arrière
    def move_back(self):
        self.position       = self.old_pos
        self.rect.topleft   = self.position
        self.feet.midbottom = self.rect.midbottom

    # Animation de base
    def get_image(self, x, y, sheet):
        image = pygame.Surface([64, 64])
        image.blit(sheet, (0, 0), (x, y, 64, 64))
        image.set_colorkey([0, 0, 0])
        return image

    # Animation pour courir
    def run_update(self):
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites_run):
            self.current_sprite = 0

        pressed = pygame.key.get_pressed()
        self.image = self.sprites_run[int(self.current_sprite)]

        if pressed[pygame.K_a]:
            return pygame.transform.flip(self.image, True, False)
        else:
            return self.image


    # Animation d'attaque 1
    def attack1_update(self):
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites_attack_1):
            self.current_sprite = 0

        self.image = self.sprites_attack_1[int(self.current_sprite)]

        return self.image

    # Animation d'attaque 2
    def attack2_update(self):
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites_attack_2) - 1:
            self.current_sprite = 0

        self.image = self.sprites_attack_1[int(self.current_sprite)]

        return self.image

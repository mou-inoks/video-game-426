import pygame
import time

import pygame.image


class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y, monster):
        
        super().__init__()
        self.sprites_run = []
        self.sprites_idle = []
        self.sprites_attack = []
        if "GOBLIN" in str(monster).upper():
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Goblin/run/Gob_Run_1.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Goblin/run/Gob_Run_2.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Goblin/run/Gob_Run_3.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Goblin/run/Gob_Run_4.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Goblin/run/Gob_Run_5.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Goblin/run/Gob_Run_6.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Goblin/run/Gob_Run_7.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Goblin/run/Gob_Run_8.png'))
            
            self.sprites_idle.append(pygame.image.load('../zip/Personnages/Goblin/Idle/Gob_idle_1.png'))
            self.sprites_idle.append(pygame.image.load('../zip/Personnages/Goblin/Idle/Gob_idle_2.png'))
            self.sprites_idle.append(pygame.image.load('../zip/Personnages/Goblin/Idle/Gob_idle_3.png'))

            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Goblin/attack/Gob_Attack_1.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Goblin/attack/Gob_Attack_2.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Goblin/attack/Gob_Attack_3.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Goblin/attack/Gob_Attack_4.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Goblin/attack/Gob_Attack_5.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Goblin/attack/Gob_Attack_6.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Goblin/attack/Gob_Attack_7.png'))

        elif "SKELETON" in str(monster).upper():
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Skeleton/run/Skel_Walk_1.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Skeleton/run/Skel_Walk_2.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Skeleton/run/Skel_Walk_3.png'))
            self.sprites_run.append(pygame.image.load('../zip/Personnages/Skeleton/run/Skel_Walk_4.png'))

            self.sprites_idle.append(pygame.image.load('../zip/Personnages/Skeleton/Idle/Skel_Idle_1.png'))
            self.sprites_idle.append(pygame.image.load('../zip/Personnages/Skeleton/Idle/Skel_Idle_2.png'))
            self.sprites_idle.append(pygame.image.load('../zip/Personnages/Skeleton/Idle/Skel_Idle_3.png'))
            self.sprites_idle.append(pygame.image.load('../zip/Personnages/Skeleton/Idle/Skel_Idle_4.png'))

            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Skeleton/attack/Skel_Attack_1.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Skeleton/attack/Skel_Attack_2.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Skeleton/attack/Skel_Attack_3.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Skeleton/attack/Skel_Attack_4.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Skeleton/attack/Skel_Attack_5.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Skeleton/attack/Skel_Attack_6.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Skeleton/attack/Skel_Attack_7.png'))
            self.sprites_attack.append(pygame.image.load('../zip/Personnages/Skeleton/attack/Skel_Attack_8.png'))

        self.current_sprite = 0

        self.x = x
        self.y = y
        
        self.image = self.sprites_idle
        self.image = self.idle_update()
        self.rect = self.image.get_rect()
        self.health = 100
        self.max_health = 100
        self.attack_dmg = 10
        self.position = [x,y]
        self.speed = 5
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_pos = self.position.copy()
        self.hitbox = [x + 15, y + 2, 60]

    #Enregistre la position du joueur
    def save_loc(self):self.old_pos = self.position.copy()

    #Se rend à droite
    def move_right(self) : self.position[0] += self.speed ; self.image = self.run_update()

    #Se rend à gauche
    def move_left(self)  : self.position[0] -= self.speed ; self.image = self.run_update()

    #Se rend en haut
    def move_up(self)    : self.position[1] -= self.speed ; self.image = self.run_update()

    #Se rend en bas
    def move_down(self)  : self.position[1] += self.speed ; self.image = self.run_update()

    #Attaque
    def attack(self, player)     :                          self.image = self.attack_update(); self.get_hit(player)


    #Update le hit, si le joueur touche
    def get_hit(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= self.attack_dmg
            if player.health <= 0:
                player.kill()
                player.game_over()
                del player

    # Image par defaut quand aucune animation n'est trigger
    def default_img(self): self.image = self.get_image(0, 0, self.sprite_sheet_default)

    # Update la position
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    #Permet au monstre de retourner en arrière
    def move_back(self):
        self.position       = self.old_pos
        self.rect.topleft   = self.position
        self.feet.midbottom = self.rect.midbottom

    # Render l'image comme il faut
    def get_image(self, x, y, sheet):
        image = pygame.Surface([64, 64])
        image.blit(sheet, (0, 0), (x, y, 64, 64))
        image.set_colorkey([0, 0, 0])
        return image

    # Animation de run
    def run_update(self):
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites_run):
            self.current_sprite = 0

        self.image = self.sprites_run[int(self.current_sprite)]

        return self.image

    # Animation d'idle
    def idle_update(self):
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites_idle):
            self.current_sprite = 0

        self.image = self.sprites_idle[int(self.current_sprite)]

        return self.image

    # Animation d'attaque
    def attack_update(self):
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites_attack):
            self.current_sprite = 0

        self.image = self.sprites_attack[int(self.current_sprite)]

        return self.image
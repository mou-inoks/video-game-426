from turtle import Screen
import pygame 
import pytmx
import pyscroll
from monster import Monster
from player import Player
import random, time

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800)) # Ne pas toucher
        self.current_round = 0

        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("../tiled/Map_foret.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #Genere un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == "Collision":
                self.walls.append(pygame.Rect(obj.x,obj.y, obj.width, obj.height))

        # dessiner les calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        self.rounds = {
            1: "1:1",
            2: "2:2",
            3: "4:3",
        }

        self.rounds_status = {
            1: False,
            2: False,
            3: False,
        }
    # Trigger l'input
    def handle_input(self):

        pressed = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if   pressed[pygame.K_w] : self.player.move_up()
        elif pressed[pygame.K_s] : self.player.move_down()
        elif pressed[pygame.K_d] : self.player.move_right()
        elif pressed[pygame.K_a] : self.player.move_left()
        elif mouse_buttons[0]    : self.player.attack(self.monsters); self.update()
        elif mouse_buttons[2]    : self.player.attack2(self.monsters) ; self.update()
        elif not True in pressed : self.player.default_img()

    # Update les images
    def update(self):
        self.group.update()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    # Crée un squelette
    def create_skeleton(self):
        monster = Monster(random.randint(200,500), random.randint(100,400), "Skeleton")
        self.group.add(monster)
        pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (monster.x + 15, monster.y + 10, monster.health, 10))
        return monster

    # Crée un goblin
    def create_goblin(self):
        monster = Monster(random.randint(150,500), random.randint(100,400), "Goblin")
        self.group.add(monster)
        return monster



    # Fin du jeu
    def end(self):
        global run
        victory = pygame.image.load('../zip/victoire-royal.png')
        self.screen.blit(victory, (30,50))
        pygame.display.update()
        time.sleep(10)
        exit()
   
    # Vérifie le round en cours
    def check_round(self, current):
        if not "Monster" in str(self.group.sprites()):
            self.rounds_status[current] = True

    # Les ennemies suivent le joueur
    def automatize(self, monster):
        if self.player.rect.x < monster.rect.x:
            monster.move_left()
        elif self.player.rect.x > monster.rect.x:
            monster.move_right()
        if self.player.rect.y > monster.rect.y:
            monster.move_down()
        elif self.player.rect.y < monster.rect.y:
            monster.move_up()
        elif self.player.rect.x - monster.rect.x <= 100:
            monster.attack(self.player)

    # Charge les monstres
    def load_monsters(self, round):
        self.Skel = []
        self.Gobl = []
        self.monsters = []

        nb_skeleton, nb_goblin = self.rounds[round].split(":")

        for _ in range(int(nb_skeleton)):
            monster = self.create_skeleton()
            self.Skel.append(monster)
            self.monsters.append(monster)

        for _ in range(int(nb_goblin)):
            monster = self.create_goblin()
            self.Gobl.append(monster)
            self.monsters.append(monster)

    # Sauvegarde localement la position des monstres
    def save_local(self):
        for Skeleton in self.Skel:
            Skeleton.save_loc()

        for Goblin in self.Gobl:
            Goblin.save_loc()
        self.player.save_loc()

    # Boucle pour que le jeu tourne
    def run(self):

        clock = pygame.time.Clock()
        self.load_monsters(1)

        self.current_round = 1

        iteration = 0

        run = True
        while run:

            self.check_round(self.current_round)
            pygame.display.set_caption(f"Escape of the Horde | Health: [{self.player.health}/100] | Round : [{self.current_round}/3]")
            iteration += 1

            if self.rounds_status[3]:
                self.end()
            elif self.rounds_status[self.current_round]:
                self.current_round += 1
                self.load_monsters(self.current_round)

            if iteration == 10:
                iteration = 0
                for monster in self.Skel:
                    self.automatize(monster)

                for monster in self.Gobl:
                    self.automatize(monster)

            self.save_local()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            clock.tick(60)
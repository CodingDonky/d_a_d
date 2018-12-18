import pygame, sys, os
ENV_DIR = os.environ['ENV_DIR']
sys.path.append(ENV_DIR+'src/utilities/')
from NPC import *
from beings import *

pygame.init()

class Player:

    def __init__(self, name):
        self.name = name
        self.stats = Stats(name="Zombie")
        self.facing = "north"
        self.health = 100

        sprite = pygame.image.load(os.path.join(ENV_DIR,"resources","graphics","player.png"))
        size = sprite.get_size()
        self.width = size[0]
        self.height = size[1]
        self.X = 0
        self.Y = 0

        # Get Player Faces
        self.faces = get_faces(sprite)

    def render(self, surface, pos):
        surface.blit( self.faces[ self.facing ], pos )

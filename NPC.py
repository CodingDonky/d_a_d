import pygame, os, sys, random, math
ENV_DIR = os.environ['ENV_DIR']
sys.path.append(ENV_DIR+'src/utilities/')
from timer import *
from globals import *
from z_map_data import *

pygame.init()

def get_faces(sprite):
    faces = {}
    size = sprite.get_size()
    tile_size = (int(size[0] / 2), int(size[1] / 2))

    # Get Player Faces
    south = pygame.Surface(tile_size, pygame.HWSURFACE|pygame.SRCALPHA)
    south.blit(sprite, (0,0), ( 0, 0, tile_size[0], tile_size[1]))
    faces["south"] = south
    north = pygame.Surface(tile_size, pygame.HWSURFACE|pygame.SRCALPHA)
    north.blit(sprite, (0,0), ( tile_size[0], tile_size[1], tile_size[0], tile_size[1]))
    faces["north"] = north
    west = pygame.Surface(tile_size, pygame.HWSURFACE|pygame.SRCALPHA)
    west.blit(sprite, (0,0), ( tile_size[0], 0, tile_size[0], tile_size[1]))
    faces["west"] = west
    east = pygame.Surface(tile_size, pygame.HWSURFACE|pygame.SRCALPHA)
    east.blit(sprite, (0,0), ( 0, tile_size[1], tile_size[0], tile_size[1]))
    faces["east"] = east

    return faces

def MoveNPC(npc):
    npc.facing = random.choice(('north','south','east','west'))
    npc.walking = random.choice((True,False))

class NPC(object):
    AllNPCs = []

    def __init__(self, name, pos, dialog, sprite):
        self.Name = name
        self.X = pos[0]
        self.Y = pos[1]
        self.Dialog = dialog
        self.width = sprite.get_width()
        self.height = sprite.get_height()
        self.walking = False
        self.Timer = Timer(interval=50)
        self.Timer.OnNext
        # lambda indicates that MoveNPC DOES NOT RETURN ANYTHING,  just sets a variable
        self.Timer.OnNext = lambda: MoveNPC(self)
        self.Timer.Start()

        self.LastLocation = [0,0]

        # GET N PC FACE
        self.facing = "south"
        self.faces = get_faces(sprite)

        NPC.AllNPCs.append(self)

    def Render(self, surface):
        self.Timer.Update()
        if self.walking:
            move_speed = 1 * Globals.deltatime

            if self.facing == "south":
                if not Tiles.Blocked_At( (round(self.X/Tiles.Size),math.ceil(self.Y/Tiles.Size)) ):
                    self.Y += move_speed
            if self.facing == "north":
                if not Tiles.Blocked_At( (round(self.X/Tiles.Size),math.floor(self.Y/Tiles.Size)) ):
                    self.Y -= move_speed
            if self.facing == "east":
                if not Tiles.Blocked_At( (math.ceil(self.X/Tiles.Size),round(self.Y/Tiles.Size)) ):
                    self.X += move_speed
            if self.facing == "west":
                if not Tiles.Blocked_At( (math.floor(self.X/Tiles.Size),round(self.Y/Tiles.Size)) ):
                    self.X -= move_speed

            # Add currently occupied block as blocked
            location = [ round(self.X/Tiles.Size), round(self.Y/Tiles.Size) ]
            if self.LastLocation in Tiles.Blocked:
                Tiles.Blocked.remove(self.LastLocation)

            if not location in Tiles.Blocked:
                #Tiles.Blocked.append(location)
                self.LastLocation = location

        surface.blit(self.faces[self.facing], (self.X + Globals.camera_x, self.Y + Globals.camera_y))

class Male1(NPC):

    def __init__(self, name, pos, dialog = None):
        # super(subClass, instance).method(args)
        super(Male1,self).__init__(name, pos, dialog, pygame.image.load(os.path.join(\
            ENV_DIR,"resources","graphics","npc1.png")))
        location = [ round(self.X/Tiles.Size), round(self.Y/Tiles.Size) ]
        self.LastLocation = location
        #Tiles.Blocked.append(location)

class Demon1(NPC):

    def __init__(self, name, pos, dialog = None):
        # super(subClass, instance).method(args)
        super(Demon1,self).__init__(name, pos, dialog, pygame.image.load(os.path.join(\
            ENV_DIR,"resources","graphics","demon1.png")))
        location = [ round(self.X/Tiles.Size), round(self.Y/Tiles.Size) ]
        self.LastLocation = location
        #Tiles.Blocked.append(location)
        #print Tiles.Blocked



#

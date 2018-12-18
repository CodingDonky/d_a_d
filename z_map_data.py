import pygame, os, math
import numpy as np
from globals import *
ENV_DIR = os.environ['ENV_DIR']

pygame.init()

class Tile():
    def __init__( self, tile_code, x, y, impassable=False ):
        self.tile_code = tile_code
        self.x = x
        self.y = y
        self.impassable = impassable


class Tiles:
    Size = 32

    Blocked = []
    Blocked_Types = ["3"]

    @staticmethod
    def Blocked_At(pos):
        if list(pos) in Tiles.Blocked:
            return True
        else:
            return False

    def Load_Texture(file, Size):
        bitmap = pygame.image.load(file)
        bitmap = pygame.transform.scale(bitmap, (Size, Size))
        surface = pygame.Surface((Size, Size), pygame.HWSURFACE|pygame.SRCALPHA)
        surface.blit(bitmap, (0, 0))
        return surface

    Grass = Load_Texture(ENV_DIR+"/resources/textures/grass.png",Size)
    Stone = Load_Texture(ENV_DIR+"/resources/textures/stone.png",Size)
    Water = Load_Texture(ENV_DIR+"/resources/textures/water.png",Size)

    Texture_Tags = {"1": Grass, "2": Stone, "3": Water}

class Map_Engine:

    @staticmethod
    def render_tile(tile, pos, addTo):
        addTo.blit(tile, (pos[0] * Tiles.Size, pos[1] * Tiles.Size))

    @staticmethod
    def load_map_from_file( file, as_matrix=False ):
        with open(file, "r") as mapfile:
            map_data = mapfile.read()

            # Read Tile Data
            map_data = map_data.split(":") # Splits into list of tiles
            map_size = map_data[len(map_data)-1] # Get map dimensions
            map_data.remove(map_size) # Now list only contains tiles
            map_size = map_size.split(",")
            map_size_tiles = map_size
            map_dim_x = int(map_size[0])
            map_dim_y = int(map_size[1])
            map_size[0] = map_dim_x * Tiles.Size
            map_size[1] = map_dim_y * Tiles.Size

            tiles = []

            for tile in range(len(map_data)):
                map_data[tile] = map_data[tile].replace("\n","")
                tiles.append(map_data[tile].split("_")) # Split position from texture

            for tile in tiles:
                tile[0] = tile[0].split(",") # Split pos into a list
                pos = tile[0]
                for p in pos:
                    try:
                        pos[pos.index(p)] = int(p)  # Convert to integer
                    except Exception as e:
                        print e

                tiles[tiles.index(tile)] = (pos,tile[1])

            # Create and pre-load Terrain
            terrain = pygame.Surface(map_size, pygame.HWSURFACE)

            for tile in tiles:
                if tile[1] in Tiles.Texture_Tags:
                    Map_Engine.render_tile(Tiles.Texture_Tags[tile[1]], tile[0], terrain)

                if tile[1] in Tiles.Blocked_Types:
                    Tiles.Blocked.append(tile[0])

            # RETURNS MAP AS A MATRIX
            if as_matrix:
                # map_matrix = np.empty([map_dim_x, map_dim_y], dtype=object)
                map_matrix = np.empty([map_dim_x+1, map_dim_y+1], dtype=object)
                for tile in tiles:
                    coordinates = tile[0]
                    try:
                        x = coordinates[0]
                        y = coordinates[1]
                        tile_code = tile[1]
                        map_matrix[x,y] = Tile( tile_code=tile_code, x=x, y=y, impassable=(tile[1] in Tiles.Blocked_Types))
                    except Exception as e:
                        print e
                        continue

                return map_matrix
            # RETURN AS PYGAME THING
            else:
                return terrain

    @staticmethod
    def load_map_from_matrix():
        length, width = Globals.map_matrix.shape
        terrain = pygame.Surface([length*Globals.tile_size, width*Globals.tile_size], pygame.HWSURFACE)

        for x in range(0,length):
            for y in range(0,width):
                pos = [x,y]
                try:
                    tile_code = str(int( Globals.map_matrix[x,y].tile_code ))
                except Exception as e:
                    tile_code = str(Globals.map_matrix[x,y].tile_code )
                Map_Engine.render_tile(Tiles.Texture_Tags[tile_code], pos, terrain)
        return terrain

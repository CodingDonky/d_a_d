import math



class Globals:
    turn_list = []

    camera_x = 0
    camera_y = 0
    camera_move = 0

    # scene = combat / roam / menu /inventory
    scene = "roam"

    deltatime = 0

    map_matrix = None
    tile_size = 32

def pixels_to_coors( x, y ):
    x_coor = int( math.floor( x/Globals.tile_size ) )
    y_coor = int( math.floor( y/Globals.tile_size ) )
    return [x_coor, y_coor]

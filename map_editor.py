import pygame, os, sys, math
ENV_DIR = os.environ['ENV_DIR']
sys.path.append(ENV_DIR+'src/utilities/')
from color_vals import *
from textures import *

print("Press P: to save map")
print("Press 1: to use grass")
print("Press 2: to use stone")
print("Press 3: to use water")
print("")

def export_map(file):
    map_data = ""

    # Get Map Dimensions
    max_x = 0
    max_y = 0

    for t in tile_data:
        if t[0] > max_x:
            max_x = t[0]
        if t[1] > max_y:
            max_y = t[1]

    # Save map Tiles
    for tile in tile_data:
        map_data = map_data + str(int( tile[0]/Tiles.Size )) + "," + \
                    str(int( tile[1]/Tiles.Size )) + "_" + tile[2] + ":"

    # Save map dimensions
    map_data = map_data + str(int(max_x/Tiles.Size)) + "," + str(int(max_y/Tiles.Size))

    # Write Map file
    with open(file, "w") as mapfile:
        mapfile.write(map_data)

def load_map(file):
    global tile_data
    with open(file,"r") as mapfile:
        map_data = mapfile.read()

    # Read Tile Data
    map_data = map_data.split(":") # Splits into list of tiles
    map_size = map_data[len(map_data)-1] # Get map dimensions
    map_data.remove(map_size) # Now list only contains tiles
    map_size = map_size.split(",")
    map_size_tiles = map_size
    map_size[0] = int(map_size[0]) * Tiles.Size
    map_size[1] = int(map_size[1]) * Tiles.Size

    tiles = []

    for tile in range(len(map_data)):
        map_data[tile] = map_data[tile].replace("\n","")
        tiles.append(map_data[tile].split("_")) # Split position from texture

    for tile in tiles:
        tile[0] = tile[0].split(",") # Split pos into a list
        pos = tile[0]
        for p in pos:
            pos[pos.index(p)] = int(p)  # Convert to integer

        tiles[tiles.index(tile)] = [pos[0]*Tiles.Size, pos[1]*Tiles.Size, tile[1]]
    tile_data = tiles

isRunning = True
window = pygame.display.set_mode((1280,720), pygame.HWSURFACE)
pygame.display.set_caption("Map Editor")
clock = pygame.time.Clock()

txt_font = pygame.font.Font(ENV_DIR+'resources/fonts/DroidSans.ttf',20)

mouse_pos = 0
mouse_x, mouse_y = 0, 0
camera_move = 0
camera_x, camera_y = 0, 0

map_width, map_height = 30*Tiles.Size, 20*Tiles.Size

selector = pygame.Surface((Tiles.Size, Tiles.Size), pygame.HWSURFACE|pygame.SRCALPHA)
selector.fill(Color.WithAlpha(100,Color.CornflowerBlue)) # alpha from 0-255

tile_data = []

brush = "1"

# Initialize default map
for x in range(0, map_width, Tiles.Size):
    for y in range(0, map_height, Tiles.Size):
        tile_data.append([x,y,"1"])


while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        # MOVEMENT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                camera_move = 1
            elif event.key == pygame.K_s:
                camera_move = 2
            elif event.key == pygame.K_a:
                camera_move = 3
            elif event.key == pygame.K_d:
                camera_move = 4

            # BRUSHES
            if event.key == pygame.K_r:
                print "r"
                brush = "r"
            if event.key == pygame.K_t:
                selection = input("Brush Tag: ")
                brush = selection
            if event.key == pygame.K_1:
                brush = "1"
            if event.key == pygame.K_2:
                brush = "2"
            if event.key == pygame.K_3:
                brush = "3"

            # SAVE MAP
            if event.key == pygame.K_p:
                print('SAVING MAP')
                name = raw_input("Map Name: ")
                if name!='q':
                    export_map(os.path.join(ENV_DIR,'resources','maps',name+".map"))
                    print("Map saved successfully!")
            # LOAD MAP
            if event.key == pygame.K_o:
                print('LOADING MAP')
                name = raw_input("Map Name: ")
                if name!='q':
                    load_map(os.path.join(ENV_DIR,'resources','maps',name+".map"))
                    print("Map loaded successfully!")

        if event.type == pygame.KEYUP:
            camera_move = 0



        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = math.floor( mouse_pos[0]/Tiles.Size ) * Tiles.Size
            mouse_y = math.floor( mouse_pos[1]/Tiles.Size ) * Tiles.Size

        if event.type == pygame.MOUSEBUTTONDOWN:
            tile = [mouse_x - camera_x, mouse_y - camera_y, brush]
            # Check if a tile is in this position
            found = False
            for t in tile_data:
                if t[0] == tile[0] and t[1] == tile[1]:
                    found = True
                    break
            if not found:
                if not brush == "r":
                    tile_data.append(tile)
            else:
                if brush == "r":
                    # Remove Tile
                    for t in tile_data:
                        if t[0] == tile[0] and t[1] == tile[1]:
                            tile_data.remove(t)
                            print("Tile Removed!")
                else:
                    print("A tile is already placed here!")



    # LOGIC
    if camera_move == 1:
        camera_y += Tiles.Size
    elif camera_move == 2:
        camera_y -= Tiles.Size
    elif camera_move == 3:
        camera_x += Tiles.Size
    elif camera_move == 4:
        camera_x -= Tiles.Size

    # RENDER GRAPHICS

    window.fill(Color.Blue)

    # Draw Map
    for tile in tile_data:
        try:
            window.blit(Tiles.Texture_Tags[tile[2]], \
            (tile[0] + camera_x, tile[1] + camera_y))
        except:
            pass

    # Draw Tile Highlight (Selector)
    window.blit(selector, (mouse_x, mouse_y) )


    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()

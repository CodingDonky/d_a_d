import pygame, sys, os, time, math
import numpy as np
ENV_DIR = os.environ['ENV_DIR']
sys.path.append(ENV_DIR+'src/utilities/')
from color_vals import *
from globals import *
from z_map_data import *
from player import *
from NPC import *
from meloonatic_gui import *

mapname = "test"

Globals.tile_size = Tiles.Size
pygame.key.set_repeat(1)
pygame.init()

cSec = 0
cFrame = 0
FPS = 0

mouse_pos = 0
mouse_x, mouse_y = 0, 0

# INIT EFFECTS
# selector = pygame.Surface((Tiles.Size, Tiles.Size), pygame.HWSURFACE|pygame.SRCALPHA)
selector = pygame.Surface((Tiles.Size/2, Tiles.Size/2), pygame.HWSURFACE|pygame.SRCALPHA)
selector.fill(Color.WithAlpha(100,Color.CornflowerBlue)) # alpha from 0-255

# INIT TERRAIN & MATRIX
# terrain = Map_Engine.load_map(file=os.path.join(ENV_DIR,'resources','maps',mapname+".map"), as_matrix=False)
Globals.map_matrix = Map_Engine.load_map_from_file( file=os.path.join(ENV_DIR,'resources','maps',mapname+".map"), as_matrix=True )
terrain = Map_Engine.load_map_from_matrix()

# INIT FONTS
fps_font = pygame.font.Font(ENV_DIR+'resources/fonts/DroidSans.ttf',20)

# INIT IMAGES
logo_img_temp = pygame.image.load(os.path.join(ENV_DIR,'resources','graphics','logo.png'))
#pygame.transform.scale(logo_img_temp, (239,176)) # Scales to (new_width, new_height)
logo_img = pygame.Surface(logo_img_temp.get_size(), pygame.HWSURFACE)
logo_img.blit(logo_img_temp, (0,0))
logo = Menu.Image(bitmap = logo_img)
del logo_img_temp
sky_temp = pygame.image.load("resources/textures/sky.png")
Sky = pygame.Surface(sky_temp.get_size(), pygame.HWSURFACE)
Sky.blit(sky_temp, (0,0))
del sky_temp


# Creates a window with spacified name and size
def create_window():
    global window, window_height, window_width, window_title
    window_width, window_height = 800, 600
    window_title = "Python Game 1"
    pygame.display.set_caption(window_title)
    window = pygame.display.set_mode(\
    (window_width,window_height),pygame.HWSURFACE|pygame.DOUBLEBUF)

def count_fps( show_fps=True ):
    global cSec, cFrame, FPS
    if show_fps:
        fps_overlay = fps_font.render(str(FPS), True, Color.Goldenrod)
        # window.blt( , POSITION )
        window.blit(fps_overlay, (0,0))
    # time.strftime("%S") returns the Second of the current time
    if cSec == time.strftime("%S"):
        cFrame += 1
    else:
        FPS = cFrame
        cFrame = 0
        cSec = time.strftime("%S")
        if FPS > 0:
            Globals.deltatime = 20.0 / FPS

# INIT WINDOW
create_window()
isRunning = True
# INIT MUSIC
# pygame.mixer.music.load( os.path.join(ENV_DIR,'resources','music',"title.wav") )
# pygame.mixer.music.play(-1) # loop x times, infinite if negative number!
# INIT SOUNDS
btnSound = pygame.mixer.Sound( os.path.join(ENV_DIR,'resources','sounds',"click.wav") )

# INIT PLAYER
player = Player("GABO")
player_w, player_h = player.width, player.height
player_move = 0
player_x = 100+(window_width/2 - player_w/2 - Globals.camera_x) #/ Tiles.Size
player_y = (window_height/2 - player_h/2 - Globals.camera_y) # / Tiles.Size
player_x = 33
player_y = 33
player_x_coor, player_y_coor= pixels_to_coors( player_x, player_y )
camera_follows_player = True
print "Player Starts:"
print player_x, player_y
print "In COORDINATE Form:"
print player_x_coor, player_y_coor

# INIT NPCs
man1 = Male1(name = "bob", pos = (200,300))
man2 = Male1(name = "byb", pos = (400,340))
man3 = Male1(name = "bap", pos = (140,770))
man4 = Male1(name = "bvb", pos = (220,100))
man5 = Male1(name = "beb", pos = (320,200))
man6 = Male1(name = "beeb", pos = (35,50))
man7 = Male1(name = "boub", pos = (37,40))
man8 = Male1(name = "bueb", pos = (55,55))
man9 = Male1(name = "byub", pos = (66,66))
demon1 = Demon1(name="Carth", pos = (820,540))

# INIT GUI FUNTIONS
def Play():
    Globals.scene = "roam"
    pygame.mixer.music.load( os.path.join(ENV_DIR,'resources','music',"forest.wav") )
    pygame.mixer.music.play(-1) # loop x times, infinite if negative number!
def Exit():
    global isRunning
    isRunning = False
# INIT GUI
btnPlay = Menu.Button(text = "PLAY", rect = (20,20,160,60),# rect = (x,y,width,height)
                        bg = Color.Gray, fg = Color.White,
                        bgr = Color.CornflowerBlue, tag = ("menu",None))
btnPlay.Left = window_width/2 - btnPlay.Width/2
btnPlay.Top = window_height/2 - btnPlay.Height/2
btnPlay.Command = Play
btnExit = Menu.Button(text = "EXIT", rect = (20,200,160,60),# rect = (x,y,width,height)
                        bg = Color.Gray, fg = Color.White,
                        bgr = Color.CornflowerBlue, tag = ("menu",None))
btnExit.Left = window_width/2 - btnPlay.Width/2
btnExit.Command = Exit
menuTitle = Menu.Text(text = "WELCOME to TEST GAME", color=Color.Cyan, font = Font.Large)
camera_corr = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_move = 1
                player.facing = "north"
            elif event.key == pygame.K_s:
                player_move = 2
                player.facing = "south"
            elif event.key == pygame.K_a:
                player_move = 3
                player.facing = "west"
            elif event.key == pygame.K_d:
                player_move = 4
                player.facing = "east"
            elif event.key == pygame.K_q:
                isRunning = False
            elif event.key == 32: # SPACEBAR
                camera_follows_player = not camera_follows_player
        elif event.type == pygame.KEYUP:
            Globals.camera_move = 0
            player_move = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # LEFT CLICK
                # HANDLE BUTTON CLICK EVENTS
                for btn in Menu.Button.All:
                    if btn.Tag[0] == Globals.scene and btn.Rolling:
                        # If a command has been set on the button
                        if btn.Command != None:
                            btn.Command() # Do button EVENT
                        btnSound.play()
                        btn.Rolling = False
                        break
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x_coor, mouse_y_coor = pixels_to_coors( mouse_pos[0], mouse_pos[1] )
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]
            if camera_corr:
                camera_correction_x = (abs(Globals.camera_x)%32)*np.sign(Globals.camera_x)
                camera_correction_y = (abs(Globals.camera_y)%32)*np.sign(Globals.camera_y)
            else:
                camera_correction_x = 0
                camera_correction_y = 0
            mouse_x_quant = (math.floor( mouse_pos[0]/Tiles.Size ) * Tiles.Size) + camera_correction_x
            mouse_y_quant = (math.floor( mouse_pos[1]/Tiles.Size ) * Tiles.Size) + camera_correction_y
            # print "_________________________________________"
            # print "CAMERA pixels"
            # print Globals.camera_x, Globals.camera_y
            # print "MOUSE pixels"
            # print mouse_pos[0], mouse_pos[1]
            # print "CAMERA X correction"
            # print camera_correction_x
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = pixels_to_coors( mouse_pos[0]- Globals.camera_x, mouse_pos[1]- Globals.camera_y )
            # Check if a tile is in this position
            try:
                print "Clicked on coordinate: "
                print click_x, click_y
                # tile_clicked = Globals.map_matrix[click_x,click_y]
                # tile_clicked.tile_code = "3"
                # terrain = Map_Engine.load_map_from_matrix()
            except Exception as e:
                print(e)




    # RENDER SCENE
    if Globals.scene == "menu":
        window.fill(Color.Black)
        logo.Render(window, (150,0))
        menuTitle.Render(window)

        for btn in Menu.Button.All:
            if btn.Tag[0] == "menu":
                btn.Render(window)

    elif Globals.scene == "roam":

        # PLAYER MOVEMENT
        if not player_move == 0:
            move_distance = 10*Globals.deltatime
        if player_move == 1: # UP
            player_x_coor, player_y_coor = pixels_to_coors( player_x+(player.width/2), player_y-move_distance+(player.height/2)-15 )
            if not Tiles.Blocked_At( ( player_x_coor, player_y_coor ) ):
                player_y -= move_distance
        elif player_move == 2: # DOWN
            player_x_coor, player_y_coor = pixels_to_coors( player_x+(player.width/2), player_y+move_distance+(player.height/2) )
            if not Tiles.Blocked_At( ( player_x_coor, player_y_coor ) ):
                player_y += move_distance
        elif player_move == 3: # LEFT
            player_x_coor, player_y_coor = pixels_to_coors( player_x-move_distance+(player.width/2)-15, player_y+(player.height/2) )
            if not Tiles.Blocked_At( ( player_x_coor, player_y_coor ) ):
                player_x -= move_distance
        elif player_move == 4: # RIGHT
            player_x_coor, player_y_coor = pixels_to_coors( player_x+move_distance+(player.width/2), player_y+(player.height/2) )
            if not Tiles.Blocked_At( ( player_x_coor, player_y_coor ) ):
                player_x += move_distance

        # Center Camera on Player
        if camera_follows_player:
            Globals.camera_x = window_width/2 - player_x - player_w/2
            Globals.camera_y = window_height/2 - player_y - player_h/2

        # RENDER GRAPHICS
        window.blit(Sky, (0,0))
        window.blit(terrain, (Globals.camera_x, Globals.camera_y))


        window.blit(selector, (mouse_x-10, mouse_y-10) )
        # Render NPCs
        for npc in NPC.AllNPCs:
            npc.Render(window)
        # Render player
        player.render(window, (player_x+Globals.camera_x,player_y+Globals.camera_y))
        # player.render(window, (window_width/2 - player_w/2, window_height/2 - player_h/2))


    elif Globals.scene == "combat":

        print "yo"



    count_fps( show_fps=True )

    # Draws everything to the window
    pygame.display.update()

pygame.quit()
sys.exit()

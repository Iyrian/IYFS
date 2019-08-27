from os import path
from PIL import Image
from MoveObjs import Enemy
import gdata as g

def load_map(map_indx = 0):
    level = Image.open(path.join(path.dirname(__file__), 'map{}.png'.format(map_indx)))
    g.MAP_WIDTH = level.size[0]
    g.MAP_HEIGHT = level.size[1]
    g.MAP = [[0 for j in range(g.MAP_WIDTH)] for i in range(g.MAP_HEIGHT)]

    # Colors for level loading
    WALL_X = (0 ,0, 0)
    WALL_Y = (50, 50, 50)
    WALL_BRICK = (100, 100, 100)
    WALL_SPBRICK = (255, 255, 0)
    ENEMY = (255, 0, 0)
    MARIO = (0, 255, 0)
    DESTINATION = (0, 0, 255)
    # Read pixel data from level map and instantiate objects corresponding to pixel colors
    for y in range(0, level.size[1]):
        for x in range(0, level.size[0]):
            color = level.getpixel((x, y))
            if color == WALL_X:
                g.MAP[y][x] = g.MAP_ENUM_WALL_X 
            elif color == WALL_Y:
                g.MAP[y][x] = g.MAP_ENUM_WALL_Y 
            elif color == WALL_BRICK:
                g.MAP[y][x] = g.MAP_ENUM_BRICK
            elif color == WALL_SPBRICK:
                g.MAP[y][x] = g.MAP_ENUM_SPBRICK
            elif color == ENEMY:
                #add enemy here
                enemy = Enemy()
                enemy.stg_x = x * g.BLOCK_SIZE
                enemy.stg_y = y * g.BLOCK_SIZE
                g.enemies.append(enemy)
            elif color == MARIO:
                #set mario pos
                g.Mario.stg_x = x * g.BLOCK_SIZE
                g.Mario.stg_y = y * g.BLOCK_SIZE
            elif color == DESTINATION:
                g.DST_STGX = x * g.BLOCK_SIZE
                g.DST_STGY = y * g.BLOCK_SIZE
    return
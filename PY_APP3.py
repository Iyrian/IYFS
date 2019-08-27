import gdata as g
from MoveObjs import Enemy, Mushroom
from Mario import Mario
from Population import Population
from drawMap import load_map
import pygame as pg
import os
import time
def CAMERA_MOVE(stg_x):
    if g.TRANSX_STG_TO_SCN(stg_x) < 0.5 * g.SCN_WIDTH:
        g.camera_rcd_stg_x = stg_x
        return
    if g.camera_rcd_stg_x != stg_x:
        dlt = stg_x - g.camera_rcd_stg_x
        g.CAMERA_STGX += dlt
        if g.CAMERA_STGX < 0.0:
            g.CAMERA_STGX = 0.0
        elif g.CAMERA_STGX > g.MAP_WIDTH * g.BLOCK_SIZE - g.SCN_WIDTH:
            g.CAMERA_STGX = g.MAP_WIDTH * g.BLOCK_SIZE - g.SCN_WIDTH
        g.camera_rcd_stg_x = stg_x
    return
def show_map():
    c_grdx = g.to_block_pos(g.CAMERA_STGX)
    shift_x = g.CAMERA_STGX - c_grdx  * g.BLOCK_SIZE
    scn_w = g.to_block_pos(g.SCN_WIDTH)
    scn_h = g.to_block_pos(g.SCN_HEIGHT)
    for i in range(scn_h):
        for j in range(scn_w):
            val = g.MAP[i][j + c_grdx]
            color = None
            if val == g.MAP_ENUM_BRICK:
                color = (100, 100, 100)
            elif val == g.MAP_ENUM_SPBRICK:
                color = (255, 255, 0)
            elif val == g.MAP_ENUM_WALL_X:
                color = (0, 0, 0)
            elif val == g.MAP_ENUM_WALL_Y:
                color = (0, 0, 0)
            else:
                color = g.SCN_BACKCOLOR
            pg.draw.rect(g.SCN_SURFACE, color,\
                         pg.Rect(j * g.BLOCK_SIZE - 0.5 * (g.BLOCK_SIZE - 1) - shift_x,\
                        i * g.BLOCK_SIZE - 0.5 * (g.BLOCK_SIZE - 1),\
                        g.BLOCK_SIZE - 1, g.BLOCK_SIZE - 1))
    return
def setup():
    g.Font_Big = pg.font.Font('Minecraft.ttf',32)
    g.Font_Small = pg.font.Font('Minecraft.ttf',16)
    #------------------------
    g.mushroom = Mushroom()
    g.mushroom.valid = False
    g.Mario = Mario()
    #------------------------
    load_map()
    return
def run(isAICtrl = False, isModelLoaded = False):
    pg.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d"%(0,30)
    g.SCN_SURFACE = pg.display.set_mode((g.SCN_WIDTH, g.SCN_HEIGHT),\
       pg.DOUBLEBUF)
    pg.display.set_caption("SimpleMario?")
    setup() 
    if not isAICtrl:
        best_score = 0
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
            #render----------------------
            g.SCN_SURFACE.fill(g.SCN_BACKCOLOR)
            show_map()
            if not g.Mario.dead:
                g.Mario.human_ctrl()
                g.Mario.show()
                CAMERA_MOVE(g.Mario.stg_x)
            else:
                dead = g.Font_Big.render(g.Mario.dead_reason, True, (255, 0, 0))
                g.SCN_SURFACE.blit(dead, (0.5 * (g.SCN_WIDTH - dead.get_rect().width), 0.5 * g.SCN_HEIGHT))
                if best_score < g.Mario.score:
                    best_score = g.Mario.score
            #renering digital sys-----------------------------------------------------------------
            score = g.Font_Small.render("BestScore<{}>".format(best_score), True, (0, 0, 0))
            g.SCN_SURFACE.blit(score, (1, 0))
            score = g.Font_Small.render("Score<{}>".format(g.Mario.score), True, (0, 0, 0))
            g.SCN_SURFACE.blit(score, (1, 24))
            #-------------------------------------------------------------------------------------
            if g.mushroom.valid:
                g.mushroom.update()
                g.mushroom.show()
            for i in range(len(g.enemies)):
                if not g.enemies[i].dead:
                    if g.enemies[i].in_screen():
                        g.enemies[i].update()
                        g.enemies[i].show()
            pg.display.flip()
            #----------------------------
    else:
        best_score = 0
        if not isModelLoaded:
            g.Pop = Population(g.POP_SIZE, g.POP_PM, g.POP_PC)
            g.Pop.init_pos(g.Mario.stg_x, g.Mario.stg_y)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
            #render----------------------
            g.SCN_SURFACE.fill(g.SCN_BACKCOLOR)
            show_map()
            if g.mushroom.valid:
                g.mushroom.update()
                g.mushroom.show()
            for i in range(len(g.enemies)):
                if not g.enemies[i].dead:
                    if g.enemies[i].in_screen():
                        g.enemies[i].update()
                        g.enemies[i].show()
            if not isModelLoaded:
                if g.Pop.done():
                    print("---------------------ALL DEAD---------------------")
                    g.Pop.generate_next()
                else:
                    g.Pop.update()
                    g.Pop.show()
                    if g.Pop.bestMario.dead:
                        dead = g.Font_Big.render(g.Pop.bestMario.dead_reason, True, (255, 0, 0))
                        g.SCN_SURFACE.blit(dead, (0.5 * (g.SCN_WIDTH - dead.get_rect().width), 0.5 * g.SCN_HEIGHT))
                    else:
                        CAMERA_MOVE(g.Pop.bestMario.stg_x)
                #renering digital sys-----------------------------------------------------------------
                generation = g.Font_Small.render("Generation<{}>".format(g.Pop.generation), True, (0, 0, 0))
                g.SCN_SURFACE.blit(generation, (1, 0))
                score = g.Font_Small.render("BestScore<{}>".format(g.Pop.bestScore), True, (0, 0, 0))
                g.SCN_SURFACE.blit(score, (1, 24))
                score = g.Font_Small.render("Score<{}>".format(g.Pop.bestMario.score), True, (0, 0, 0))
                g.SCN_SURFACE.blit(score, (1, 48))
                life_left = g.Font_Small.render("LifeLeft<{}>".format(g.Pop.bestMario.lifeLeft), True, (0, 0, 0))
                g.SCN_SURFACE.blit(life_left, (1, 72))
                #distance = g.Font_Small.render("DistanceLeft<{}>".format(g.Pop.bestMario.distance_left), True, (0, 0, 0))
                #g.SCN_SURFACE.blit(distance, (0, 96))
                #-------------------------------------------------------------------------------------
            else:
                if not g.Mario.dead:
                    g.Mario.think()
                    g.Mario.update()
                    g.Mario.show()
                    CAMERA_MOVE(g.Mario.stg_x)
                else:
                    dead = g.Font_Big.render(g.Mario.dead_reason, True, (255, 0, 0))
                    g.SCN_SURFACE.blit(dead, (0.5 * (g.SCN_WIDTH - dead.get_rect().width), 0.5 * g.SCN_HEIGHT))
                    time.sleep(5)
                    g.Mario = g.Mario.clone()
                    if best_score < g.Mario.score:
                        best_score = g.Mario.score
                #renering digital sys-----------------------------------------------------------------
                score = g.Font_Small.render("BestScore<{}>".format(best_score), True, (0, 0, 0))
                g.SCN_SURFACE.blit(score, (1, 0))
                score = g.Font_Small.render("Score<{}>".format(g.Mario.score), True, (0, 0, 0))
                g.SCN_SURFACE.blit(score, (1, 24))
                #-------------------------------------------------------------------------------------
            pg.display.flip()
            #----------------------------
    return
if __name__ == '__main__':
    run(True)
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
def restart():
    g.enemies = []
    g.mushroom = Mushroom()
    g.mushroom.valid = False
    load_map()
    g.CAMERA_STGX = 0.0
    return
#define button pos---------------------------------
button_width = 100
button_height = 22
button_save_x = g.SCN_WIDTH - button_width - 2
button_save_y = 2
button_save_as_y = button_save_y + 24
button_load_y = button_save_as_y + 24
#--------------------------------------------------
def run(isAICtrl = False, isModelLoaded = False):
    pg.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d"%(0,30)
    g.SCN_SURFACE = pg.display.set_mode((g.SCN_WIDTH, g.SCN_HEIGHT),\
       pg.DOUBLEBUF)
    pg.display.set_caption("SimpleMario?")
    setup() 
    t_save = g.Font_Small.render("Save", True, (0, 0, 0))
    t_save_as = g.Font_Small.render("Save As", True, (0, 0, 0))
    t_load = g.Font_Small.render("Load", True, (0, 0, 0))
    if not isAICtrl:
        best_score = 0
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if g.Mario.dead and event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        g.Mario = Mario()
                        restart()
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
            #time.sleep(0.010)
            #----------------------------
    else:
        best_score = 0
        cur_id = 0
        mario_score = 0
        distance_left = 0
        distance_moved = 0
        life_left = 0
        model_resurrect = 0
        if not isModelLoaded:
            g.Pop = Population(g.POP_SIZE, g.POP_PM, g.POP_PC)
            g.Pop.init_pos(g.Mario.stg_x, g.Mario.stg_y)
        else:
            g.Mario.brain.load()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.MOUSEBUTTONDOWN:  # 判断鼠标位置以及是否摁了下去。
                    pg.event.clear(pg.MOUSEBUTTONDOWN)
                    if button_save_x <= event.pos[0] <= button_save_x + button_width:
                        if button_save_y <= event.pos[1] <= button_save_y + button_height:#save
                            if not isModelLoaded:
                                if cur_id == 0:
                                    g.Pop.bestMario.brain.save()
                                else:
                                    g.Pop.marios[cur_id - 1].brain.save()
                            else:
                                g.Mario.brain.save()
                        elif button_save_as_y <= event.pos[1] <= button_save_as_y + button_height:#save as
                            if not isModelLoaded:
                                if cur_id == 0:
                                    g.Pop.bestMario.brain.save_as()
                                else:
                                    g.Pop.marios[cur_id - 1].brain.save_as()
                            else:
                                g.Mario.brain.save_as()
                        elif button_load_y <= event.pos[1] <= button_load_y + button_height:#load
                            if not isModelLoaded:
                                if cur_id == 0:
                                    g.Pop.bestMario.brain.load()
                                else:
                                    g.Pop.marios[cur_id - 1].brain.load()
                            else:
                                g.Mario.brain.load()
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
                if cur_id > len(g.Pop.marios):
                    print("\n---------------------ALL DEAD---------------------")
                    g.Pop.generate_next()
                    restart()
                    cur_id = 0
                else:
                    #g.Pop.update()
                    #g.Pop.show()
                    if cur_id == 0:
                        g.Pop.bestMario.think()
                        g.Pop.bestMario.update()
                        g.Pop.bestMario.show()
                        mario_score = g.Pop.bestMario.score
                        distance_moved = g.Pop.bestMario.distance_passed
                        distance_left = g.DST_STGX - g.Pop.bestMario.stg_x
                        life_left = g.Pop.bestMario.lifeLeft
                        if g.Pop.bestMario.dead:
                            print("No0. Mario Dead, Reason<{}>".format(g.Pop.bestMario.dead_reason))
                            #dead = g.Font_Big.render(g.Pop.bestMario.dead_reason, True, (255, 0, 0))
                            #g.SCN_SURFACE.blit(dead, (0.5 * (g.SCN_WIDTH - dead.get_rect().width), 0.5 * g.SCN_HEIGHT))
                            cur_id += 1
                            restart()
                        else:
                            CAMERA_MOVE(g.Pop.bestMario.stg_x)                       
                    else:
                        g.Pop.marios[cur_id - 1].think()
                        g.Pop.marios[cur_id - 1].update()
                        g.Pop.marios[cur_id - 1].show()
                        mario_score = g.Pop.marios[cur_id - 1].score
                        distance_moved = g.Pop.marios[cur_id - 1].distance_passed
                        distance_left = g.DST_STGX - g.Pop.marios[cur_id - 1].stg_x
                        life_left = g.Pop.marios[cur_id - 1].lifeLeft
                        if g.Pop.marios[cur_id - 1].dead:
                            print("No{}. Mario Dead, Reason<{}>".format(cur_id, g.Pop.marios[cur_id - 1].dead_reason))
                            #dead = g.Font_Big.render(g.Pop.marios[cur_id - 1].dead_reason, True, (255, 0, 0))
                            #g.SCN_SURFACE.blit(dead, (0.5 * (g.SCN_WIDTH - dead.get_rect().width), 0.5 * g.SCN_HEIGHT))
                            cur_id += 1
                            restart()
                        else:
                            CAMERA_MOVE(g.Pop.marios[cur_id - 1].stg_x)         
                #renering digital sys-----------------------------------------------------------------
                generation = g.Font_Small.render("Generation<{}>, No{}. Mario".format(g.Pop.generation, cur_id), True, (0, 0, 0))
                g.SCN_SURFACE.blit(generation, (1, 0))
                score = g.Font_Small.render("BestScore<{}>".format(g.Pop.bestScore), True, (0, 0, 0))
                g.SCN_SURFACE.blit(score, (1, 24))
                score = g.Font_Small.render("Score<{}>".format(mario_score), True, (0, 0, 0))
                g.SCN_SURFACE.blit(score, (1, 48))
                tlife_left = g.Font_Small.render("LifeLeft<{}>".format(life_left), True, (0, 0, 0))
                g.SCN_SURFACE.blit(tlife_left, (1, 72))
                distance = g.Font_Small.render("Moved<{}/km>".format(distance_moved), True, (0, 0, 0))
                g.SCN_SURFACE.blit(distance, (1, 96))
                distance = g.Font_Small.render("DistanceLeft<{}/km>".format(distance_left), True, (0, 0, 0))
                g.SCN_SURFACE.blit(distance, (1, 120))
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
                    if best_score < g.Mario.score:
                        best_score = g.Mario.score
                    model_resurrect += 1
                    if model_resurrect == 30:
                        g.Mario = g.Mario.clone()
                        restart()
                        model_resurrect = 0
                #renering digital sys-----------------------------------------------------------------
                score = g.Font_Small.render("BestScore<{}>".format(best_score), True, (0, 0, 0))
                g.SCN_SURFACE.blit(score, (1, 0))
                score = g.Font_Small.render("Score<{}>".format(g.Mario.score), True, (0, 0, 0))
                g.SCN_SURFACE.blit(score, (1, 24))
                distance = g.Font_Small.render("Moved<{}/km>".format(g.Mario.distance_passed), True, (0, 0, 0))
                g.SCN_SURFACE.blit(distance, (1, 48))
                distance = g.Font_Small.render("DistanceLeft<{}/km>".format(g.DST_STGX - g.Mario.stg_x), True, (0, 0, 0))
                g.SCN_SURFACE.blit(distance, (1, 72))
                #-------------------------------------------------------------------------------------
            #draw buttons---------------------
            pg.draw.rect(g.SCN_SURFACE, (0 , 0, 0), pg.Rect(button_save_x, button_save_y, button_width, button_height), 1)
            pg.draw.rect(g.SCN_SURFACE, (0 , 0, 0), pg.Rect(button_save_x, button_save_as_y, button_width, button_height), 1)
            pg.draw.rect(g.SCN_SURFACE, (0 , 0, 0), pg.Rect(button_save_x, button_load_y, button_width, button_height), 1)
            g.SCN_SURFACE.blit(t_save, (button_save_x + 8, button_save_y))
            g.SCN_SURFACE.blit(t_save_as, (button_save_x + 8, button_save_as_y))
            g.SCN_SURFACE.blit(t_load, (button_save_x + 8, button_load_y))
            pg.display.flip()
            #----------------------------
    return
if __name__ == '__main__':
    run(True, True)
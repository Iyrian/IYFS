import gdata as g
import pygame as pg
class MoveObject(object):
    def __init__(self):
        self.stg_x = 0
        self.stg_y = 0
        self.mv_x = -0.5
        self.mv_y = 0.0
        return
    def move(self):
        self.stg_x += self.mv_x
        gy = g.to_block_pos(self.stg_y + self.mv_y)
        gx = g.to_block_pos(self.stg_x)
        if g.MAP[gy + 1][gx] == 0:#falling
            self.stg_y += self.mv_y
            self.mv_y += g.GRAVITY
        else:
            if self.mv_y > 0.0:
                self.stg_y = gy * g.BLOCK_SIZE
                self.mv_y = 0.0
        if g.MAP[gy][gx + (1 if self.mv_x > 0.0 else -1)] != 0:
            self.mv_x = -self.mv_x
        return
class Enemy(MoveObject):#move left
    def __init__(self):
        self.stg_x = 0
        self.stg_y = 0
        self.mv_x = -0.5
        self.mv_y = 0.0
        self.dead = False
        return
    def move(self):
        MoveObject.move(self)
        if self.stg_y > g.SCN_HEIGHT - 2 * g.BLOCK_SIZE:
            self.dead = True
        if g.TRANSX_STG_TO_SCN(self.stg_x) < g.BLOCK_SIZE:
            self.dead = True
        return
    def in_screen(self):
        return g.TRANSX_STG_TO_SCN(self.stg_x) < g.SCN_WIDTH
    def update(self):
        self.move()
        if self.dead:
            self.stg_y = 2 * g.SCN_HEIGHT
    def show(self):
        pg.draw.rect(g.SCN_SURFACE, [255, 0, 255],\
           pg.Rect(g.TRANSX_STG_TO_SCN(self.stg_x) - 0.5 * (g.BLOCK_SIZE - 1),\
          self.stg_y - 0.5 * (g.BLOCK_SIZE - 1), g.BLOCK_SIZE - 1, g.BLOCK_SIZE - 1))
        return
class Mushroom(object):
    def __init__(self):
        self.stg_x = 0
        self.stg_y = 0
        self.mv_x = 1.0
        self.mv_y = 0.0
        self.valid = True
        return
    def in_screen(self):
        return g.TRANSX_STG_TO_SCN(self.stg_x) < g.SCN_WIDTH
    def move(self):
        MoveObject.move(self)
        if self.stg_y > g.SCN_HEIGHT - 2 * g.BLOCK_SIZE:
            self.valid = False
        return
    def update(self):
        self.move()
        if not self.valid:
            self.stg_y = 2 * g.SCN_HEIGHT
        return
    def show(self):
        pg.draw.rect(g.SCN_SURFACE, [0, 255, 0],\
           pg.Rect(g.TRANSX_STG_TO_SCN(self.stg_x) - 0.5 * (g.BLOCK_SIZE - 1),\
          self.stg_y - 0.5 * (g.BLOCK_SIZE - 1), g.BLOCK_SIZE - 1, g.BLOCK_SIZE - 1))
        return
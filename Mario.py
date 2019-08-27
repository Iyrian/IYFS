import gdata as g
from NeuroNetwork import NeuralNet
from MoveObjs import Mushroom
import math
import pygame as pg
from random import random
class Mario(object):
    def __init__(self):
        self.dead_reason = ""
        self.move_descision = ""

        self.spd = 1.5
        self.spd_y = 6
        self.stg_x = 0
        self.stg_y = 0.0
        self.dead = False
        self.mv_x = 0
        self.mv_y = 0
        self.jump = False
        self.extraLife = False

        self.score = 0
        self.lifeLeft = 100
        self.lifetime = 0
        self.fitness = 0
        
        self.unrivalled = 0

        self.distance_left = 1000000
        self.distance_passed = 0.0
        self.brain = NeuralNet(g.NN_INPUT_SIZE, g.NN_HIDDEN_SIZE, g.NN_OUTPUT_SIZE,\
            g.NN_HIDDENLAYER_NUM)

        self.vision = [0.0 for i in range(g.NN_INPUT_SIZE)]
        self.descision = [0.0 for i in range(g.NN_OUTPUT_SIZE)]
        return
    def clone(self):
        rst = Mario()
        rst.brain = self.brain.clone()
        return rst
    def crossover(self,parent):
        rst = Mario()
        rst.brain = self.brain.crossover(parent.brain)
        return rst
    def mutate(self, pm):
        self.brain.mutate(pm)
        return
    def calculate_fitness(self):
        self.fitness = ((10.0 * self.distance_passed) + (3.0 * self.lifetime)) * (10.0 * self.score + 1)
        return
    def look(self):
        add_to = self.look_in_direction(0.0)
        for i in range(9):
            self.vision[i] = add_to[i]
        add_to = self.look_in_direction(math.pi / 4.0)
        for i in range(9):
            self.vision[i + 9] = add_to[i]
        add_to = self.look_in_direction(math.pi / 2.0)
        for i in range(9):
            self.vision[i + 18] = add_to[i]
        add_to = self.look_in_direction(3.0 * math.pi / 4.0)
        for i in range(9):
            self.vision[i + 27] = add_to[i]
        add_to = self.look_in_direction(math.pi)
        for i in range(9):
            self.vision[i + 36] = add_to[i]
        add_to = self.look_in_direction(5.0 * math.pi / 4.0)
        for i in range(9):
            self.vision[i + 45] = add_to[i]
        add_to = self.look_in_direction(3.0 * math.pi / 2.0)
        for i in range(9):
            self.vision[i + 54] = add_to[i]
        add_to = self.look_in_direction(7.0 * math.pi / 4.0)
        for i in range(9):
            self.vision[i + 63] = add_to[i]
        return
    #angle : in arc
    def look_in_direction(self, angle):
        rst = [0.0] * 9
        x_rate = math.cos(angle)
        y_rate = math.sin(angle)
        for step in range(0, g.SCN_HEIGHT, 4):
            cur_x = self.stg_x + x_rate * step
            cur_y = self.stg_y + y_rate * step
            gy = g.to_block_pos(cur_y)
            gx = g.to_block_pos(cur_x)
            if gx < 0.0 or gy < 0.0:
                continue
            if gy > g.MAP_HEIGHT - 1 or gx > g.MAP_WIDTH - 1:
                continue
            if g.MAP[gy][gx] == g.MAP_ENUM_SPBRICK:
                rst[0] = 1.0
                if rst[5] == 0.0:
                    rst[5] = step
            elif g.MAP[gy][gx] == g.MAP_ENUM_WALL_X:
                rst[1] = 1.0
                if rst[6] == 0.0:
                    rst[6] = step
            elif g.MAP[gy][gx] == g.MAP_ENUM_WALL_Y:
                rst[2] = 1.0
                if rst[7] == 0.0:
                    rst[7] = step
            if g.mushroom != None:
                if g.check_collide(self.stg_x, self.stg_y, g.mushroom.stg_x, g.mushroom.stg_y):
                    rst[3] = 1.0
                    if rst[8] == 0.0:
                        rst[8] = step
            #enemies
            distance = 10000.0
            for j in range(len(g.enemies)):
                dx = g.enemies[j].stg_x - self.stg_x
                dy = g.enemies[j].stg_y - self.stg_y
                dst = math.sqrt(dx ** 2 + dy ** 2)
                if dst < distance:
                    rst[4] = dst
                    distance = dst
        return rst
    #look,grep inputs
    #trans to NN
    #grep NN output and perform it
    #check self state
    def think(self):
        #grep NN input
        self.look()
        #grep NN output
        self.descision = self.brain.output(self.vision)
        if self.descision[0] < self.descision[1]:#move left
            self.mv_x = -self.spd
            self.move_descision = "LEFT"
        else:
            self.mv_x = self.spd
            self.move_descision = "RIGHT"
        if self.descision[2] < self.descision[3]:
            if not self.jump:
                self.jump = True
                self.mv_y = -self.spd_y
                self.move_descision += "-JUMP"
        return
    def update(self):       
        self.distance_passed += abs(self.mv_x)
        self.mv_y += g.GRAVITY
        #collision judge:
        bid_y = g.to_block_pos(self.stg_y + self.mv_y)
        bid_x = g.to_block_pos(self.stg_x + self.mv_x) + (1 if self.mv_x > 0.0 else -1)
        val = g.MAP[bid_y][bid_x]
        if val == 0:
            self.stg_x += self.mv_x
            #self.stg_x = g.to_block_pos(self.stg_x) * g.BLOCK_SIZE
        else:
            self.stg_x = g.to_block_pos(self.stg_x + self.mv_x) * g.BLOCK_SIZE
            self.mv_x = 0.0
        if g.TRANSX_STG_TO_SCN(self.stg_x) < 0.0:
            self.stg_x = g.TRANSX_SCN_TO_STG(0.0)
            #self.stg_x = g.to_block_pos(self.stg_x) * g.BLOCK_SIZE
        val = g.MAP[g.to_block_pos(self.stg_y + self.mv_y) + 1][g.to_block_pos(self.stg_x)] #检查地面
        on_ground = False
        if val != 0:
            if self.mv_y > 0.0:
                self.stg_y = g.to_block_pos(self.stg_y + self.mv_y) * g.BLOCK_SIZE
                self.mv_y = 0.0
            self.jump = False
            on_ground = True

        if self.stg_y < 0.0:
            self.stg_y = 0.0
            self.mv_y = 0.0
        #---------------------------------------------------------------------
        #collide special block---------------------------------------------------------------------
        val = g.MAP[g.to_block_pos(self.stg_y) - 1][g.to_block_pos(self.stg_x)] #检查头顶
        if val == g.MAP_ENUM_SPBRICK:
            g.MAP[g.to_block_pos(self.stg_y) - 1][g.to_block_pos(self.stg_x)] = g.MAP_ENUM_WALL_X
            if self.mv_y < 0.0:
                self.mv_y = 0.0
                self.stg_y = g.to_block_pos(self.stg_y) * g.BLOCK_SIZE
            #add mushroom
            if (not g.mushroom.valid) and random() < g.MUSHROOM_PSB:
                g.mushroom = Mushroom()
                g.mushroom.stg_y = (g.to_block_pos(self.stg_y) - 2) * g.BLOCK_SIZE
                g.mushroom.stg_x = g.to_block_pos(self.stg_x) * g.BLOCK_SIZE
            else:
                self.score += 100#pick up gold
        elif val == g.MAP_ENUM_BRICK:
            if self.mv_y < 0.0:
                self.mv_y = 0.0
                self.stg_y = g.to_block_pos(self.stg_y) * g.BLOCK_SIZE
            if self.extraLife:
                g.MAP[g.to_block_pos(self.stg_y) - 1][g.to_block_pos(self.stg_x)] = 0
        elif val != 0:
            if self.mv_y < 0.0:
                self.mv_y = 0.0
                self.stg_y = g.to_block_pos(self.stg_y) * g.BLOCK_SIZE
        if g.mushroom.valid:
            dx = g.mushroom.stg_x - self.stg_x
            dy = g.mushroom.stg_y - self.stg_y
            if math.sqrt(dx ** 2 + dy ** 2) < g.BLOCK_SIZE:#collide with mushroom
                self.score += 1500
                self.extraLife = True
                #remove mushroom   
                g.mushroom.valid = False  
        self.stg_y += self.mv_y
        bid_y = g.to_block_pos(self.stg_y)
        bid_x = g.to_block_pos(self.stg_x)
        val = g.MAP[bid_y][bid_x]
        if val != 0:
            self.stg_x = (bid_x + 1 if self.mv_x > 0.0 else -1)* g.BLOCK_SIZE
            self.stg_y = (bid_y + 1 if self.mv_y > 0.0 else -1)* g.BLOCK_SIZE
            #self.stg_x = g.to_block_pos(self.stg_x) * g.BLOCK_SIZE
        #check state
        if self.stg_y > g.SCN_HEIGHT - 2 * g.BLOCK_SIZE:
            self.dead = True
            self.dead_reason = "Falling Down"
            return
        for i in range(len(g.enemies)):
            if not g.enemies[i].dead:
                dx = g.enemies[i].stg_x - self.stg_x
                dy = g.enemies[i].stg_y - self.stg_y
                if math.sqrt(dx ** 2 + dy ** 2) < g.BLOCK_SIZE:#collide with enemy
                    if dy > 0.5 * g.BLOCK_SIZE:
                        g.enemies[i].dead = True
                        self.score += 100#kill enemy
                        self.mv_y = -self.spd_y
                        self.jump = True
                    else:
                        if self.extraLife:
                            self.extraLife = False
                            self.unrivalled = 120
                        else:
                            if self.unrivalled == 0:
                                self.dead_reason = "Get Killed"
                                self.dead = True
                            return
        if self.unrivalled != 0:
            self.unrivalled -= 1
        if g.check_collide(self.stg_x, self.stg_y, g.DST_STGX, g.DST_STGY):
            self.dead = True
            self.dead_reason = "Reach Destination"
            self.score += 10000
            return
        if self.lifeLeft == 0:
            dx = g.DST_STGX - self.stg_x
            if dx < self.distance_left:
                self.distance_left = dx
                self.lifeLeft = 100 #restart
            else:
                self.dead = True
                self.dead_reason = "Time out"
                return
        self.lifetime += 1
        self.lifeLeft -= 1
        #bid_x = g.to_block_pos(self.stg_x)
        #bid_y = g.to_block_pos(self.stg_y)
        #rect = g.get_block_rect(bid_x, bid_y)
        #if g.check_collide_rect(rect, self.stg_x, self.stg_y):#shift pos
        #    self.stg_x = bid_x * g.BLOCK_SIZE
        #    self.stg_y = bid_y * g.BLOCK_SIZE
        return
    def human_ctrl(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
           self.mv_x = -self.spd
        elif keys[pg.K_d]:
           self.mv_x = self.spd
        else:
            self.mv_x = 0.0
        if keys[pg.K_SPACE]:
            if not self.jump:
                self.jump = True
                self.mv_y = -self.spd_y
        self.update()
        return
    def show(self):
        print(self.move_descision)
        if self.extraLife:
           pg.draw.rect(g.SCN_SURFACE, [150, 0, 0],\
                pg.Rect(g.TRANSX_STG_TO_SCN(self.stg_x) - 0.5 * (g.BLOCK_SIZE + 5),\
                self.stg_y - 0.5 * (g.BLOCK_SIZE + 5), g.BLOCK_SIZE + 5, g.BLOCK_SIZE + 5))
        else:
            if not self.unrivalled & 1:
                pg.draw.rect(g.SCN_SURFACE, [255, 0, 0],\
                    pg.Rect(g.TRANSX_STG_TO_SCN(self.stg_x) - 0.5 * (g.BLOCK_SIZE - 1),\
                    self.stg_y - 0.5 * (g.BLOCK_SIZE - 1), g.BLOCK_SIZE - 1, g.BLOCK_SIZE - 1))

        return
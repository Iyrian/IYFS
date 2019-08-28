import math
SCN_WIDTH = 640
SCN_HEIGHT = 480

SCN_SURFACE = None

SCN_BACKCOLOR = (255, 255, 255)

BLOCK_SIZE = 32
def to_block_pos(val):
    return round(val / BLOCK_SIZE)
#map-------------------------------
MAP_WIDTH : int = 0#in block size
MAP_HEIGHT : int = 0#in block size
MAP = []#contain block infs
MAP_ENUM_WALL_X = 1
MAP_ENUM_WALL_Y = 2
MAP_ENUM_BRICK = 3
MAP_ENUM_SPBRICK = 4
#define NN shape-------------------
NN_INPUT_SIZE : int = 108 #12 * 9
NN_OUTPUT_SIZE : int = 4
NN_HIDDENLAYER_NUM : int = 2
#fixed hidden layer size
NN_HIDDEN_SIZE : int = 18
POP_SIZE = 100#种群数
POP_PM = 0.1#变异率
POP_PC = 0.7#交叉率
#----------------------------------
GRAVITY = 0.1

enemies = []
mushroom = None
MUSHROOM_PSB = 0.8
#stg pos of destination
DST_STGX = 0
DST_STGY = 0
def check_collide_rect(rect : list, x0, y0):
    collide_x = x0 > rect[0] and x0 < rect[0] + rect[2]
    collide_y = y0 > rect[1] and y0 < rect[1] + rect[3]
    return collide_x and collide_y
#return : [0], [1] : left-top
#         [2], [3] : width-height
def get_block_rect(bid_x, bid_y):
    rst = [0.0]*4
    rst[0] = bid_x * BLOCK_SIZE
    rst[1] = bid_y * BLOCK_SIZE
    rst[2] = BLOCK_SIZE
    rst[3] = BLOCK_SIZE
    return rst
def check_collide(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    return math.sqrt(dx ** 2 + dy ** 2) < BLOCK_SIZE
#camera : pos transition------------------------------
CAMERA_STGX = 0
camera_rcd_stg_x = 0
def TRANSX_STG_TO_SCN(stg_x):
    return stg_x - CAMERA_STGX
def TRANSX_SCN_TO_STG(scn_x):
    return scn_x + CAMERA_STGX
#--------------------------------------------------------------
Mario = None#player or model
Pop = None#population
#fonts---------------------------------------------------------
Font_Big = None
Font_Small = None
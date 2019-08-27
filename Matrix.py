import numpy as np
import random
import math
def abs_lmod(mod) :
    return 2.0 * random.random() * mod - mod
#激活函数
def ReLu(z):
    return z if z > 0.0 else 0.0
class Matrix(object):
    def __init__(self, row, column):
        self.Cols = column
        self.Rows = row
        self.Vals = np.zeros((row, column)) #矩阵值
        return
    #由二维数组构建
    @staticmethod
    def from2dArray(raw : np.ndarray):
        self.Rows = len(raw)
        self.Cols = len(raw[0])
        self.Vals = np.zeros((self.Rows, self.Cols))
        for i in range(self.Rows):
            for j in  range(self.Cols):
                self.Vals[i][j] = raw[i][j]
        return self
    #从列表获得一个单列矩阵
    @staticmethod
    def fromArray(raw : list):
        self = Matrix(len(raw), 1)
        for i in range(self.Rows):
            self.Vals[i][0] = raw[i]
        return self
    def dot(self, matrx):
        rst = Matrix(self.Rows, matrx.Cols)
        if self.Cols == matrx.Rows:
            for i in range(self.Rows):
                for j in range(matrx.Cols):
                    sum = 0.0
                    for k in range(self.Cols):
                        sum += self.Vals[i][k] * matrx.Vals[k][j]
                    rst.Vals[i][j] = sum
        return rst
    #随机化矩阵值
    def randomize(self):
        for i in range(self.Rows):
            for j in  range(self.Cols):
                self.Vals[i][j] = abs_lmod(1.0)
        return
    def toArray(self):
        rst = [1.0] * (self.Cols * self.Rows)
        for i in range(self.Rows):
            for j in range(self.Cols):
                rst[i * self.Cols + j] = self.Vals[i][j]
        return rst
    def addBias(self):
        rst = Matrix(self.Rows + 1, 1)
        for i in range(self.Rows):
            rst.Vals[i][0] = self.Vals[i][0]
        rst.Vals[self.Rows][0] = 1.0
        return rst
    def activate(self):
        rst = Matrix(self.Rows, self.Cols)
        for i in range(self.Rows):
             for j in range(self.Cols):
                 rst.Vals[i][j] = ReLu(self.Vals[i][j])
        return rst
    def mutate(self, rate):
        for i in range(self.Rows):
             for j in range(self.Cols):
                 if random.random() < rate:
                     #replace the randomGaussian() for lacking this function
                     self.Vals[i][j] += np.random.randn() / 3.0
                     if self.Vals[i][j] > 1.0:
                         self.Vals[i][j] = 1.0
                     elif self.Vals[i][j] < -1.0:
                         self.Vals[i][j] = -1.0
        return
    #矩阵杂交
    #限定 : shape(matrx.Vals) == shape(self.Vals)
    def crossover(self, matrx):
        rst = Matrix(self.Rows, self.Cols)
        randC = math.floor(random.random() * self.Cols)
        randR = math.floor(random.random() * self.Rows)
        for i in range(self.Rows):
            for j in range(self.Cols):
                if i < randR or (i == randR and j <= randC) :
                    rst.Vals[i][j] = self.Vals[i][j]
                else:
                    rst.Vals[i][j] = matrx.Vals[i][j]
        return rst
    def clone(self):
        rst = Matrix(self.Rows, self.Cols)
        for i in range(self,Rows):
            for j in range(self.Cols):
                rst.Vals[i][j] = self.Vals[i][j] 
        return rst
    def setVals(self, vals : list):
        for i in range(self.Rows):
            for j in range(self.Cols):
                self.Vals[i][j] = vals[i * self.Cols + j]
        return
    def __str__(self):
        str = "|"
        for i in range(self.Rows - 1):
            for j in range(self.Cols):
                str += "{},\t".format(self.Vals[i][j])
            str += "|\n|"
        for j in range(self.Cols):
            str += "{},\t".format(self.Vals[self.Rows - 1][j])
        str += "|\n"
        return str
############################################################
import gdata as g
from Mario import Mario
import random
class Population(object):
    def __init__(self, size, pm, pc):
        self.bestMario = Mario()
        self.marios = [Mario() for i in range(size)]
        self.pm = pm
        self.pc = pc

        self.bestScore = 0 
        self.generation = 0 
        self.bestFitness = 0.0
        self.fitnessSum = 0.0
        return
    def update(self):
        if not self.bestMario.dead:
            self.bestMario.think()
            self.bestMario.update()
        for i in range(len(self.marios)):
            if not self.marios[i].dead:
                self.marios[i].think()
                self.marios[i].update()
        return
    def calculate_fitness(self):
        self.bestMario.calculate_fitness()
        for i in range(len(self.marios)):
            self.marios[i].calculate_fitness()
        return
    def show(self):
        if not self.bestMario.dead:
            self.bestMario.show()
        return
    def done(self):
        if not self.bestMario.dead:
            return False
        for i in range(len(self.marios)):
            if not self.marios[i].dead:
                return False
        return True
    #GA------------------------------------------------------------------
    def set_best(self):
        max_fitness = 0
        max_indx = 0
        for i in range(len(self.marios)):
            if max_fitness < self.marios[i].fitness:
                max_fitness = self.marios[i].fitness
                max_indx = i
        if max_fitness > self.bestMario.fitness:
            if max_fitness > self.bestFitness:
                self.bestFitness = max_fitness
            self.bestScore = self.marios[i].score
            self.bestMario = self.marios[i].clone()
        else:
            if self.bestMario.fitness > self.bestFitness:
                self.bestFitness = self.bestMario.fitness
            self.bestScore = self.bestMario.score
            self.bestMario = self.bestMario.clone()
        return
    def select_parent(self):
        rand = random.uniform(0,self.fitnessSum)
        summation = 0
        for i in range(len(self.marios)):
            summation += self.marios[i].fitness
            if summation > rand:
                return self.marios[i]
        return self.bestMario
    def mutate(self):
        for i in range(len(self.marios)):
            self.marios[i].mutate(self.pm)
        return
    def generate_next(self):
        self.calculate_fitness()
        #get fitness sum:-----------------------------
        sum_rcd = self.fitnessSum
        self.fitnessSum = self.bestMario.fitness
        for i in range(len(self.marios)):
            self.fitnessSum += self.marios[i].fitness
        if self.fitnessSum < sum_rcd:
            print("-------------!!!Degenerate!!!--------------")
        print("Generation<{}> :\n\tBestFitness<{}>\tFitnessSum<{}>".format(self.generation,\
           self.bestFitness, self.fitnessSum))
        #---------------------------------------------
        self.set_best()
        next_generation = []
        for i in range(len(self.marios)):
            if i % 200 == 0:
                print("\tG<{}> new NO.{} Mario".format(self.generation, i))
            child = self.select_parent().crossover(self.select_parent())
            child.mutate(self.pm)
            next_generation.append(child)
        #copy back
        for i in range(len(self.marios)):
            self.marios[i] = next_generation[i]
        self.generation += 1
        return
    #--------------------------------------------------------------------
    def init_pos(self, stg_x, stg_y):
        self.bestMario.stg_x = stg_x
        self.bestMario.stg_y = stg_y
        for i in range(len(self.marios)):
            self.marios[i].stg_x = stg_x
            self.marios[i].stg_y = stg_y
        return
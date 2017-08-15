from random import randint
from GenotypicFunctions import Genotype
# --------------------------------
# 
# --------------------------------

# Generation class
#  Purpose: to hold a collection of Genotypes and allow operations to be down on them
#  Requires: Specific Selector, Mutator, Replicator, and a Population
class Generation:
    def __init__(self, selector, mutator, recombiner, replicator, population):
        self.__selector = selector
        self.__mutator = mutator
        self.__recombiner = recombiner
        self.__replicator = replicator
        self.__population = population
        self.__subpopulation = []
    def select(self):
        self.__subpopulation = self.__selector.select(self.__population)
    def mutate(self):
        self.__subpopulation = self.__mutator.mutate(self.__subpopulation)
    def recombine(self):
        self.__subpopulation = self.__recombiner.recombine(self.__subpopulation)
    def replicate(self):
        self.__population = self.__replicator.replicate(self.__population, self.__subpopulation)

class Selector:
    def __init__(self):
        self.__type = "Tournament"
    def select(self, population, N):
        subpopulation = []
        for i in range(1, N):
            tempSubset = tournamentSelection(population, len(population)/10)
            self.__subpopulation += sorted(tempSubset)[-1]
        return self.__subpopulation
    def tournamentSelection(self, population, size):
        tempSubset = []
        selectedIndices = []
        for i in range(0, size):
            rand = randint(0, len(population)-1)
            while (rand in selectedIndices):
                rand = randint(0, len(population)-1)
            chosenIndices += rand
            tempSubset += population[rand]
        return tempSubset
    
class Mutator:
    def __init__(self, mType):
        self.__type = mType
    def mutate(self, population):
        if self.__type is "Bit Flip":
            return bitFlipMutation(population)
        elif self.__type is "Inversion":
            return inversionMutation(population)
    def bitFlipMutation(self, population):
        rate = 3;
        for index in range(0, len(population)-1):
            roll = randint(0, 100)
            if roll < rate:
                geneIndex = randint(0, population[index].getLength()-1)
                chromosomeIndex = randint(0, population[index][geneIndex].getLength()-1)
                if population[index][geneIndex][chromosomeIndex] is '0':
                    population[index][geneIndex][chromosomeIndex] = '1'
                else:
                    population[index][geneIndex][chromosomeIndex] = '0'
        return population
    def inversionMutation(self, population):
        rate = 3;
        for index in range(0, len(population)-1):
            roll = randint(0, 100)
            if roll < rate:
                geneIndex = randint(0, population[index].getLength())
                chromosomeIndexIni = randint(0, population[index][geneIndex].getLength()-2)
                chromosomeIndexEnd = randint(chromosomeIndexIni, population[index][geneIndex].getLength()-1)
                counter = 0; tempPopulation = population
                for i in range(chromosomeIndexIni, chromosomeIndexEnd):
                    population[index][geneIndex][i] = tempPopulation[index][geneIndex][chromosomeIndexEnd-counter]
                    counter += 1
            return population
    
class Recombiner:
    def __init__(self, rType):
        self.__type = rType
    def recombine(self, population):
        if self.__type is "Single":
            return singlePointRecombination(population)
        elif self.__type is "Uniform":
            return uniformRecombination(population)
    def singlePointRecombination(self, population):
        for i in range(0, len(population)/5):
            index1 = randint(0, len(population)-1)
            index2 = randint(0, len(population)-1)
            while index1 is index2:
                index2 = randint(0, len(population)-1)
            geneIndex = randint(0, population[index1].getLength())
            tempPopulation = population
            population[index1] = tempPopulation[index1][:geneIndex] + tempPopulation[index2][geneIndex:]
            population[index2] = tempPopulation[index2][:geneIndex] + tempPopulation[index1][geneIndex:]
        return population
    def uniformRecombination(self, population):
        rate = 10; tempPopulation = population
        for a in range(0, len(population)/5):
            index1 = randint(0, len(population)-1)
            index2 = randint(0, len(population)-1)
            while index1 is index2:
                index2 = randint(0, len(population)-1)
            tempPopulation = population
            for i in population[index1]:
                for j in population[index1][i]:
                    for k in population[index1][i][j]:
                        roll = randint(0, 100)
                        if roll < rate:
                            population[index1][i][j][k] = tempPopulation[index2][i][j][k]
                            population[index2][i][j][k] = tempPopulation[index1][i][j][k]
        return population
        
class Replicator:
    def __init__(self, rType):
        self.__type = rType
    def replicate(self, population, subpopulation):
        if self.__type is "Generational":
            return generationalReplication(population, subpopulation)
        elif self.__type is "Steady State":
            return steadyStateReplication(population, subpopulation)
    def generationalReplication(self, population, subpopulation):
        length = len(population)
        population = []
        for i in range(0, length):
            index = randint(0, len(subpopulation)-1)
            population += subpopulation[index]
        return population
    def steadyStateReplication(self, population, subpopulation):
        replacedIndices = []
        for i in subpopulation:
            index = randint(0, len(population)-1)
            while index in replacedIndices:
                index = randint(0, len(population)-1)
            population[index] = i
        return population

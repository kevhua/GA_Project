class GenoPhenoConverter:
    def __init__(self):
        self.__genoToPheno = { "00000": "Do Nothing", "00001": "Press Up", "00010": "Press Down", "00011": "Press Left", "00100": "Press Right",
                               "00101": "Release Up", "00110": "Release Down", "00111": "Release Left", "01000": "Release Right", "01001": "Press A",
                               "01010": "Press B", "01011": "Release A", "01100": "Release B", "01101": "Illegal", "01110": "Illegal", "01111": "Illegal",
                               "10000": "Press Up-Left", "10001": "Press Up-Right", "10010": "Release Up-Left", "10011": "Release Up-Right",
                               "10100": "Press Down-Left", "10101": "Press Down-Right", "10110": "Release Down-Left", "10111": "Release Down-Right",
                               "11000": "Press Down-A", "11001": "Press Down-B", "11010": "Release Down-A", "11011": "Release Down-B",
                               "11100": "Press Up-A", "11101": "Press Up-B", "11110": "Release Up-A", "11111": "Release Up-B" }
        self.__phenoToGeno = { "Do Nothing": "00000", "Press Up": "00001", "Press Down": "00011", "Press Left": "00100", "Press Right": "00100",
                               "Release Up": "00101", "Release Down": "00110", "Release Left": "00111", "Release Right": "01000", "Press A": "01001",
                               "Press B": "01010", "Release A": "01100", "Release B": "01100", "Illegal":["01101", "01110", "01111"],
                               "Press Up-Left": "10000", "Press Up-Right": "10001", "Release Up-Left": "10010", "Release Up-Right": "10011",
                               "Press Down-Left": "10100", "Press Down-Right": "10101", "Release Down-Left": "10110", "Release Down-Right": "10111",
                               "Press Down-A", "11000", "Press Down-B": "11001", "Release Down-A": "11010", "Release Down-B": "11011",
                               "Press Up-A": "11100", "Press Up-B": "11101", "Release Up-A": "11110", "Release Up-B": "11111" }
    def genoToPheno(self, genotypeUnit):
        return PhenotypeUnit(self.__genoToPheno[genotypeUnit.getString()])
    def phenoToGeno(self, phenotype):
        return GenotypeUnit(self.__phenoToGeno[phenotype.getString()])

class Generation:
    def __init__(self, selector, mutator, recombiner, replicator):
        self.__selector = selector
        self.__mutator = mutator
        self.__recombiner = recombiner
        self.__replicator = replicator
        self.__population = []
        self.__subpopulation = []
    def select(self):
        self.__subpopulation = self.__selector.select(self.__population)
    def mutate(self):
        self.__subpopulation = self.__mutator.mutate(self.__subpopulation)
    def recombine(self):
        self.__subpopulation = self.__recombiner.recombine(self.__subpopulation)
    def replicate(self):
        return self.__replicator.replicate(self.__subpopulation)

class Selector:
    def __init__(self):
        self.__type = "Tournament Style"
    def select(self, population, N):
        subpopulation = []
        for (i in range(1, N)):
            tournSubset = self.tournamentSelection(population, len(population)/10)
            subpopulation += sorted(tournSubset)[-1] #define leq, geq, eq
        return subpopulation
    def tournamentSelection(self, population, size):
        pop = []
        chosenIndices = []
        for (i in range(0, size)):
            rand = randint(0, len(population)-1)
            while (rand in chosenIndices):
                rand = randint(0, len(population)-1)
            chosenIndices += rand
            pop += population[rand]
        return pop
            
class Mutator:
    def __init__(self, mType):
        self.__type = mType
    def mutate(self, population):
        if (self.__type is "Bit Flip"):
            return bitFlipMutation(population)
        elif (self.__type is "Inversion"):
            return inversionMutation(population)
    def bitFlipMutation(self, population):
        roll = randint(0, 100)
        if (roll < 5):
            index = randint(0, len(population)-1)
            chromosomeIndex = randint(0, population[index].getLength())
            if (population[index][chromosome] is "0"):
                population[index].setIndex(chromosome, "1")
            else:
                population[index].setIndex(chromosome, "0")
        return population
    def inversionMutation(self, population):
        roll = randint(0, 100)
        if (roll < 5):
            index = randint(0, len(population)-1)
            chromosomeIndex = randint(0, population[index].getLength() - 5)
            counter = 0
            tempPopulation = population
            for i in range(chromosomeIndex+5, chromosomeIndex):
                population[index].setIndex(i) = tempPopulation[index][i+5 - counter]
                counter += 1
        return population
    
class Recombiner:
    def __init__(self, rType):
        self.__type = rType
        # single point vs uniform
    def recombine(self, population):
        if (self.__type is "Single Point"):
            return singlePointRecombination(population)
        elif (self.__type is "Uniform"):
            return uniformRecombination(population)
    def singlePointRecombination(self, population):
        index1 = randint(0, len(population)-1)
        index2 = randint(0, len(population)-1)
        chromosomeFlipIndex = randint(0, population[index].getLength())
        while (index2 == index1):
            index2 = randint(0, len(population)-1)
        tempPopulation = population
        population[index1].setString(population[index1].getString()[:chromosomeFlipIndex] + tempPopulation[index2].getString()[chromosomeFlipIndex:])
        population[index2].setString(population[index2].getString()[:chromosomeFlipIndex] + tempPopulation[index1].getString()[chromosomeFlipIndex:])
        return population
    def uniformRecombination(self, population):
        return population
    
class Replicator:
    def __init__(self, rType):
        self.__type = rType
    def replicate(self, population):
        if (self.__type is "Generational"):
            return generationalReplication(population)
        elif (self.__type is "Stead State"):
            return steadyStateReplication(population)
    def generationalReplication(self, population):
        return population
    def steadyStateReplication(self, population):
        return population

class PhenotypeUnit:
    def __init__(self, phenoString):
        self.__phenoUnit = phenoString
    def getString(self):
        return self.__phenoUnit

class GenotypeUnit:
    def __init__(self, genoString):
        self.__genoUnit = genoString
    def getString(self):
        return self.__genoUnit

class Phenotype:
    def __init__(self, genotype):
        
class Genotype:
    def __init__(self, binStringParent, binStringAddition):
        self.__binString = binStringParent + binStringAddition
        self.__binLength = len(self.__binString)
        self.__binUnitLength = 4
        self.__currIndex = 0
        self.__dictionary = GenoPhenoConverter()
        self.__fitness = 0
    def __getitem__(self, key):
        return self.__binString[key:key+self.__binUnitLength]
    def __setitem__(self, key, string):
        currIndex = 0
        for (i in range(key, key+len(string))):
            self.__binString[i] = string[currIndex]
            currIndex += 1
    def __lt__(self, rhs):
        return self.__fitness < rhs.getFitness()
    def __gt__(self, rhs):
        return self.__fitness > rhs.getFitness()
    def __eq__(self, rhs):
        return self.__fitness == rhs.getFitness()
    def __ne__(self, rhs):
        return self.__fitness != rhs.getFitness()
    def __le__(self, other):
        return self.__fitness <= rhs.getFitness()
    def __ge__(self, other):
        return self.__fitness >= rhs.getFitness()
    def getNextGene(self):
        returnStr = binString[self.__currIndex, self.__currIndex + self.__binUnitLength]
        self.__currIndex += 1
        return returnStr
    def getFitness(self):
        return self.__fitness
    def getIndex(self, index):
        
    def setIndex(self, index, value):
        
    def getString(self):
        return self.__binString
    def setString(self, string):
        self.__binString = string
        
    

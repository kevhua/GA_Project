class Genotype:
    def __init__(self, collection):
        self.__genoUnitCollection = collection
        self.__fitness = 0
    def __getitem__(self, key):
        return self.__genoUnitCollection[key]
    def __setitem__(self, key, item):
        self.__genoUnitCollection[key] = item
    def __lt__(self, other):
        return self.__fitness < other.getFitness()
    def __le__(self, other):
        return self.__fitness <= other.getFitness()
    def __gt__(self, other):
        return self.__fitness > other.getFitness()
    def __ge__(self, other):
        return self.__fitness >= other.getFitness()
    def __eq__(self, other):
        return self.__fitness == other.getFitness()
    def __ne__(self, other):
        return self.__fitness != other.getFitness()
    def getFitness(self):
        return self.__fitness
    def phenotype(self):
        phenoCollection[]
        for i in self.__genoUnitCollection:
            phenoCollection += i.phenotype()

class GenotypeUnit:
    def __init__(self, value):
        self.__value = value
    def __getitem__(self, key):
        return self.__value[key]
    def __setitem__(self, key, item):
        self.__value[key] = item
    def phenotype(self):
        return ""                                                           # to do



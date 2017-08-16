import pyautogui
from pyautogui import *
from PIL import Image, ImageFilter, ImageGrab, ImageEnhance
from pytesser import image_to_string
import string
# --------------------------------

class Converter:
    phenoDict = { "00000": lambda: keyDown('left'),
                  "00001": lambda: keyDown('right'),
                  "00010": lambda: keyDown('up'),
                  "00011": lambda: keyDown('down'),
                  "00100": lambda: keyUp('left'),
                  "00101": lambda: keyUp('right'),
                  "00110": lambda: keyUp('up'),
                  "00111": lambda: keyUp('down'),
                  "01000": lambda: keyDown('a'),
                  "01001": lambda: keyDown('b'),
                  "01010": lambda: keyUp('a'),
                  "01011": lambda: keyUp('b'),
                  "01100": lambda: not keyDown('left') and not keyDown('up'),
                  "01101": lambda: not keyDown('right') and not keyDown('up'),
                  "01110": lambda: not keyUp('left') and not keyUp('up'),
                  "01111": lambda: not keyUp('right') and not keyUp('up'),
                  "10000": lambda: not keyDown('left') and not keyDown('down'),
                  "10001": lambda: not keyDown('right') and not keyDown('down'),
                  "10010": lambda: not keyUp('left') and not keyUp('down'),
                  "10011": lambda: not keyUp('right') and not keyUp('down'),
                  "10100": lambda: not keyDown('a') and not keyDown('up'),
                  "10101": lambda: not keyDown('b') and not keyDown('up'),
                  "10110": lambda: not keyUp('a') and not keyUp('up'),
                  "10111": lambda: not keyUp('b') and not keyUp('up'),
                  "11000": lambda: not keyDown('a') and not keyDown('down'),
                  "11001": lambda: not keyDown('b') and not keyDown('down'),
                  "11010": lambda: not keyUp('a') and not keyUp('down'),
                  "11011": lambda: not keyUp('b') and not keyUp('down'),
                  "11100": lambda: not keyDown('a') and not keyDown('b'),
                  "11101": lambda: not keyUp('a') and not keyUp('b'),
                  "11110": lambda: keyDown('right'),
                  "11111": lambda: keyDown('a') }

class GenotypeUnit:
    def __init__(self, value):
        self.__value = value
    def __getitem__(self, key):
        return self.__value[key]
    def __setitem__(self, key, item):
        self.__value[key] = item
    def getLength(self):
        return len(self.__value)
    def phenotype(self):
        Converter.phenoDict[self.__value]()

class Genotype:
    def __init__(self, collection):
        self.__genoUnitCollection = []
        for i in collection:
            self.__genoUnitCollection.append(GenotypeUnit(i))
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
    def getLength(self):
        return len(self.__genoUnitCollection)
    def getFitness(self):
        return self.__fitness
    def getCollection(self):
        return self.__genoUnitCollection
    def phenotype(self):
        pyautogui.PAUSE = 1
        for i in self.__genoUnitCollection:
            i.phenotype()
        # Grab screenshot and crop score area
        screenshot = ImageGrab.grab()
        scoreRectangle = (560, 650, 660, 680)
        cropped_rectangle = screenshot.crop(scoreRectangle)
        # Filter and enhance area to better recognize digits
        cropped_rectangle = cropped_rectangle.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(cropped_rectangle)
        cropped_rectangle = enhancer.enhance(2)
        cropped_rectangle = cropped_rectangle.convert('1')
        text = image_to_string(cropped_rectangle)
        # Remove non-digits from score
        all = string.maketrans('','')
        nodigits = all.translate(all, string.digits)
        # Convert to Int and save as Fitness
        self.__fitness = int(text.translate(all, nodigits))

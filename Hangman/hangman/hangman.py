# ---------- < MODULES > ----------
from random import shuffle
from .fileHandler import FileHandler


# ---------- < HANGMAN CLASS > ----------

class Hangman:
    def __init__(self, debug:bool=False, repeat:bool=False, lives:int=5, wordData:str="Words.txt"):
        self.debug = debug
        self.repeat = repeat
        self.lives = lives
        self.wordData = wordData
        self.fileHandler = FileHandler(debug, wordFile=wordData)

    def selectRandomWord(self):
        result = self.fileHandler.getDataFromFile()

        if result:
            shuffle(result)
            word = result[0]
            if word.find("(") != -1:
                word = word[:word.find("(") - 1]
            return word.upper()
        else:
            return False


hangMan = Hangman(wordData="WordList.csv")
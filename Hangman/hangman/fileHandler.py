# ---------- < MODULES > ----------
from pathlib import Path
from .console import Console


# ---------- < OBJECTS > ----------

console = Console()


# ---------- < FILEHANDLER CLASS > ----------

class FileHandler:
    def __init__(self, *args, wordFile:Path):
        try:
            self.debug = args[0]
        except:
            self.debug = False

        self.wordFile = wordFile

    def getDataFromFile(self):
        try:
            file = open(self.wordFile, "r")
        except:
            if self.debug:
                console.writeline(f"{self.wordFile} doesn't exist or failed to open, skipping!", symbols=True, ifEnd=True)
            return False

        fileLines = file.readlines()
        words = []

        for line in fileLines:
            line = line.strip("\n")
            line = line.strip("ï»¿")
            words.append(line)
        file.close()

        return words
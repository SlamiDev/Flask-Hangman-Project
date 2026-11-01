# ---------- < CONSOLE CLASS > ----------

class Console:
    def __init__(self, displacement : int=30, symbol : str="-"):
        self.displacement = displacement
        self.symbol = symbol

    # WHITESPACE GENERATOR

    def whitepsace(self, amount):
        for count in range(amount):
            print()
        
    # WRITE LINE METHOD WITH SYMBOLS
    def writeLine(self, text, *args, symbols=False, ifEnd=False):
        try:
            whitespaceCount = args[0]
        except:
            whitespaceCount = 0

        self.whitepsace(whitespaceCount)

        if not symbols:
            print(text)
            return
        
        print(self.symbol * self.displacement)
        print(text)
        
        if ifEnd:
            print(self.symbol * self.displacement)
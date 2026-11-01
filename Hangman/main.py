# ---------- < MODULES > ----------
from flask import *
from hangman.hangman import Hangman
from hangman.fileHandler import FileHandler
from random import shuffle



# ---------- < VARIABLES > ----------

wordFile = "WordList.csv"
lifeCount = 8


# ---------- < OBJECTS > ----------

hangman = Hangman(wordData=wordFile)
fileHandler = FileHandler(wordFile=wordFile)



# ---------- < FUNCTIONS > ----------

def getAllowedChars(words):
    chars = []
    wordList = []

    for word in words:
        if word.find("(") != -1:
            word = word[:word.find("(") - 1]
        wordList.append(word)
        for char in word:
            char = char.upper()
            if not char in chars:
                chars.append(char)

    chars.sort()
    return chars, wordList

allowedChars, choiceWordList = getAllowedChars(fileHandler.getDataFromFile())

def findAllLocations(char, word):
    locations = []
    location = 0

    while True:
        if word.find(char, location) != -1:
            location = word.find(char, location)

            locations.append(location)

            location += 1
        else:
            break

    return locations


# ---------- < FLASK > ----------

app = Flask(__name__)
app.secret_key = "3c5f645f2dd5f7ee4d67d5bdef34d961ebd56f3226e169d47ea6126a8d2e0647"

@app.route('/')
def homeRedirect():
    return redirect(url_for("home"))

@app.route('/Home')
def home():
    return render_template("home.html")

@app.route('/WordList')
def wordList():
    return render_template("wordList.html", wordList=choiceWordList)

@app.route('/Game', methods=["POST", "GET"])
def game():
    if request.method == "GET":
        session["Word"] = hangman.selectRandomWord()
        session["Guessed"] = []
        session["CorrectLetterCount"] = 0
        session["TotalUniqueLetterCount"] = len(getAllowedChars([session["Word"]])[0])
        session["LifeCount"] = lifeCount
        return render_template("game.html", word=len(session["Word"]), allowedChars=allowedChars, lifeCount=session["LifeCount"])

    if request.method == "POST":
        letter = request.get_json()["letter"]

        guessed = session["Guessed"]

        if not letter in guessed:
            guessed.append(letter)
            session["Guessed"] = guessed
        else:
            return jsonify(message=f"You already guessed '{letter}'!")

        if letter in session["Word"]:
            session["CorrectLetterCount"] += 1
            if session["TotalUniqueLetterCount"] <= session["CorrectLetterCount"]:
                return jsonify(message=f"You've won!", positions=findAllLocations(letter, session["Word"]), char=letter, won=True)
            else:
                return jsonify(message=f"You guessed correctly!", positions=findAllLocations(letter, session["Word"]), char=letter)
        else:
            session["LifeCount"] -= 1
            if session["LifeCount"] <= 0:
                return jsonify(message=f"You lost. The word was: '{session["Word"]}'", lifeCount=session["LifeCount"], gameOver=True)
            
            return jsonify(message=f"You guessed incorrectly!", lifeCount=session["LifeCount"])

app.run()
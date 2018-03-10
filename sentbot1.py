# SentBot is a genetic algorithm that learns how sentences are constructed by obtaining sample sentences, and running
# genetic simulations to produce the most accurate results possible.

import random
import time
import os
from colorama import init, AnsiToWin32, Fore, Back, Style

init(autoreset=False)

personalities = []

class Personality:
    def __init__(self, dictionary, server, stackSize, deathCount, iterations, averaging, minimumScore):
        self.dictionary = dictionary #This is not the dictionary variable. It is a path relating to the file it is stored in.
        self.server = server #The name of the server that the certain personality is in.
        self.stackSize = stackSize #The size of the populations used in the genetic algorithm. Less population = faster response.
        self.deathCount = deathCount #The amount of sentences that will die in each iteration.
        self.iterations = iterations #The amount of iterations.
        self.averaging = averaging #Whether to use an average or absolute value for scoring.
        self.minimumScore = minimumScore #If the score of the sentence goes over a certain threshold, it will automatically be chosen. (-1 = do not use)

        self.debugging = False #While debugging, messages are printed to the server, and settings can be changed.

        # Data items.
        self.sentenceLengths = [5]
        self.averageSentenceLength = 5

class Word:
    def __init__(self, text=""):
        self.prev = []
        self.text = text
        self.next = []

    def add(self, prev, next):
        if prev != "":
            for s in prev:
                if s not in self.prev:
                    self.prev.append(s)
        if next != "":
            for s in next:
                if s not in self.next:
                    self.next.append(s)

def splitArray(arr, val):
    newArr = []
    buffer = []
    for item in arr:
        if item == val:
            newArr.append(buffer)
            buffer = []
        else:
            buffer.append(item)

    newArr.append(buffer)

    return newArr

def getInput(p, inp):
    # Split the input into words, including punctuation and capitalisation. That's important.
    words = []
    buffer = ""
    for char in inp:
        if char == " ":
            words.append(buffer)
            buffer = ""
        else:
            buffer += char

    if buffer != "":
        words.append(buffer)
        buffer = ""

    #Change the average accordingly.
    p.sentenceLengths.append(len(words))
    tot = 0
    for item in p.sentenceLengths:
        tot += item
    p.averageSentenceLength = tot / len(p.sentenceLengths)

    # Add it all to the word entry in the dictionary. Or make a new one.
    for item in words:
        found = False
        for word in p.dictionary:
            if word.text == item:
                word.add(splitArray(words, item)[0], splitArray(words, item)[1])
                found = True

        if not found:
            p.dictionary.append(Word(item))
            p.dictionary[-1].add(splitArray(words, item)[0], splitArray(words, item)[1])

def checkForSortedArray(arr):
    sorted = True
    prev = -1
    for item in arr:
        if item < prev:
            sorted = False
        prev = item

    return sorted

def testIfOkay(sent):
    try:
        # print(Fore.BLACK, sent, Style.RESET_ALL)
        return True
    except:
        return False

def scoreSentence(p, sent, vari=True):
    stat = 0
    i = 0
    penalty = 1
    lastWord = None
    for word in sent:
        if lastWord == word:
            penalty /= 1.5
        lastWord = word

        for w in word.prev:
            for j in splitArray(sent, word)[0]:
                if w == j.text:
                    stat += 1

        for w in word.next:
            for j in splitArray(sent, word)[1]:
                if w == j.text:
                    stat += 1

        if word.prev == [] and i == 0:
            penalty *= 1.7
        if word.next == [] and i == len(sent) - 1:
            penalty *= 1.7

        i += 1

    dif = len(sent) - p.averageSentenceLength if len(sent) > p.averageSentenceLength else p.averageSentenceLength - len(sent)
    stat /= 1 + (dif * 9)

    stat *= penalty

    return stat / len(sent) if vari else stat

def createPhrase(p):
    # Populate a list full of 50 random sentences.
    sentencePop = []
    ids = []
    sentenceStats = []
    for i in range(0, p.stackSize):
        # Create a completely random sentence of length (1-20) characters.
        sentence = []
        for i in range(random.randint(1,11)):
            sentence.append(random.choice(p.dictionary))

        sentencePop.append(sentence)
        ids.append([random.randint(0, 4), random.randint(0, 4), random.randint(0, 4), random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)])

    # Now that we've got a list of 50 random sentences, we're going to judge the 25 best ones and delete the 25 worst ones.
    # After that, we'll add random mutations of the 25 surviving sentences to fill up the 50. Repeat this a few times and you
    # (hopefullly) have a coherent sentence.

    stats = []

    for sent in sentencePop:
        stats.append(scoreSentence(p, sent, p.averaging))

    while not checkForSortedArray(stats):
        prev = 999
        i = 0
        for item in stats:
            if item < prev and i != 0:
                buf = stats[i - 1]
                stats[i - 1] = stats[i]
                stats[i] = buf

                buf = sentencePop[i - 1]
                sentencePop[i - 1] = sentencePop[i]
                sentencePop[i] = buf

                buf = ids[i - 1]
                ids[i - 1] = ids[i]
                ids[i] = buf

            prev = item
            i += 1

    #Delete the x worst sentences, and replace them with new ones, which are different mutations of the surviving (y-x).
    z = 0
    while (stats[-1] < p.minimumScore or p.minimumScore == -1) and z < p.iterations:
        z += 1
        #Remove the x last sentences in the array
        sentencePop = sentencePop[p.deathCount:]
        ids = ids[p.deathCount:]

        for i in range(0,p.deathCount):
            sentence = []
            for word in sentencePop[i]:
                if random.randint(0,3) != 1:
                    sentence.append(random.choice(p.dictionary) if random.randint(0,3) == 1 else word)
                if random.randint(0,5) != 1:
                    sentence.append(random.choice(p.dictionary))

            if len(sentence) == 0:
                sentence.append(random.choice(p.dictionary))

            sentencePop.append(sentence)
            ids.append([random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4)])

        stats = []

        for sent in sentencePop:
            stats.append(scoreSentence(p, sent, p.averaging))

        while not checkForSortedArray(stats):
            prev = 999
            i = 0
            for item in stats:
                if item < prev and i != 0:
                    buf = stats[i - 1]
                    stats[i - 1] = stats[i]
                    stats[i] = buf

                    buf = sentencePop[i - 1]
                    sentencePop[i - 1] = sentencePop[i]
                    sentencePop[i] = buf

                prev = item
                i += 1

        # print(Fore.WHITE, Style.BRIGHT, "- ITERATION " + str(z) + " -")
        k = 0
        cols = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA]
        for sent in sentencePop:
            uid = Style.BRIGHT + "["
            l = 0
            for item in ids[k]:
                uid += Style.BRIGHT + cols[item] + "#" + Style.RESET_ALL + ("-" if l != len(ids[k]) - 1 else Style.BRIGHT + "]")
                l += 1

            # print(uid, end="  ")
            # print((Fore.RED if k != p.stackSize - p.deathCount - 1 else Fore.YELLOW) if k < p.stackSize - p.deathCount else Fore.GREEN if k != p.stackSize - 1 else Fore.CYAN, end="  ")
            #for word in sent:
                # print(word.text, end=" ")

            # print("-", stats[k])
            k += 1
        # print(Style.RESET_ALL)

    string = ""
    choice = 1
    if random.randint(0,3) == 0:
        choice += 1
        if random.randint(0,3) == 0:
            choice += 1

    for word in sentencePop[choice * -1]:
        # print(word.text, end=" ")
        string += word.text + " "

    # print("-", stats[choice * -1])

    return string

def determinePersonality(message):
    #If it exists, return it.
    for p in personalities:
        if message.server == p.server:
            return p

    #If it's a DM, fuck it.
    if message.server == None:
        return None
    #If it doesn't exist, make it.
    else:
        personalities.append(
            Personality(
                [],
                message.server,
                30,
                15,
                10,
                True,
                -1
            )
        )

        #Then return it.
        return personalities[-1]
    

testP = Personality(
                [],
                "sorry nothing",
                30,
                15,
                10,
                True,
                -1
            )

while True:
    getInput(testP, input("\n\n>> "))

    print(createPhrase(testP))


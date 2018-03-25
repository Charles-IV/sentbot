# SentBot is a genetic algorithm that learns how sentences are constructed by obtaining sample sentences, and running
# genetic simulations to produce the most accurate results possible.

# i don't actually want to be associated with this project, really. it's kinda bad :^) -satanicbanana

import random
import time
import os
from colorama import init, AnsiToWin32, Fore, Back, Style
import discord
import asyncio

init(autoreset=False)

personalities = []

class Personality:
    def __init__(self, dictionary, channel, server, serverMode, stackSize, deathCount, iterations, averaging, minimumScore, staff):
        self.dictionary = dictionary #This is not the dictionary variable. It is a path relating to the file it is stored in.
        self.channel = channel  # the channel ID the bot's in - this will determine personalities
        self.server = server #The name of the server that the certain personality is in.
        self.serverMode = serverMode  # whether servers are used for personalities or not
        self.stackSize = stackSize #The size of the populations used in the genetic algorithm. Less population = faster response.
        self.deathCount = deathCount #The amount of sentences that will die in each iteration.
        self.iterations = iterations #The amount of iterations.
        self.averaging = averaging #Whether to use an average or absolute value for scoring.
        self.minimumScore = minimumScore #If the score of the sentence goes over a certain threshold, it will automatically be chosen. (-1 = do not use)
        self.staff = staff  # the staff that can run admin commands on that server only

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
        if p.serverMode:  # if in server mode
            if message.server == p.server:
                return p
        elif not p.serverMode:  # if in channel mode
            if message.channel.id == p.channel:
                return p

    #If it's a DM, tell me to return an error later
    if message.server == None:
        return "dm"
    #If it doesn't exist, make it.
    else:
        personalities.append(
            Personality(
                [],
                message.channel.id,
                message.server,
                False,
                30,
                15,
                10,
                True,
                -1,
                []
            )
        )

        #Then return it.
        return personalities[-1]
    
# load discord bot details
def loadDetails():
    try:
        f = open("discord-details.txt", "r")
    except IOError:  # if file doesn't exist
        print("ERROR:\ndiscord-details.txt not found.\nPlease generate form discord-details-template.txt")
        exit()
    
    botName = f.readline().strip('\n')
    token = f.readline().strip('\n')  # auto-reads the next line

    admins = f.readline().split(',')
    admins[-1] = admins[-1].strip('\n')  # strip the newline off the end of the last admin
    
    return botName, token, admins

    

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    messageContent = message.content #editable message content block
    commandMode = -1 # determines the command being used. If it is not a command, the mode is -1.
    prefixes = ["!", "d.", ".", "$"]
    for i in range(0, len(prefixes)): #iterate through each item in the prefix group until you hit the one it is (or not) 
        if messageContent.startswith(prefixes[i]):
            commandMode = i # set the command mode
            messageContent = messageContent.lstrip(prefixes[i]) # remove the command prefix from the command
            break # we don't need to iterate any more
                   
    botName, token, admins = loadDetails()  # update details on every message
    try:
        per = determinePersonality(message)
        if str(message.author) == botName:
            return  # do nothing - so i dont have to put it all in if str(message.author) != botName:
        elif per == "dm":  # if it's a DM
            await client.send_message(message.author, "FATAL_ERROR:\nDM's ARE UNSUPPORTED")
            # they don't have to be :^) just use the user ID - will work on this
        else:
            if commandMode == 3:  # admin commands
                if str(message.author) in admins:
                    if messageContent == "SHUTDOWN":
                        await client.send_message(message.channel, ":wave:")
                        os._exit(1)
                    
                    elif messageContent.startswith("STAFF_ADD"):
                        newStaff = str(messageContent.split(" ", 1)[1])
                        per.staff.append(newStaff)
                        await client.send_message(message.channel, newStaff + " added to staff list")
                        
                    elif messageContent.startswith("STAFF_REMOVE"):
                        delStaff = str(messageContent.split(" ", 1)[1])
                        per.staff.remove(delStaff)
                        await client.send_message(message.channel, delStaff + " removed from staff list")
                        
                    else:
                        await client.send_message(message.channel, "FATAL_ERROR:\nCOMMAND NOT FOUND")
                        
                else:
                    await client.send_message(message.channel, "FATAL_ERROR:\nUSER-TYPE \"" + str(message.author.mention) + "\" IS NOT AUTHORISED TO ACCESS ADMINISTRATION COMMANDS")
                   
                   
            elif commandMode == 2:  # staff commands
                if str(message.author) in admins or str(message.author) in per.staff:                       
                    if messageContent == "CLEAR_DICTIONARY":
                        per.dictionary = []
                        await client.send_message(message.channel, "DICTIONARY CLEARED")

                    elif messageContent == "CHANNEL_MODE":
                        per.serverMode = False
                        await client.send_message(message.channel, "CHANNEL MODE ACTIVE")     
                        
                    elif messageContent == "SERVER_MODE":
                        per.serverMode = True
                        await client.send_message(message.channel, "SERVER MODE ACTIVE")
                        
                    else:
                        await client.send_message(message.channel, "FATAL_ERROR:\nCOMMAND NOT FOUND")
                        
                else:
                    await client.send_message(message.channel, "FATAL_ERROR:\nUSER-TYPE \"" + str(message.author.mention) + "\" IS NOT AUTHORISED TO ACCESS STAFF COMMANDS")
                    
                   
            elif commandMode == 1:  # debug commands
                if str(message.author) in admins or str(message.author) in per.staff:
                    if messageContent.startswith("stackSize="):
                        per.stackSize = int(messageContent.split(" ")[1])
                        await client.send_message(message.channel, "STACK_SIZE CHANGED TO " + str(per.stackSize))
                    if messageContent.startswith("deathCount="):
                        per.deathCount = int(messageContent.split(" ")[1])
                        await client.send_message(message.channel, "DEATH_COUNT CHANGED TO " + str(per.deathCount))
                    if messageContent.startswith("iterations="):
                        per.iterations = int(messageContent.split(" ")[1])
                        await client.send_message(message.channel, "ITERATIONS CHANGED TO " + str(per.iterations))
                    if messageContent.startswith("averaging="):
                        per.averaging = messageContent.split(" ")[1] == "true"
                        await client.send_message(message.channel, "FLAG _AVERAGING CHANGED TO " + str(per.averaging))
                    if messageContent.startswith("minimumScore="):
                        per.minimumScore = int(messageContent.split(" ")[1])
                        await client.send_message(message.channel, "minimum_SCORE CHANGED TO " + str(per.minimumScore))
                
                else:
                    await client.send_message(message.channel, "FATAL_ERROR:\nUSER-TYPE \"" + str(message.author.mention) + "\" IS NOT AUTHORISED TO EXECUTE DEBUG COMMANDS")
                    
                   
            elif commandMode == 0:  # normal commands
                if messageContent == "LIST_WORDS":
                    stro = "ALL_WORDS\n\n"
                    for word in per.dictionary:
                        stro += "(" + str(len(word.prev)) + ") " + word.text + " (" + str(len(word.next)) + ")\n"
                    await client.send_message(message.channel, stro)

                elif messageContent == "DUMP_STATS":
                    stri = "FULL STAT LIST\n\n"
                    await client.send_message(message.channel, stri + str(per.stackSize) + "\n" + str(per.deathCount) + "\n" + str(per.iterations) + "\n" + str(per.averaging) + "\n" + str(per.minimumScore) + "\n\n" + str(per.averageSentenceLength))
                    
                elif messageContent == "LIST_STAFF":
                    stru = "STAFF LIST:\n\n"
                    for staff in per.staff:
                        stru += staff + "\n"
                    await client.send_message(message.channel, stru)

                elif messageContent == "HELP" or messageContent == "help":
                    await client.send_message(message.channel, "HELPFUL HELP STUFF:\n\n" +
                    "I highly recommend checking out the project on discord for actual useful stuff: `https://github.com/Charles-IV/sentbot`\n" +
                    "Alternatively, get the list of commands and details about them with `!LIST_COMMANDS`")

                elif messageContent == "LIST_COMMANDS":
                    await client.send_message(message.channel, "COMMAND LIST: (probs out of date)\n\n" +
                    "**TYPES OF COMMAND**\n\n" +
                    "There are 4 types of command: admin, staff, debug and normal\n" +
                    "People with admin commands to the bot (not the server) can run all commands, " +
                    "staff can run staff, debug and normal commands, and"+
                    "normal users can only run normal commands.\nAdmins can add extra staff.\n\n" +
                    "**PREFIXES:**\n\n" +
                    "Admin - `$`\nStaff - `.`\nDebug - `d.`\nNormal - `!`")  # new message so it's not too long
                    await client.send_message(message.channel, "**\nACTUAL COMMANDS**:\n\n" +
                    "**Admin commands**\n" +
                    "`$SHUTDOWN`\nBrings the bot offline. The bot owner will have to bring it back online\n\n" +
                    "`$STAFF_ADD <StaffName#0000>`\nChange the bits in <> as appropiate. Adds a staff member to the list of staff for that personality.\n\n" +
                    "`$STAFF_REMOVE <StaffName#0000>`\nChange the bits in <> as appropiate. Removes a staff member to the list of staff for that personality.\n\n" +
                    "**Staff commands**\n" +
                    "`.CLEAR_DICTIONARY`\nDelete all words in the dictionary for that personality.\n\n" +
                    "`.CHANNEL_MODE`\nSwitches the personalities in that server to channel mode - each channel has a different set of words and staff. This is default.\n\n" +
                    "`.SERVER_MODE`\nSwitches to one personality shared across the whole server - words and staff are the same for all channels.\n\n" +
                    "**Debug commands**\nidk what all these do. When I do, I'll (hopefully) update this.\n" +
                    "`d.stackSize= <>`\n`d.deathCount= <>`\n`d.iterations= <>`\n`d.averaging= <>`\n`d.minimumScore`\n\n" +
                    "**Normal commands**\n" +
                    "`!LIST_WORDS`\nOutputs a list of the words in that personality, also gives details on the number of words before and after it in the sentence it was provided with.\n\n" +
                    "`!DUMP_STATS`\nOutputs (some of) the stats. I'll probs change this one.\n\n" +
                    "`!SAVE`\nSaves all current personalities and their words to a file somewhere. (UNDER DEVELOPMENT)\n\n" +
                    "`!RESTORE`\nRestores the personalities from the file. This should probably be an admin command. (UNER DEVELOPMENT)\n\n" +
                    "`!LIST_STAFF`\nOutputs a list of staff for that personality\n\n" +
                    "`!HELP`\nTries to help you by not telling you much.\n\n" +
                    "`!LIST_COMMANDS`\nOutputs a list of commands. You know, the thing I've just done. You better have got that. Come on.")

                else:
                    await client.send_message(message.channel, "FATAL_ERROR:\nCOMMAND NOT FOUND")
            
                   
            else:  # standard text
                await client.send_typing(message.channel)
                per = determinePersonality(message)
                if per != None:
                    if testIfOkay(message.content):
                        getInput(per, message.content)
                        await client.send_message(message.channel, createPhrase(per))
                    else:
                        await client.send_message(message.channel, "FATAL_ERROR:\nBOT-TYPE 'SENTBOT' DOES NOT WORK WITH NON-ASCII CHARACTERS")
                else:
                    await client.send_message(message.channel, "FATAL_ERROR:\nBOT-TYPE 'SENTBOT' DOES NOT WORK IN DIRECT MESSAGING ENVIRONMENTS")
                        

    except:
        print("FATAL_ERROR:\nUNKNOWN")

        
botName, token, admins = loadDetails()  # this is needed - for the token

client.run(token)

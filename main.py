import os
import datetime
import time
from random import SystemRandom, randint

totalResults = {}
bestSim = 0
worstSim = 0
bestSimMatch = 0
worstSimMatch = 10000000000
simCount = 0
runningTotal = 0
timer = 0

# Prepping constitution for analysis and comparison to monkey's answers
def readConstitution():
    # Ensuring the user actually has a file named constitution
    try:
        # Global variable so we can set and forget, and not pass this around
        global constitution
        with open('constitution.txt', 'r') as file:
            constitution = file.read()
            parseConstitution()
    # Simple Error Handeling to provide descriptive error messages
    except FileNotFoundError:
        print("ERROR: Constitution not found! Please ensure the file 'constitution.txt' exists before trying again!")
        exit()
    except:
        print("ERROR: Something went wrong.\nA highly specialized team of monkeys is working to fix this issue....")
        exit()
        
# Manipulating the constitution that was read in
# In interest of more interesting statistics, I have limited the possible characters to numbers, the space character and the upper and lower case alphabet
def parseConstitution():
    global oneLineConstitution 
    global lenConstitution
    global constitutionArray
    # Monkey does not have access to the new line character.... poor monkey
    oneLineConstitution = constitution.replace('\n', ' ')
    # Removing Double Spaces created by previous call
    oneLineConstitution = oneLineConstitution.replace('  ', ' ')
    lenConstitution = len(oneLineConstitution)
    constitutionArray = list(oneLineConstitution)
    
# This is the keyboard the monkey will use: 0-9, ,A-Z,a-z
# I have removed all other characters from the constitution in hopes for more interesting results
def createKeyBoard():
    global keyboard
    keyboard = []
    for x in range(48, 58):
        keyboard.append(chr(x))
    for x in range(65, 91):
        keyboard.append(chr(x))
    for x in range(97, 123):
        keyboard.append(chr(x))
    keyboard.append(chr(32))
        
    
def createDir():
    try:
        directory = monkeyName +'__' + datetime.datetime.now().strftime("%m_%d_%Y__%H_%M_%S")
        os.mkdir(directory)
        global path
        path = os.getcwd()+ '\\' + directory
    except:
        print("Could not create directory....")
        exit()
    
# Monkey worked very hard! Let's grade his performance.
def gradeMonkey(simulation, correctChars):
    # Preparing results output
    global simCount
    global bestSim 
    global worstSim 
    global bestSimMatch
    global worstSimMatch
    global runningTotal 
    # Average
    simCount += 1
    runningTotal += correctChars
    # Best Simulation
    if correctChars > bestSimMatch:
        bestSimMatch = correctChars
        bestSim = simulation
    # Worst Simulation
    elif correctChars < worstSimMatch:
        worstSimMatch = correctChars
        worstSim = simulation
    # Every Simulation with their respective stats
    totalResults[simulation] = {}
    totalResults[simulation]['correctChars'] = correctChars
    totalResults[simulation]['percent'] = format((correctChars/lenConstitution)*100, '.4f') + '%'
    # On the 0 > % chance he gets it correct, stop the run
    if(correctChars == lenConstitution):
        print('MONKEY CREATED THE CONSTITUTION BEFORE DESTROYING HUMANITY')
        compileResults()
        exit()
    


# Small chance that the monkey may nuke the world
# Ends program immediately
def nuke():
    print("Monkey has pressed the nuke world button.")
    with open(path+'\\NUKE.txt', 'a+') as oops:
        oops.write("I don't want to set the world on fire\nI just want to start a flame in your heart\nIn my heart I have but one desire\nAnd that one is you\nNo other will do\nI've lost all ambition for worldly acclaim\nI just want to be the one you love\nAnd with your admission that you feel the same\nI'll have reached the goal I'm dreaming of\nBelieve me\nI don't want to set the world on fire\nI just want to start a flame in your heart\nI don't want to set the world on fire honey\nI love you too much\nI just want to start a great big flame\nDown in your heart\nYou see, way down inside of me\nDarlin' I have only one desire\nAnd that one desire is you\nAnd I know, nobody else ain't gonna do\nI've lost all ambition for worldly acclaim\nI just want to be the one you love\nAnd with your admission that you feel the same\nI'll have reached the goal I'm dreaming of\nBelieve me\nI don't want to set the world on fire\nI just want to start a flame in your heart")
    compileResults()
    exit()

def compileResults():
    with open(path+'\\RESULTS.txt', 'a+') as results:
        try:
            results.write('Simulation took ' + format(time.time() - timer, '.2f') + ' seconds to run\n')
            results.write('Out of ' + str(simCount) + ' complete runs:\n')
            results.write('Best Performance: Simulation '+ str(bestSim) + ' had ' + str(totalResults[bestSim]['correctChars']) + ' correct characters and matched ' + str(totalResults[bestSim]['percent'])+ ' of all characters\n')
            results.write('Worst Performance: Simulation '+ str(worstSim) + ' had ' + str(totalResults[worstSim]['correctChars']) + ' correct characters and matched ' + str(totalResults[worstSim]['percent'])+ ' of all characters\n')
            aveChars = runningTotal/simCount
            results.write('Average Correct characters: ' + format(aveChars, '.4f')+ ' matched ' + format((aveChars/lenConstitution)*100, '.4f') + '%\ of all characters')
        except KeyError: 
            results.write(monkeyName + ' nuked simulation before enough data was captured....')

# Printing out the monkey output to text files
# Each file will be the length of the constitution so he can be graded fairly 
# But.... Someone put the keys to the United States nuclear arsenal next to him... what will he do?!
def runSimulation(chances):
    fileCount = 1
    # Lets name the files of the text
    # Infinite Loop unless the monkey duplicates the constitution, or presses the nuke button
    rng1 = SystemRandom()
    rng2 = SystemRandom()
    while 0 < 1:
        fileName = path + '\\' + monkeyName + '_sim_' +str(fileCount)+'.txt'
        with open(fileName, 'a+') as sim:
            charCount = 0
            matchChar = 0
            while charCount < lenConstitution:
                monkeyType = keyboard[rng1.randint(0, len(keyboard)-1)]
                sim.write(monkeyType)
                # We have a running counter of the monkey's correct characters he typed
                if monkeyType == constitutionArray[charCount]:
                    matchChar += 1
                nukeChance = rng2.randint(0, chances)
                # Did he nuke?
                if nukeChance == 1:
                    nuke()
                charCount += 1
            # Time to give him a grade
            gradeMonkey(fileCount, matchChar)
        fileCount += 1
        # Monkies can't type all day
        #sleep(1)


def main():
    global monkeyName
    global timer
    readConstitution()
    createKeyBoard()
    print('====================================\n             Welcome!\n====================================')
    monkeyName = input("Please give the monkey a name: ")
    nukeChances = input("How long do you want this simulation to run?\n  Type A for FAST\n  Type B for LONG\n  Type C for VERY LONG\n")
    
    
    createDir()
    timer = time.time()
    
    if nukeChances == 'A' or nukeChances == 'a':
        print('\n    Running FAST')
        print('\n    Please wait.......\n')
        runSimulation(100000) 
    elif nukeChances == 'B' or nukeChances == 'b':
        print('\n    Running LONG')
        print('\n    Please wait.......\n')
        runSimulation(10000000) 
    elif nukeChances == 'C' or nukeChances == 'c':
        print('\n    Running VERY LONG')
        print('\n    Please wait.......\n')
        runSimulation(1000000000) 
    else:
        print('Invalid input, running FAST')
        print('\n    Please wait.......\n')
        runSimulation(100000) 
    


if __name__ == "__main__":
    main()
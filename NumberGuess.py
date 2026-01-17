isPlaying = False
import time

def RandomizeNumber(difficulty):
    import random
    diff = "Easy"
    if difficulty == 1:
        attempts = 10
        range = 25
        number = random.randint(1, 25)
    elif difficulty == 2:
        diff = "Medium"
        attempts = 8
        range = 50
        number = random.randint(1, 50)
    elif difficulty == 3:
        diff = "Hard"
        attempts = 8
        range = 100
        number = random.randint(1, 100)

    print(f"You Picked {diff} Difficulty!")
    time.sleep(2)

    return number, range, attempts   

def EndGame():
    time.sleep(3)
    global isPlaying
    isPlaying = False
    SelectDifficulty()

def GuessNumber(number, range, attempts):
    global isPlaying
    guess = None

    while isPlaying:
        inRange = True
        try:
            print(f"\n\nPick a number between 1 {range}")
            guess = int(input("Enter your guess: "))
            if guess > range or guess < 1:
                print('Outside of range!')
                inRange = False
                time.sleep(1)
            elif guess > number:
                print("\n\nNumber is less than that!")
                time.sleep(1)
            elif guess < number:
                print("\n\nNumber is more than that!")
                time.sleep(1)
            elif guess == number:
                print(f"\n\nYou Got It With {attempts - 1} Attempts Left!")
                time.sleep(2)
                EndGame()

        except ValueError:
            print("\n\nInvalid input")
    
        if isPlaying:
            if inRange:
                attempts -= 1
            else:
                inRange = True    
            if attempts > 1:
                print(f"\n\n{attempts} Attempts Left!")
                time.sleep(1)
            elif attempts == 1:
                print("\n\nThis Is Your Final Attempt!")
                time.sleep(1)
            elif attempts == 0:
                print("\n\nYou Lost ):")
                time.sleep(2)
                EndGame()

            if isPlaying:
                GuessNumber(number, range, attempts)

def SelectDifficulty():
    time.sleep(2)

    global isPlaying
    rules = False
    try:
        difficulty = (input("\n\nSelect difficulty level: Easy, Medium, Hard: "))
        if difficulty[0] in ["E", "M", "H", "e", "m", "h"]:
            isPlaying = True
            number = 1
            if difficulty[0] == "E" or difficulty[0] == "e":
                number = 1
            elif difficulty[0] == "M" or difficulty[0] == "m":
                number = 2
            elif difficulty[0] == "H" or difficulty[0] == "h":
                number = 3

            values = RandomizeNumber(number)

            GuessNumber(values[0], values[1], values[2])
        elif difficulty[0] == "R" or difficulty[0] == "r":
            rules = True
            Rules()
        else:
            print("\n\nPlease select a valid difficulty level between 1 and 3.")
            time.sleep(1)
    except ValueError:
        if not rules:
            print("\n\nInvalid input. Please enter a number between 1 and 3.")
            time.sleep(1)

def WelcomeMsg():
    print("-- Welcome, this is a number guessing game! --\n")
    Rules()

def Rules():
    time.sleep(1)
    print("-- Rules -- \n" \
          "A random number will be picked depending on the difficulty\n" \
          "Easy: 1-25\nMedium: 1-50\nHard: 1-100\n" \
          "It is your job to guess this number\n" \
          "after each guess you will be told wether the number guessed is higher or lower than the target number,\n" \
          "and thats it! Good Luck!\n" \
          "Re-read the rules by typing 'R' into the difficulty selection\n")

WelcomeMsg()

while not isPlaying:
    SelectDifficulty()
import sys
import random
from ratings import ratings

class cards:
    CARDS_IN_DECK = 52
    CARDS_DRAWN = 7
    NUM_COMBINATIONS = 21

    def __init__(self, card="", value=0, suit=""):
        self.card = card
        self.value = value
        self.suit = suit
        self.myHand = None

    # same comparison logic
    def CompareTo(self, other):
        if self.value != other.value:
            return (self.value > other.value) - (self.value < other.value)
        return (self.getSuitLevel(self.suit) > self.getSuitLevel(other.suit)) - (self.getSuitLevel(self.suit) < self.getSuitLevel(other.suit))

    def __lt__(self, other):
        return self.CompareTo(other) < 0

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit

    def getMyHand(self):
        return self.myHand

    def getSuitLevel(self, suit):
        if suit == "D":
            return 1
        elif suit == "C":
            return 2
        elif suit == "H":
            return 3
        elif suit == "S":
            return 4
        return 0

    def initializeStack(self):
        cardstrings = [
            " 2H", " 3H", " 4H", " 5H", " 6H", " 7H", " 8H", " 9H", "10H", " JH", " QH", " KH", " AH", 
            " 2D", " 3D", " 4D", " 5D", " 6D", " 7D", " 8D", " 9D", "10D", " JD", " QD", " KD", " AD", 
            " 2C", " 3C", " 4C", " 5C", " 6C", " 7C", " 8C", " 9C", "10C", " JC", " QC", " KC", " AC", 
            " 2S", " 3S", " 4S", " 5S", " 6S", " 7S", " 8S", " 9S", "10S", " JS", " QS", " KS", " AS"
        ]

        myStack = [None] * self.CARDS_IN_DECK
        for i in range(len(cardstrings)):
            value = 0
            prefix = cardstrings[i][:2]
            if prefix == " J":
                value = 11
            elif prefix == " Q":
                value = 12
            elif prefix == " K":
                value = 13
            elif prefix == " A":
                value = 14
            elif prefix == "10":
                value = 10
            else:
                value = int(cardstrings[i][1:2])
            
            myStack[i] = cards(cardstrings[i], value, cardstrings[i][2:])

        return myStack

    def shuffleStack(self, myStack):
        myShuffledStack = list(myStack)
        random_gen = random.Random()

        for i in range(len(myShuffledStack) - 1, 0, -1):
            newPos = random_gen.randint(0, i)

            temp = myShuffledStack[i]
            myShuffledStack[i] = myShuffledStack[newPos]
            myShuffledStack[newPos] = temp
            
        return myShuffledStack

    def drawHand(self, myStack):
        myHand = [None] * self.CARDS_DRAWN

        for i in range(self.CARDS_DRAWN):
            myHand[i] = myStack[i]
            
        return myHand

    def printStack(self, myStack):
        print("        ✦✦✦ Shuffled " + str(self.CARDS_IN_DECK) + " card deck: ✦✦✦")
        for i in range(len(myStack)):
            print(myStack[i].card, end=" ")
            if (i + 1) % 9 == 0:
                print("")
        print("\n✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦")

    def printHand(self, myHand):
        print("\n✦✦✦✦✦✦✦✦✦✦✦✦✦✦ Your Hand: ✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦")
        for i in range(self.CARDS_DRAWN):
            print(myHand[i].card, end=" ")
        print("\n✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦")

    def deliverStackandHand(self):

        myStack = self.initializeStack()
        myStack = self.shuffleStack(myStack)
        self.myHand = self.drawHand(myStack)
        self.printStack(myStack)
        self.printHand(self.myHand)

    def evaluateHand(self, myHand):

        myCombinations = self.getCombinations(myHand)
        self.printCombinations(myCombinations)

        handRatings = [None] * self.NUM_COMBINATIONS
        for i in range(self.NUM_COMBINATIONS):
            rowHand = [None] * self.CARDS_DRAWN
            for j in range(self.CARDS_DRAWN):
                rowHand[j] = myCombinations[i][j]
            handRatings[i] = ratings(rowHand)

        handRatings.sort()

        print("\n✦✦✦✦✦✦✦✦✦✦✦✦✦HIGH HAND ORDER✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦")
        for i in range(self.NUM_COMBINATIONS):
            for j in range(5):
                print(handRatings[i].playedHand[j].card, end=" ")
            print(" | " + handRatings[i].extraCards[0].card + " " + handRatings[i].extraCards[1].card, end="")
            Hand = handRatings[i].convertScoreToHand(handRatings[i].score)
            print(" --- " + Hand)

        print("\n✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦")

    def getCombinations(self, myHand):
        myCombinations = [[None for _ in range(self.CARDS_DRAWN)] for _ in range(self.NUM_COMBINATIONS)]
        combination = 0

        for i in range(self.CARDS_DRAWN):
            for j in range(i + 1, self.CARDS_DRAWN):
                index = 0

                for k in range(self.CARDS_DRAWN):
                    if k != i and k != j:
                        myCombinations[combination][index] = myHand[k]
                        index += 1

                myCombinations[combination][5] = myHand[i]
                myCombinations[combination][6] = myHand[j]

                combination += 1

        return myCombinations

    def printCombinations(self, myCombinations):
        print("\n✦✦✦✦✦✦✦✦✦✦ Hand Combinations: ✦✦✦✦✦✦✦✦✦✦✦✦✦")
        for i in range(len(myCombinations)):
            for j in range(len(myCombinations[i])):
                print(myCombinations[i][j].card, end=" ")
                if j == 4:
                    print(" | ", end="")
            print("")

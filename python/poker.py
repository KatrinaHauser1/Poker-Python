import cards
import os
import sys

class poker:

    def main(self):

        myCards = cards.cards("", 0, "")

        args = sys.argv[1:]
        self.printIntro(args)

        if len(args) == 0:
            myCards.deliverStackandHand()
            activeHand = myCards.getMyHand()
        else:
            activeHand = self.testDeck(args)
        myCards.evaluateHand(activeHand)


    def printIntro(self, args):
        print("✦✦✦✦✦ POKER ✦✦✦✦✦ HAND ✦✦✦✦✦ ANALYZER ✦✦✦✦✦")
        if len(args) == 0:
            print("\n✦✦✦✦✦ USING ✦✦✦✦ RANDOMIZED ✦✦✦✦ DECK ✦✦✦✦✦")
        else:
            print("✦✦✦✦✦✦ File - " + str(args) + " ✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦")
            print("\n✦✦✦✦✦ USING ✦✦✦✦✦ TEST ✦✦✦✦✦✦✦ DECK ✦✦✦✦✦")

    def testDeck(self, args):

        testHand = [None] * 7

        testFile = args[0]

        if not os.path.exists(testFile):
            print("Error: File not found")
            sys.exit(1)

        with open(testFile, "r") as file:
            line = file.read()

        testStrings = [item.rstrip() for item in line.split(",") if item.strip()]

        if len(testStrings) != 7:
            print("Error: Incorrect Card Format")
            sys.exit(1)


        for i in range(len(testStrings)):
            if len(testStrings[i]) != 3:
                print("\nError: Incorrect Card Format")
                sys.exit(1)

            value = 0
            valueString = testStrings[i][0:2]

            if (valueString == " J"):
                value = 11
            elif(valueString ==" Q"):
                value = 12
            elif(valueString == " K"):
                value = 13
            elif(valueString ==" A"):
                value = 14
            elif(valueString =="10"):
                value = 10
            else:
                value = int(testStrings[i][0:2].strip())

            testHand[i] = cards.cards(testStrings[i], value, testStrings[i][2:])

        print("\n✦✦✦✦✦✦✦✦✦✦✦✦✦✦ Your Hand: ✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦")

        for j in range(7):
            print(testHand[j].card + " ",end="")

        print("\n✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦")


        tempHand = sorted(testHand, key=lambda c: c.card)

        for h in range(len(tempHand)-1):
            if (tempHand[h].card == tempHand[h+1].card):
                print("\nError: Duplicate found in Hand")
                print("DUPLICATE: " + tempHand[h].card)
                sys.exit(1)

        return testHand;


if __name__ == "__main__":
    game = poker()
    game.main()



class ratings:

    def __init__(self, combination):
        self.playedHand = [None] * 5
        self.extraCards = [None] * 2

        for i in range(7):
            if i < 5:
                self.playedHand[i] = combination[i]
            else:
                self.extraCards[i - 5] = combination[i]

        self.playedHand.sort()

        self.score = self.getScore(self.playedHand)
        self.tiebreak = self.getTiebreak(self.playedHand, self.score)


    # using just __lt__ for less than
    def CompareTo(self, other):
        if self.score != other.score:
            return (other.score > self.score) - (other.score < self.score)
        for i in range(len(self.tiebreak)):
            if self.tiebreak[i] != other.tiebreak[i]:
                return (other.tiebreak[i] > self.tiebreak[i]) - (other.tiebreak[i] < self.tiebreak[i])
        return 0

    def __lt__(self, other):
        return self.CompareTo(other) < 0


    # grade hand
    def getScore(self, playable):
        score = 0

        if self.isAscending(playable) and self.isFlush(playable) and (playable[0].value == 10):
            score = 10
        elif self.isAscending(playable) and self.isFlush(playable):
            score = 9
        elif self.numDuplicates("four of a kind", playable):
            score = 8
        elif self.numDuplicates("full house", playable):
            score = 7
        elif self.isFlush(playable):
            score = 6
        elif self.isAscending(playable):
            score = 5
        elif self.numDuplicates("three of a kind", playable):
            score = 4
        elif self.numDuplicates("two pair", playable):
            score = 3
        elif self.numDuplicates("pair", playable):
            score = 2
        else:
            score = 1
        return score


    # tiebreaker array, same length for every played hand
    def getTiebreak(self, playable, score):
        tiebreak = [0] * 5
        index = 0

        if score == 10:
            tiebreak[0] = self.cardStrength(playable[4])
        elif score == 9 or score == 5: #same conditions
            if playable[4].value == 14 and playable[0].value == 2:
                tiebreak[0] = self.cardStrength(playable[3])
            else:
                tiebreak[0] = self.cardStrength(playable[4])
        elif score == 8:
            fourValue = playable[2].value

            for i in range(4, -1, -1):
                if playable[i].value == fourValue:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1

            for i in range(4, -1, -1):
                if playable[i].value != fourValue:
                    tiebreak[index] = self.cardStrength(playable[i])
                    break
        elif score == 7:
            threeValue = playable[2].value

            for i in range(4, -1, -1):
                if playable[i].value == threeValue:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1

            if tiebreak[0] < tiebreak[1]:
                t = tiebreak[0]
                tiebreak[0] = tiebreak[1]
                tiebreak[1] = t
            if tiebreak[1] < tiebreak[2]:
                t = tiebreak[1]
                tiebreak[1] = tiebreak[2]
                tiebreak[2] = t
            if tiebreak[0] < tiebreak[1]:
                t = tiebreak[0]
                tiebreak[0] = tiebreak[1]
                tiebreak[1] = t

            for i in range(4, -1, -1):
                if playable[i].value != threeValue:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1

            if tiebreak[3] < tiebreak[4]:
                t = tiebreak[3]
                tiebreak[3] = tiebreak[4]
                tiebreak[4] = t
        elif score == 6:
            for i in range(4, -1, -1):
                tiebreak[index] = self.cardStrength(playable[i])
                index += 1
        elif score == 4:
            tripValue = playable[2].value

            for i in range(4, -1, -1):
                if playable[i].value == tripValue:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1

            if tiebreak[0] < tiebreak[1]:
                t = tiebreak[0]
                tiebreak[0] = tiebreak[1]
                tiebreak[1] = t
            if tiebreak[1] < tiebreak[2]:
                t = tiebreak[1]
                tiebreak[1] = tiebreak[2]
                tiebreak[2] = t
            if tiebreak[0] < tiebreak[1]:
                t = tiebreak[0]
                tiebreak[0] = tiebreak[1]
                tiebreak[1] = t

            for i in range(4, -1, -1):
                if playable[i].value != tripValue:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1

            if tiebreak[3] < tiebreak[4]:
                t = tiebreak[3]
                tiebreak[3] = tiebreak[4]
                tiebreak[4] = t
        elif score == 3:
            highPair = playable[3].value
            lowPair = playable[1].value

            for i in range(4, -1, -1):
                if playable[i].value == highPair:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1

            if tiebreak[0] < tiebreak[1]:
                t = tiebreak[0]
                tiebreak[0] = tiebreak[1]
                tiebreak[1] = t

            for i in range(4, -1, -1):
                if playable[i].value == lowPair:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1

            if tiebreak[2] < tiebreak[3]:
                t = tiebreak[2]
                tiebreak[2] = tiebreak[3]
                tiebreak[3] = t

            for i in range(4, -1, -1):
                if playable[i].value != highPair and playable[i].value != lowPair:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1
                    break
        elif score == 2:
            pairValue = 0

            for i in range(4):
                if playable[i].value == playable[i + 1].value:
                    pairValue = playable[i].value
                    break

            for i in range(4, -1, -1):
                if playable[i].value == pairValue:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1

            if tiebreak[0] < tiebreak[1]:
                t = tiebreak[0]
                tiebreak[0] = tiebreak[1]
                tiebreak[1] = t

            for i in range(4, -1, -1):
                if playable[i].value != pairValue:
                    tiebreak[index] = self.cardStrength(playable[i])
                    index += 1
        else:
            for i in range(4, -1, -1):
                tiebreak[index] = self.cardStrength(playable[i])
                index += 1

        return tiebreak

    def cardStrength(self, card):
        return card.value * 10 + self.getSuitLevel(card.suit)

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

    def isAscending(self, playable):
        normalStraight = True

        for i in range(len(playable) - 1):
            if (playable[i].getValue() + 1) != (playable[i + 1].getValue()):
                normalStraight = False

        if normalStraight:
            return True

        if playable[4].getValue() == 14 and playable[0].getValue() == 2 and playable[1].getValue() == 3 and playable[2].getValue() == 4 and playable[3].getValue() == 5:
            return True

        return False

    #helper method for determining hand
    def sumUp(self, playable):
        sum = 0
        for i in range(len(playable)):
            sum += playable[i].getValue()
        return sum

    #same as above
    def isFlush(self, playable):
        for i in range(len(playable) - 1):
            if not (playable[i].getSuit() == playable[i + 1].getSuit()):
                return False
        return True

    #helper method, find certain type of duplicate values foe pairs/fours/full house
    def numDuplicates(self, handtype, playable):
        duplicates = [0] * 15
        for i in range(len(playable)):
            currentValue = playable[i].getValue()
            duplicates[currentValue] += 1

        duplicates.sort()

        highest = duplicates[len(duplicates) - 1]
        secondHighest = duplicates[len(duplicates) - 2]

        if handtype == "pair":
            return highest == 2 and secondHighest == 1
        elif handtype == "two pair":
            return highest == 2 and secondHighest == 2
        elif handtype == "three of a kind":
            return highest == 3 and secondHighest == 1
        elif handtype == "four of a kind":
            return highest >= 4
        elif handtype == "full house":
            return highest == 3 and secondHighest == 2
        else:
            return False

    def convertScoreToHand(self, score):
        if score == 1:
            return "High Card"
        elif score == 2:
            return "Pair"
        elif score == 3:
            return "Two Pair"
        elif score == 4:
            return "Three of a Kind"
        elif score == 5:
            return "Straight"
        elif score == 6:
            return "Flush"
        elif score == 7:
            return "Full House"
        elif score == 8:
            return "Four of a Kind"
        elif score == 9:
            return "Straight Flush"
        elif score == 10:
            return "Royal Straight Flush"
        else:
            return "Something went very wrong aaaaaaaa"

#Aubrey Wood
#CS 495 Senior Capstone
#Interactive Voting Protocol
#Advisor: Dr. Xukai Zou

import random

class Collector:
    #shares sent by each voter
    collectedShares = []
    revCollectedShares = []

    def __init__(self):
        self.collectedShares = []
        self.revCollectedShares = []
        
class VoterRegistration:
    #number of voters for this simulation
    numVoters = 0
    #holds voter instances
    voterList = []
    #holds occupied locations for voters
    locList = []

    def __init__(self, collectorA, collectorB):
        keepGoing = True
        print("Select the number of voters.")
        while keepGoing == True:
            try:
                self.numVoters = int(input())
                keepGoing = False
            except:
                print("Select the number of voters.")              
        for i in range(self.numVoters):
            self.locList.append(0)
        self.collectorA = collectorA
        self.collectorB = collectorB
        self.generateVoters()

    #generates instances of voters
    def generateVoters(self):
        voterNum = 0
        temp = 0
        simFlag = 0
        print("Simulate voters? [Y/N]")
        simChoice = input()
        if simChoice == "Y" or simChoice == "y":
            print(simChoice)
            simFlag = 1
            print(simFlag)
        for i in range(self.numVoters):
            newVoter = Voter(self, voterNum, self.collectorA, self.collectorB, simFlag)
            self.voterList.append(newVoter)
            voterNum = voterNum + 1
            
class Voter:
    #reference to voter registration to access numVoters and voterList
    voterReg = -1
    #unique number for each voter
    voterNum = -1
    #voter's unique location
    uniqueLoc = -1
    #total number of candidates
    numCandidates = 2
    #holds voter's vector choice
    locChoice = -1
    #holds voter's candidate choice
    canChoice = -1
    #voter's unique vector built from total voters and candidates and includes the voter's candidate choice at their unique location
    uniqueVec = []
    #voter's binary string representation of their vote
    uniqueBin = ""
    #voter's decimal representation of uniqueBin
    uniqueDec = -1
    #voter's decimal represenation of reversed uniqueBin
    revUniqueDec = -1
    #list of voter's shares of their unique decimal number
    thisShareList = []
    #list of voter's shares of the reverse of their unique decimal number
    revThisShareList = []
    #list of other voters' shares
    otherShareList = []
    #list of other voters' shares of their reverse decimal number
    revOtherShareList = []
    #voter's commitment
    #doesn't seem to be used in section 3.1 but as it is described I'm keeping it in here
    commitment = 0
    #voter's reverse commitment
    #doesn't seem to be used in section 3.1 but as it is described I'm keeping it in here
    revCommitment = 0
    #voter's ballot taking into account voter's share and all other shares received
    ballot = 0
    #voter's reverse ballot taking into account voter's share and all other shares received
    revBallot = 0
    #set to 1 in voter registration class if voters will be simulated
    simFlag = 0

    #initialization for voter
    def __init__(self, voterReg, voterNum, collectorA, collectorB, simFlag):
        self.voterReg = voterReg
        self.voterNum = voterNum
        self.collectorA = collectorA
        self.collectorB = collectorB
        self.simFlag = simFlag
        self.chooseLoc()
        self.chooseCandidate()
        self.genUniqueVec()
        self.genUniqueBin()
        self.genUniqueDecimal()
        self.generateShares()
        self.otherShareList = []
        self.revOtherShareList = []
        self.commitment = 0
        self.revCommitment = 0
        self.ballot = 0
        self.revBallot = 0
    
    #have voter choose their unique location
    def chooseLoc(self):
        if self.simFlag == 0:
            uniqueFlag = 0
            while uniqueFlag == 0:
                keepGoing = True
                while keepGoing == True:
                    print("Choose a location from 1 to " + str(self.voterReg.numVoters) + ".")
                    self.locChoice = input()
                    self.locChoice = self.checkInt(self.locChoice)
                    #bounds checking
                    if self.locChoice > 0 and self.locChoice <= self.voterReg.numVoters:
                    #takes into account 0 index
                        self.locChoice = self.locChoice - 1
                        keepGoing = False
                uniqueFlag = self.enforceUniqueLoc(self.locChoice)
        #simulating voters only
        else:
            keepGoing = True
            self.locChoice = self.voterNum
            while keepGoing == True:
                if self.voterReg.locList[self.locChoice] == 0:
                    self.voterReg.locList[self.locChoice] = 1
                    keepGoing = False
                else:
                    self.locChoice = self.locChoice + 1
                    
    #ensures input is an integer               
    def checkInt(self, choice):
        keepGoing = True
        while keepGoing == True:
            try:
                choice = int(choice)
                keepGoing = False
            except:
                print("Invalid input. Please try again.")
                choice = input()
        return choice
            
        
        
    def enforceUniqueLoc(self, locChoice):
        if self.voterReg.locList[locChoice] == 0:
            self.voterReg.locList[locChoice] = 1
            return 1
        else:
            print("That location has been chosen by another voter. Please choose a different location.")
            return 0
        
    #have voter choose which candidate to vote for
    def chooseCandidate(self):
        if self.simFlag == 0:
            keepGoing = True
            while keepGoing == True:
                print("Please choose which candidate to vote for:")
                for i in range(1, (self.numCandidates + 1)):
                    print(str(i) + ": Candidate " + str(i) + ".")
                self.canChoice = input()
                self.canChoice = self.checkInt(self.canChoice)
                if self.canChoice > 0 and self.canChoice <= self.numCandidates:
                    keepGoing = False
            #takes into account 0 index
            self.canChoice = self.canChoice - 1
            #self.canChoice = -1
        #simulating voters only
        else:
            self.canChoice = random.randint(0, self.numCandidates - 1)

    #builds voter's unique vector based on their chosen location
    def genUniqueVec(self):
        #2D list filled with 0s
        self.uniqueVec = [[0] * self.numCandidates for i in range(self.voterReg.numVoters)]
        #1 replaces a 0 at voter's unique location for their chosen candidate
        self.uniqueVec[self.locChoice][self.canChoice] = 1

    #builds voter's binary number for their choice of candidate and location
    def genUniqueBin(self):
        #iterates through list
        for l in self.uniqueVec:
            #iterates through each element in sublists
            for i in l:
                self.uniqueBin += str(i)

    #builds voter's decimal represenation of their binary number as well as the decimal represneation of the reverse of that binary number            
    def genUniqueDecimal(self):
        self.uniqueDec = int(self.uniqueBin, 2)
        
        #reverses voter position
        voterElem = self.uniqueBin.find("1")
        tempList = list(self.uniqueBin)
        tempList[voterElem] = "0"
        tempList[(VoterRegistration.numVoters * self.numCandidates) - (1 + voterElem)] = "1"
        tempRevBin = "".join(tempList)
        self.revUniqueDec = int(tempRevBin, 2)

    #break up voter's unique decimal number to be sent to the other voters and collectors
    def generateShares(self):
        random.seed()
        #used as a starting point x for the equation x = x - a - b - ... - z + ( a + b ... + z )
        #the number randomly generated below will be repeatedly subtracted from tempTally and added to tempSum
        #after the loop concludes, tempTally and tempSum are added to get the final number to ensure that the original decimal will be recreated once all the shares are added together
        tempTally = self.uniqueDec
        revTempTally = self.revUniqueDec
        self.thisShareList = []
        self.revThisShareList = []
        tempSum = 0
        revTempSum = 0
        #generates a random number and subtracts it from the unique decimal while adding it to a summation variable to ensure accuracy later. bounds dont necessarily matter but I have chosen +/- the unique decimal number
        for i in range(self.voterReg.numVoters):
            tempNum = random.randint((0 - self.uniqueDec), self.uniqueDec)
            revTempNum = random.randint((0 - self.revUniqueDec), self.revUniqueDec)
            self.thisShareList.append(tempNum)
            self.revThisShareList.append(revTempNum)
            tempTally = tempTally - tempNum
            revTempTally = revTempTally - revTempNum
            tempSum = tempSum + tempNum
            revTempSum = revTempSum + revTempNum
        #negating last generated number
        tempTally = tempTally + tempNum
        revTempTally = revTempTally + revTempNum
        #negating last generated number
        tempSum = tempSum - tempNum
        revTempSum = revTempSum - revTempNum
        #ensuring the original decimal is reached
        tempSum = tempTally + tempSum
        self.commitment = tempSum
        revTempSum = revTempTally + revTempSum
        self.revCommitment = revTempSum
        self.thisShareList[self.voterReg.numVoters - 1] = tempTally
        self.revThisShareList[self.voterReg.numVoters - 1] = revTempTally

    #sends shares of this voter's unique decimal number to other voters
    def distributeShares(self):
        #iterate over instances of voters
        for l in range(len(self.voterReg.voterList)):
            #sending share V_il and V'_il to C1 if i and l are both even or odd or to C2 if i is even/odd and l is odd/even
            if self.voterNum % 2 == 0:
                if l % 2 == 0:
                    self.collectorA.collectedShares.append(self.thisShareList[l])
                    self.collectorA.revCollectedShares.append(self.revThisShareList[l])
                else:
                    self.collectorB.collectedShares.append(self.thisShareList[l])
                    self.collectorB.revCollectedShares.append(self.revThisShareList[l])
            else:
                if l % 2 == 0:
                    self.collectorB.collectedShares.append(self.thisShareList[l])
                    self.collectorB.revCollectedShares.append(self.revThisShareList[l])
                else:
                    self.collectorA.collectedShares.append(self.thisShareList[l])
                    self.collectorA.revCollectedShares.append(self.revThisShareList[l])
            #don't send one of the shares denoted by this voter's position in list to another voter (it would just send the share to itself anyway)
            if self.voterReg.voterList[l] != self:
                #appends this voter's share to the end of the list of shares held by another voter
                self.voterReg.voterList[l].otherShareList.append(self.thisShareList[l])
                self.voterReg.voterList[l].revOtherShareList.append(self.revThisShareList[l])

    #adds up each share received from other voters plus
    def computeBallot(self):
        #holds values for the ballot and reverse ballot
        tempSum = 0
        revTempSum = 0
        for i in self.otherShareList:
            tempSum = tempSum + i
        tempSum = tempSum + self.thisShareList[self.voterNum]
        self.ballot = tempSum
        for i in self.revOtherShareList:
            revTempSum = revTempSum + i
        revTempSum = revTempSum + self.revThisShareList[self.voterNum]
        self.revBallot = revTempSum

    #function to remove shares if for some reason a ballot was not cast
    def removeShares(self, endBallot, revEndBallot):
        curBallot = endBallot
        revCurBallot = revEndBallot
        for i in range(len(self.thisShareList)):
            curBallot = curBallot - self.thisShareList[i] + self.otherShareList[i]
            revCurBallot = revCurBallot - self.revThisShareList[i] + self.revOtherShareList[i]
        return curBallot, revCurBallot

def main():
    collectorA = Collector()
    collectorB = Collector()
    voterReg = VoterRegistration(collectorA, collectorB)
    tempSum = 0
    revTempSum = 0
    #have each voter give each other voter their shares
    for i in voterReg.voterList:
        i.distributeShares()
    #have each voter add up all of the shares from each other voter plus their share to determine their ballot
    for i in voterReg.voterList:
        i.computeBallot()
    print("---------------------------------------")
    print("| Voter | Secret Ballot | Aggregation |")
    #add up all ballots for the final tally
    vNum = 1
    for i in voterReg.voterList:
        tempSum = tempSum + i.ballot
        revTempSum = revTempSum + i.revBallot
        print("| " + str(vNum).center(5, ' ') + " | " + str(i.ballot).center(13, ' ') + " | " + str(tempSum).center(11, ' ') + " |")
        vNum = vNum + 1
    print("---------------------------------------")
    #collectors adding up their total shares
    tS = 0
    rTS = 0
    for i in collectorA.collectedShares:
        tS = tS + i
    for i in collectorB.collectedShares:
        tS = tS + i
    for i in collectorA.revCollectedShares:
        rTS = rTS + i
    for i in collectorB.revCollectedShares:
        rTS = rTS + i

    
#TESTING
    a = 0
    b = 0
    for i in voterReg.voterList:
        a = a + i.uniqueDec
        b = b + i.revUniqueDec
    print("For testing/demo purposes")
    print("Binary tally from all voters : {0:b}".format(int(a)))
    print("Decimal tally from all voters : " + str(a))
    count = 1
    for i in voterReg.voterList:
        print("Voter " + str(count) + "'s unique decimal : " + str(i.uniqueDec))
        count = count + 1
    print("Reverse binary tally from all voters : {0:b}".format(int(b)))
    print("Reverse decimal tally from all voters : " + str(b))
    print("Binary tally from collectors : {0:b}".format(int(tS)))
    print("Decimal tally from collectors : " + str(tS))
    print("Reverse binary tally from collectors : {0:b}".format(int(rTS)))
    print("Reverse decimal tally from collectors : " + str(rTS))
    
#TESTING
        
    
if __name__ == "__main__":
    main()

from CLIPS import *
from riskStructs import *

class RiskPythonToCLIPS:
    def __init__(self):
        self.Clips = CLIPS()
        self.loadClipsFile()

    def loadClipsFile(self):
        self.Clips.load("AutoP1.clp")
        self.Clips.reset()

    def printFacts(self):
        self.Clips.printFacts()

    def reset(self):
        return self.Clips.reset()

    def run(self):
        return self.Clips.run()

    def exit(self):
        self.Clips.exit()

    def translateAdjacentCountriesDToDeffacts(self):
        deffactString = ""
        for country in adjacentCountriesD:
            # next line isn't readable TROLOLOLOLOL
            deffactString += " (%s (country %s) (adjacent-to %s)) " % ("adjacent-countries", country.replace(" ", "-"), " ".join([cntry.replace(" ", "-") for cntry in adjacentCountriesD[country]]))
        self.Clips.deffacts("adjacents", deffactString)

    def translateBookBonusToFact(self, bookArmiesBonusList):
        strBookArmiesList = []
        for num in bookArmiesBonusList:
            strBookArmiesList.append(str(num))
        factString = "(bookArmiesBonusList %s)" % (" ".join(strBookArmiesList))
        self.Clips.assertFact(factString)

    def translatePlayerInfoToFact(self, player, playerDMe):
        cardCountryString = ""
        for card in playerDMe[player]["cards"]:
            cardCountryString += card[0].replace(" ", "-") + " " ##makes country name CLIPS friendly
            cardFactString = "(card (country %s) (type %s))" % (card[0].replace(" ", "-"), card[1])
            self.Clips.assertFact(cardFactString)
        playerFactString = "(player-info (player %s) (armies %s) (card-countries %s))" % (player, playerDMe[player]["armies"], cardCountryString)
        self.Clips.assertFact(playerFactString)

    def initiateBookSelectionAndReturnList(self, bookArmiesBonusList, player, playerDMe):
        self.translateBookBonusToFact(bookArmiesBonusList)
        self.translatePlayerInfoToFact(player, playerDMe)
        self.Clips.assertFact("(phase book-select)")
        return eval(self.Clips.run())

#testPlayerDMe = {1:{"armies":30,"color":'green',"loc":(-350,257),"cards":[["test1", "artillery"], ["test2", "cavalry"], ["test3", "wild"]]}}
testPlayerDMe = {1:{"armies":30,"color":'green',"loc":(-350,257),"cards":[["test1", "r"], ["test2", "r"], ["test3", "r"]]}}
test = RiskPythonToCLIPS()
test.initiateBookSelectionAndReturnList(['10'], 1, testPlayerDMe)

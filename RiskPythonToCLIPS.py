from CLIPS import *
from riskStructs import *

class RiskPythonToCLIPS:
    def __init__(self):
        self.Clips = CLIPS()
        self.loadClipsFile()

    def loadClipsFile(self):
        self.Clips.load("AutoP1.clp")

    def reset():
        self.Clips.reset()

    def run():
        self.Clips.run()

    def translateAdjacentCountriesDToDeffacts(self):
        deffactString = ""
        for country in adjacentCountriesD:
            # next line isn't readable TROLOLOLOLOL
            deffactString += " (%s (country %s) (adjacent-to %s)) " % ("adjacent-countries", country.replace(" ", "-"), " ".join([cntry.replace(" ", "-") for cntry in adjacentCountriesD[country]]))
        self.Clips.deffacts("adjacents", deffactString)

    def translateBookBonusToFact(self, bookArmiesBonusList):
        factString = "(bookArmiesBonusList %s)" % (" ".join(bookArmiesBonusList))
        self.Clips.assertFact(factString)

    def translatePlayerInfoToFact(self, player, playerDMe):
        pass

test = RiskPythonToCLIPS()

"""
Information for battery parameters.
Each anode and cathode have specific string names.
String names are attached to constants.

"""
import pprint

def dictTest():
    thisdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
    }
    return thisdict

class immutableDict:
    def __init__(self):
        self.params = dictTest()
        pass
    def getParams(self):
        return self.params.copy()
    def addParams(self, name, dif, rad, conc):
        if name in self.params:
            return
        self.params[name] = [dif, rad, conc]
        pass

        
if __name__ == "__main__":
    dictTest()
import numpy as np

global position_overview
position_overview = {
    "offense": {
        "line": ["C", "G", "T"],
        "backfield": ["HB", "QB", "FB"],
        # note that Y and U pass catchers are tight ends and others are wideouts.
        "pass_catchers": ["WR", "TE"]
    },
    "defense": {
        "line": ["DT", "DE"],
        "linebackers": ["S", "M", "W"],
        "backs": ["CB", "SF", "N"]
    },
    "special_teams": {
        "kickers": ["PK", "PT"],
        "other": ["LS", "GR"]
    }

}
class RatedPlayer:
    def __init__(self, name = "", unit = position_overview.keys(), subunit = set(), position = "", 
                 ratings = {"consistency": 5, "explosiveness": 5}):
        self.name = name
        self.unit = unit
        self.subunit = subunit
        self.position = position
        self.ratings = ratings
    def get_overall(self):
        return np.mean([self.ratings[attribute] for attribute in self.ratings])
    def __repr__(self):
        return self.name + ", " + self.position + " consistency: " + str(self.ratings["consistency"]) + " explosiveness: " + str(self.ratings["explosiveness"])
if __name__ == '__main__':
    kirk = RatedPlayer("Kirk Cousins", set("offense"), "backfield", "quarterback", {"consistency":7, "explosiveness": 6})
    print(kirk.get_overall())
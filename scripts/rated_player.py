import numpy as np

global position_overview
position_overview = {
    "offense": {
        "offensive_line": ["C", "G", "T"],
        "backfield": ["HB", "QB", "FB"],
        # note that Y and U pass catchers are tight ends and others are wideouts.
        "pass_catchers": ["WR", "TE"]
    },
    "defense": {
        "defensive_line": ["DT", "DE"],
        "linebackers": ["S", "M", "W"],
        "backs": ["CB", "SF", "N"]
    },
    "special_teams": {
        "kickers": ["PK", "PT"],
        "other": ["LS", "GR"]
    }

}
def get_unit_and_subunit(position):
    for unit in position_overview:
        for subunit in position_overview[unit]:
            for pos in position_overview[unit][subunit]:
                if pos == position:
                    return unit, subunit, pos
class RatedPlayer:
    def __init__(self, name = "", unit = position_overview.keys(), subunit = set(), position = "", 
                 ratings = {"consistency": 5, "explosiveness": 5}, years_played = 0):
        self.name = name
        self.unit = unit
        self.subunit = subunit
        self.position = position
        self.ratings = ratings
        self.years_played = years_played

    def get_overall(self):
        return np.mean([self.ratings[attribute] for attribute in self.ratings])
    def get_obfuscated_ratings(self, obfuscation_variance = 1):
        return {"consistency": self.ratings["consistency"] + np.random.normal(0, obfuscation_variance),
                "explosiveness": self.ratings["explosiveness"] + np.random.normal(0, obfuscation_variance)}
    def print_obfuscated_ratings(self, obfuscation_variance = 1):
        obfuscated_ratings = self.get_obfuscated_ratings(obfuscation_variance)
        print(self.name + ", " + self.position + ", overall: " + str(round(np.mean([obfuscated_ratings["consistency"], obfuscated_ratings["explosiveness"]]), 3))+ " consistency: " + str(round(obfuscated_ratings["consistency"], 3)) + " explosiveness: " + str(round(obfuscated_ratings["explosiveness"], 3)))
    def __repr__(self):
        return self.name + ", " + self.position + " consistency: " + str(round(self.ratings["consistency"], 3)) + " explosiveness: " + str(round(self.ratings["explosiveness"], 3))
if __name__ == '__main__':
    kirk = RatedPlayer("Kirk Cousins", set("offense"), "backfield", "quarterback", {"consistency":7, "explosiveness": 6})
    print(kirk.get_overall())
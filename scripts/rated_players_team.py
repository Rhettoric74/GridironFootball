from team import Team
from rated_player import RatedPlayer, position_overview
import numpy as np
import random

# 12 players is the basic number on offense and defense to account for different packages
# e.g. 11 personel & 21 personel, base & nickel
# four players are designated as special teams
RATING_VARIANCE = 1.5
def generate_player_names(num_players = 28):
    male_first_names = []
    last_names = []
    with open("data/male_names.txt") as fp1:
        for first_name in fp1:
            male_first_names.append(first_name.strip("\n"))
    male_first_names = male_first_names[7:]
    with open("data/last_names.txt") as fp2:
        for last_name in fp2:
            last_names.append(last_name.strip(",\n"))
    # TODO: rework this to come up with realistic names
    return [random.choice(male_first_names) +  " " + random.choice(last_names) for i in range(num_players)]

class RatedPlayersTeam(Team):
    def __init__(self, team_name, abbreviation = None, mascot = None, division = None, conference = None, color = "white"):
        super().__init__(team_name, abbreviation, mascot, division, conference, color)
        self.players = []
    def add_player(self, player):
        self.players.append(player)
    def remove_player(self, player):
        self.players.remove(player)
    def get_unit(self, unit_name):
        return [player for player in self.players if player.unit == unit_name]
    def get_subunit(self, subunit_name):
        return [player for player in self.players if player.subunit == subunit_name]
    def get_position_group(self, position_name):
        return [player for player in self.players if player.position == position_name]
    def avg_player_consistency(players_list):
        return np.mean([player.ratings["consistency"] for player in players_list])
    def avg_player_explosiveness(players_list):
        return np.mean([player.ratings["explosiveness"] for player in players_list])
    def get_offensive_overall(self):
        return np.mean([player.get_overall() for player in self.players if "offense" in player.unit])
    def get_defensive_overall(self):
        return np.mean([player.get_overall() for player in self.players if "defense" in player.unit])
    def get_special_teams_overall(self):
        return np.mean([player.get_overall() for player in self.players if "special_teams" in player.unit])
    def get_team_overall(self):
        OFFENSIVE_WEIGHT = 11
        DEFENSIVE_WEIGHT = 11
        SPECIAL_TEAMS_WEIGHT = 4
        return (OFFENSIVE_WEIGHT * self.get_offensive_overall() + DEFENSIVE_WEIGHT * self.get_defensive_overall() + SPECIAL_TEAMS_WEIGHT * self.get_special_teams_overall()) / (
            DEFENSIVE_WEIGHT + OFFENSIVE_WEIGHT + SPECIAL_TEAMS_WEIGHT
        )
    def generate_random_players(self, player_names = None, mean_consistency = 5, mean_explosiveness = 5):
        if self.players != []:
            print("Cannot generate players on already populated team!")
            return
        if player_names == None:
            player_names = generate_player_names()
        idx = 0
        position_counts = {"QB": 1, "HB": 1, "FB": 1, "T": 2, "G": 2, "C": 1, "TE": 1, "WR": 3, "DE": 2, "DT": 2, "S": 1, "M": 1, "W": 1, "CB": 2, "SF": 2, "N": 1, "PK": 1, "PT": 1, "LS": 1, "GR": 1}
        for unit in position_overview:
            for subunit in position_overview[unit]:
                for position in position_overview[unit][subunit]:
                    for i in range(position_counts[position]):
                        new_player = RatedPlayer(player_names[idx], unit, subunit, position, {
                            "consistency": random.normalvariate(mu=mean_consistency, sigma=RATING_VARIANCE),
                            "explosiveness": random.normalvariate(mu=mean_explosiveness, sigma=RATING_VARIANCE),
                        })
                        idx += 1
                        self.players.append(new_player)
                        print(new_player)
    def __repr__(self):
        return (self.team_name + " Overall: " + str(self.get_team_overall()) + " Consistency: " + str(RatedPlayersTeam.avg_player_consistency(self.players)) +
                 " Explosiveness: " + str(RatedPlayersTeam.avg_player_explosiveness(self.players)) + "\n")
if __name__ == '__main__':
    vikings = RatedPlayersTeam("Minnesota", "MN", "Vikings", "N", "NFC", "purple")
    vikings.generate_random_players()
    print(vikings.get_defensive_overall())
    print(vikings.get_offensive_overall())
    print(vikings.get_team_overall())

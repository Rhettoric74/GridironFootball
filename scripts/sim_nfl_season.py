from game_state import GameState
from team import Team
from rated_players_team import RatedPlayersTeam
import csv
from dice_game import DiceGame
from game_simulator import GameSimulator
from rated_players_simulator import RatedPlayersSimulator
import numpy as np
import random

def load_teams_from_csv(filepath = "data/nfl_teams.csv"):
    with open(filepath) as fp:
        team_data = csv.DictReader(fp)
        teams_list = []
        for row in team_data:
            team_name = " ".join(row["Name"].split(" ")[:-1])
            team_mascot = row["Name"].split(" ")[-1]
            teams_list.append(Team(team_name, row["Abbreviation"], team_mascot, row["Division"], row["Conference"]))
        return teams_list
def load_rated_teams_from_csv(filepath = "data/nfl_teams.csv"):
    with open(filepath) as fp:
        team_data = csv.DictReader(fp)
        teams_list = []
        for row in team_data:
            team_name = " ".join(row["Name"].split(" ")[:-1])
            team_mascot = row["Name"].split(" ")[-1]
            cur_team = RatedPlayersTeam(team_name, row["Abbreviation"], team_mascot, row["Division"], row["Conference"])
            cur_team.generate_random_players(None, random.randint(3, 7), random.randint(3, 7))
            teams_list.append(cur_team)

        return teams_list

class League:
    def __init__(self, teams = load_teams_from_csv(), simulator: GameSimulator = DiceGame):
        self.teams = teams
        self.conferences = list(set([team.conference for team in self.teams]))
        self.divisions = list(set([team.conference + " " + team.division for team in self.teams]))
        self.simulator = simulator
    def play_round_robin(self):
        played_already = set()
        for team in self.teams:
            played_already.add(team)
            for other_team in self.teams:
                if other_team not in played_already:
                    team.schedule.append(other_team)
                    other_team.schedule.append(team)
                    self.simulator(team, other_team).simulate_game()
    def list_records(self):
        self.teams.sort(key=lambda team: team.num_wins)
        for team in self.teams:
            print(str(team) + " " + str(team.num_wins) + "-" + str(team.num_losses) + "-"
                   + str(team.num_ties) + ", point per game: " + str(np.mean(team.points_for)) + " points allowed per game: " + str(np.mean(team.points_allowed)))
            print("Yards per game: " + str(np.mean(team.yards_for)) + ". Yards allowed per game: " + str(np.mean(team.yards_allowed)))
            print()



if __name__ == '__main__':
    teams = load_rated_teams_from_csv()
    for team in teams:
        print(team)
    league = League(teams, RatedPlayersSimulator)
    league.play_round_robin()
    league.list_records()
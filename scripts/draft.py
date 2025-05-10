from rated_players_team import RatedPlayersTeam, generate_player_names
from rated_player import RatedPlayer, position_overview, get_unit_and_subunit
from sim_nfl_season import League, load_rated_teams_from_csv
import random
import time

def get_selection_from_terminal(prospects):
    shuffled_first_ten = prospects[-10:]
    random.shuffle(shuffled_first_ten)
    for i in range(min(10, len(prospects))):
        print(i, end=": ")
        shuffled_first_ten[i].print_obfuscated_ratings()
    prospects_viewed = 0
    MAX_VIEWABLE = 3
    for i in range(MAX_VIEWABLE):
        print("Choose up to " + str(MAX_VIEWABLE - i) + " more players to evaluate a second time.")
        index_chosen = None
        while index_chosen not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "STOP"]:
            index_chosen = input("Enter the index of the prospect you would like a second evaluation of, or type STOP to skip.")
            if index_chosen == "STOP":
                print("Moving on to the draft selection step")
                break
            elif index_chosen in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                shuffled_first_ten[int(index_chosen)].print_obfuscated_ratings(0.5)
                prospects_viewed += 1
        if index_chosen == "STOP":
            break
    selection = None
    while selection not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        selection = input("Enter the index of the player you want to pick: ")
    return shuffled_first_ten[int(selection)]


class Draft:
    def __init__(self, teams, draft_selections = None, prospects = [], num_rounds=7):
        self.prospects = prospects
        self.teams = teams
        if draft_selections == None:
            self.draft_selections = [self.teams for i in range(num_rounds)]
        else:
            self.draft_selections = draft_selections
        self.num_rounds = num_rounds
        self.num_picks = len(self.teams) * self.num_rounds
        self.pick_index = 0
    def team_on_the_clock(self):
        if self.pick_index >= self.num_picks:
            print("Draft has ended")
            return
        return self.draft_selections[self.pick_index // len(self.teams)][self.pick_index % len(self.teams)]
    def draft_player(self, team, player):
        if team != self.team_on_the_clock():
            print(team.team_name + " is not currently on the clock!")
            return
        self.prospects.remove(player)
        team.players.append(player)
        self.pick_index += 1
    def generate_prospects(self, num_prospects = 300, rating_mean = 5, rating_std = 1.5):
        num_to_generate = num_prospects - len(self.prospects)
        player_names = generate_player_names(num_to_generate)
        position_counts = {"QB": 1, "HB": 1, "FB": 1, "T": 2, "G": 2, "C": 1, "TE": 1, "WR": 3, "DE": 2, "DT": 2, "S": 1, "M": 1, "W": 1, "CB": 2, "SF": 2, "N": 1, "PK": 1, "PT": 1, "LS": 1, "GR": 1}
        new_prospects = []
        for player_name in player_names:
            position = random.choices(list(position_counts.keys()), weights=list(position_counts.values()))[0]
            print(position)
            unit, subunit, position = get_unit_and_subunit(position)
            rating = {"consistency": random.normalvariate(rating_mean, rating_std), "explosiveness": random.normalvariate(rating_mean, rating_std)}
            new_prospects.append(RatedPlayer(player_name, unit, subunit, position, rating))
        self.prospects = sorted(self.prospects + new_prospects, key=lambda player: player.get_overall())
    def simulate_draft(self, wait_time_between_picks = 1):
        for round_num in range(self.num_rounds):
            print("Round " + str(round_num + 1) + " begins!")
            for selection in self.draft_selections[round_num]:
                pick = selection.draft_strategy(self.prospects)
                print("With the " + str(self.pick_index + 1) + " pick the " + selection.team_name + " " + selection.mascot + " select:")
                print(pick)
                print()
                self.draft_player(selection, pick)
                time.sleep(wait_time_between_picks)
if __name__ == '__main__':
    teams = load_rated_teams_from_csv()
    for team in teams:
        print(team)
    league = League(teams)
    league.teams[0].draft_strategy = get_selection_from_terminal
    draft = Draft(league.teams)
    draft.generate_prospects()
    for prospect in draft.prospects:
        prospect.print_obfuscated_ratings()
    draft.simulate_draft(wait_time_between_picks=0)

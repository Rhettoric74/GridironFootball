from rated_players_team import *
from game_simulator import GameSimulator
import turtle
import game_state
from turtle_graphics import draw_game_state, erase_game_state, draw_field
import time
import numpy as np

TURNOVER_WEIGHT = 0.03
TURNOVER_BASE_PROB = 0.016
SACK_WEIGHT = 0.1
SACK_BASE_PROB = 0.0413
BIG_PLAY_BASE_PROB = 0.04
BIG_PLAY_WEIGHT = 0.04
BASE_OFFENSIVE_VARIATION = 2

class RatedPlayersSimulator(GameSimulator):
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.game_state = game_state.GameState(self.home_team, self.away_team, 15)
    
    def play_from_scrimmage(self):
        turnover = False
        # riskiness rating reflects how much less consistent one team is than its opponent is explosive.
        defensive_explosiveness = RatedPlayersTeam.avg_player_explosiveness(self.game_state.get_team_without_possession().get_unit("defense"))
        offensive_consistency = RatedPlayersTeam.avg_player_consistency(self.game_state.team_with_possession.get_unit("offense"))
        off_riskiness_rating = (defensive_explosiveness - offensive_consistency) / 10
        offensive_explosiveness = RatedPlayersTeam.avg_player_explosiveness(self.game_state.team_with_possession.get_unit("offense"))
        defensive_consistency = RatedPlayersTeam.avg_player_consistency(self.game_state.get_team_without_possession().get_unit("defense"))
        print(defensive_consistency, offensive_consistency)
        def_riskiness_rating = (offensive_explosiveness - defensive_consistency) / 10
        play_score = random.random()
        yards_gained = 0
        if play_score < TURNOVER_BASE_PROB + TURNOVER_WEIGHT * off_riskiness_rating:
            # case of turnover
            turnover = True
            yards_gained = - np.random.poisson(defensive_explosiveness)
        elif play_score < TURNOVER_BASE_PROB + SACK_BASE_PROB + SACK_WEIGHT * off_riskiness_rating:
            # case of sack / tfl
            print("Sack!")
            yards_gained = - np.random.poisson(5 + defensive_explosiveness - offensive_consistency)
        elif play_score > 1 - (BIG_PLAY_BASE_PROB + BIG_PLAY_WEIGHT * def_riskiness_rating):
            print("Big play!")
            yards_gained = 15 + abs(offensive_explosiveness * np.random.poisson(2))
        else:
            print("normal play")
            yards_gained = np.random.poisson(5.3 + offensive_consistency - defensive_consistency)
        #yards_gained = round(yards_gained)                                                     
        self.game_state.update_state(yards_gained, turnover, time_elapsed=0.4)
    def field_goal_try(self):
        active_kicker = self.game_state.team_with_possession.get_position_group("PK")
        return random.normalvariate(18 + RatedPlayersTeam.avg_player_consistency(active_kicker), RatedPlayersTeam.avg_player_explosiveness(active_kicker)) - self.game_state.yards_to_goal() >= 0
    def kick_field_goal(self):
        self.game_state.update_state(0, is_kick_good=self.field_goal_try(), time_elapsed=0.1)
    def punt(self):
        active_punter = self.game_state.team_with_possession.get_position_group("PT")
        self.game_state.update_state(round(35 + random.normalvariate(RatedPlayersTeam.avg_player_consistency(active_punter), RatedPlayersTeam.avg_player_explosiveness(active_punter))), punt=True, time_elapsed=0.2)
    def kickoff(self):
        # TODO: come up with a dice model for how to proper kickoffs.
        # so far this function just assumes you always get an NFL-rules touchback
        self.game_state.update_state(30, time_elapsed=0)
    def play_fourth_down(self):
        if self.game_state.yards_to_goal() <= 35:
            self.kick_field_goal()
        elif random.randint(1, 10) > self.game_state.distance + (self.game_state.yards_to_goal() // 10):
            self.play_from_scrimmage()
        else:
            self.punt()
    def kick_pat(self):
        active_kicker = self.game_state.team_with_possession.get_position_group("PK")
        kick = random.uniform(0, 2 * RatedPlayersTeam.avg_player_consistency(active_kicker)) > 1
        self.game_state.update_state(0, is_kick_good=kick)
    def simulate_game(self, turn_time = 0, turtle = None):
        while not self.game_state.game_is_over:
            if self.game_state.down == "kickoff":
                self.kickoff()
            elif self.game_state.down_counter in [1, 2, 3]:
                # conditions where you should attempt a field goal not on fourth down
                if self.game_state.time_remaining <= 0.4 and self.game_state.current_quarter in [2, 4] and self.game_state.yards_to_goal() <= 35 and self.game_state.away_score - self.game_state.home_score <= -3:
                    self.kick_field_goal()
                else: 
                    self.play_from_scrimmage()
            elif self.game_state.down_counter == 4:
                self.play_fourth_down()
            elif self.game_state.down == "PAT":
                self.kick_pat()
            print(self.game_state)
            print()
            if turtle != None:
                draw_game_state(self.game_state, turtle)
            time.sleep(turn_time)
            if turtle != None:
                erase_game_state(self.game_state, turtle)
if __name__ == '__main__':
    home, away = RatedPlayersTeam("Kansas City", "KC", mascot="Chiefs", color="red"), RatedPlayersTeam("Philiadelphia", "PHI", mascot="Eagles", color="darkgreen")
    home.generate_random_players(mean_consistency=1, mean_explosiveness=9)
    away.generate_random_players(mean_consistency=9, mean_explosiveness=1)
    print(home.get_team_overall())
    print(away.get_team_overall())
    game = RatedPlayersSimulator(home, away)
    #t, screen = draw_field(home, away)
    game.simulate_game()
    print(game.game_state)
    print(away.yards_for, away.yards_allowed, home.yards_for, home.yards_allowed)
from rated_players_team import *
from game_simulator import GameSimulator
import turtle
import game_state
from turtle_graphics import draw_game_state, erase_game_state, draw_field
import time
import numpy as np
from playcall_classifier import decide_next_play, decide_fourth_down

BASE_FUMBLE_RATE = 0.008
MEAN_RUSH_YARDS = 4.2
MEAN_YARDS_PER_COMPLETION = 10
BASE_INTERCEPTION_RATE = 0.016
EXPLOSIVE_RUN_RATE = 0.11
EXPLOSIVE_RUN_WEIGHT = 0.01
BASE_COMPLETION_PERCENTAGE = 0.63
BASE_SACK_RATE = 0.075
SACK_WEIGHT = 0.005
TURNOVER_WEIGHT = 0.001
COMPLETION_PERCENTAGE_WEIGHT = 0.01
YARDAGE_WEIGHT = 0.25

class RatedPlayersSimulatorV2(GameSimulator):
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.game_state = game_state.GameState(self.home_team, self.away_team, 15)
    
    def run_play(self):
        turnover = False
        # riskiness rating reflects how much less consistent one team is than its opponent is explosive.
        d_front_seven = self.game_state.get_team_without_possession().get_defensive_front_seven()
        d_front_seven_consistency = RatedPlayersTeam.avg_player_consistency(d_front_seven)
        d_front_seven_explosiveness = RatedPlayersTeam.avg_player_explosiveness(d_front_seven)

        o_front_seven = self.game_state.team_with_possession.get_offensive_front_seven()
        o_front_seven_consistency = RatedPlayersTeam.avg_player_consistency(o_front_seven)
        o_front_seven_explosiveness = RatedPlayersTeam.avg_player_explosiveness(o_front_seven)
        yards_gained = 0
        seed = random.random()
        if seed > 1 - (BASE_FUMBLE_RATE + ((o_front_seven_consistency - d_front_seven_explosiveness) * TURNOVER_WEIGHT)):
            print("fumble!")
            turnover = True
            yards_gained = 10 - 5 * np.random.poisson(max(2 + d_front_seven_explosiveness - o_front_seven_consistency, 0))
        elif seed < EXPLOSIVE_RUN_RATE + ((o_front_seven_explosiveness - d_front_seven_consistency) * EXPLOSIVE_RUN_WEIGHT):
            print("explosive run play!")
            yards_gained = 10 + 3 * np.random.poisson(max(0, 4 + o_front_seven_explosiveness - d_front_seven_consistency))
        else:
            yards_gained = -2 + np.random.poisson(2 + MEAN_RUSH_YARDS + (o_front_seven_consistency - d_front_seven_consistency) * YARDAGE_WEIGHT)
        self.game_state.update_state(yards_gained, turnover)
        


    def pass_play(self):
        turnover = False
        # riskiness rating reflects how much less consistent one team is than its opponent is explosive.
        d_back_seven = self.game_state.get_team_without_possession().get_defensive_back_seven()
        d_back_seven_consistency = RatedPlayersTeam.avg_player_consistency(d_back_seven)
        d_back_seven_explosiveness = RatedPlayersTeam.avg_player_explosiveness(d_back_seven)

        o_skills = self.game_state.team_with_possession.get_offensive_skill_positions()
        o_skills_consistency = RatedPlayersTeam.avg_player_consistency(o_skills)
        o_skills_explosiveness = RatedPlayersTeam.avg_player_explosiveness(o_skills)
        
        o_line_consistency = RatedPlayersTeam.avg_player_consistency(self.game_state.team_with_possession.get_subunit("offensive_line"))
        d_line_explosiveness = RatedPlayersTeam.avg_player_explosiveness(self.game_state.get_team_without_possession().get_subunit("defensive_line"))
        yards_gained = 0
        time_elapsed = 0.5
        sack_seed = random.random()
        if sack_seed < BASE_SACK_RATE + ((d_line_explosiveness - o_line_consistency) * SACK_WEIGHT):
            print("Sack!")
            yards_gained = - np.random.poisson(max(d_line_explosiveness, 0))
        else:
            seed = random.random()
            if seed < BASE_INTERCEPTION_RATE + ((d_back_seven_explosiveness - o_skills_consistency) * TURNOVER_WEIGHT):
                print("Interception!")
                turnover = True
                yards_gained = 20 - 5 * np.random.poisson(max(5 + d_back_seven_explosiveness - o_skills_consistency, 0))
            elif seed < 1 - (BASE_COMPLETION_PERCENTAGE + ((o_skills_consistency - d_back_seven_consistency) * COMPLETION_PERCENTAGE_WEIGHT)):
                # incomplete pass case
                yards_gained = 0
                time_elapsed = 0.1
            else:
                yards_gained = np.random.poisson(max(MEAN_YARDS_PER_COMPLETION + (o_skills_explosiveness - d_back_seven_consistency) * YARDAGE_WEIGHT, 0))
        self.game_state.update_state(yards_gained, turnover, time_elapsed=time_elapsed)
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
    def kick_pat(self):
        active_kicker = self.game_state.team_with_possession.get_position_group("PK")
        kick = random.uniform(0, 2 * RatedPlayersTeam.avg_player_consistency(active_kicker)) > 1
        self.game_state.update_state(0, is_kick_good=kick)
    def qb_kneel(self):
        self.game_state.update_state(yardage=-1, time_elapsed=2/3)
    def qb_spike(self):
        self.game_state.update_state(yardage=0, time_elapsed=0.05)
    def simulate_game(self, turn_time = 0, turtle = None):
        while not self.game_state.game_is_over:
            if self.game_state.down == "kickoff":
                self.kickoff()
            elif self.game_state.down == "PAT":
                # TODO: add decision process for whether to go for two or kick XP.
                self.kick_pat()
            else:
                play_call = None
                if self.game_state.down_counter == 4:
                    play_call = decide_fourth_down(self.game_state.get_state_vector())
                else:
                    play_call = decide_next_play(self.game_state.get_state_vector())
                print(play_call)
                if play_call == "extra_point":
                    self.kick_pat()
                elif play_call == "field_goal":
                    self.kick_field_goal()
                elif play_call == "kickoff":
                    print("kickoff predicted incorrectly")
                    return
                elif play_call == "no_play":
                    # TODO: figure out a more elegant way to handle this, in real life would be a penalty but that's
                    # hard to model, so just defaulting to a pass play instead.
                    print("no_play predicted")
                    self.pass_play()
                elif play_call == "pass":
                    self.pass_play()
                elif play_call == "punt":
                    self.punt()
                elif play_call == "qb_kneel":
                    self.qb_kneel()
                elif play_call == "qb_spike":
                    self.qb_spike()
                elif play_call == "run":
                    self.run_play()
                else:
                    print("None predicted!")
                    self.run_play()
                
                    
            
            print(self.game_state)
            print()
            if turtle != None:
                draw_game_state(self.game_state, turtle)
            time.sleep(turn_time)
            if turtle != None:
                erase_game_state(self.game_state, turtle)
if __name__ == '__main__':
    home, away = RatedPlayersTeam("Minnesota", "MIN", mascot="Vikings", color="purple"), RatedPlayersTeam("Green Bay", "GB", mascot="Packers", color="darkgreen")
    home.generate_random_players(mean_consistency=7, mean_explosiveness=3)
    away.generate_random_players(mean_consistency=3, mean_explosiveness=7)
    print(home.get_team_overall())
    print(away.get_team_overall())
    game = RatedPlayersSimulatorV2(home, away)
    t, screen = draw_field(home, away)
    game.simulate_game(turn_time=1, turtle=t)
    print(game.game_state)
    print(away.yards_for, away.yards_allowed, home.yards_for, home.yards_allowed)
from team import Team
import random
import pandas as pd

downs_map = {1:"1st", 2:"2nd", 3:"3rd", 4:"4th"}
# constant for how many yards from the line of scrimmage kickers kick from
FIELD_GOAL_HOLDING_DISTANCE = 8
class GameState:
    def __init__(self, home_team = Team("Home team", color="black"), away_team = Team("Away team", color="white"), quarter_length = 15):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.home_yards = 0
        self.away_yards = 0
        self.coin_toss_winner = random.choice([self.home_team, self.away_team])
        self.team_with_possession = self.coin_toss_winner
        self.down = "kickoff"
        self.down_counter = 0
        self.distance = 0
        self.yard_line = 35
        if self.team_with_possession == self.away_team:
            self.yard_line = 65
        self.quarter_length = quarter_length
        self.current_quarter = 1
        self.time_remaining = self.quarter_length
        self.game_is_over = False
    def describe_yard_line(self):
        if self.yard_line < 50:
            return self.home_team.abbreviation + " " + str(self.yard_line)
        elif self.yard_line > 50:
            return self.away_team.abbreviation + " " + str(100 - self.yard_line)
        else:
            return "50"
    def yards_to_goal(self):
        if self.home_team == self.team_with_possession:
            return 100 - self.yard_line
        else:
            return self.yard_line
    def __repr__(self):
        if self.down != "kickoff":
            return (str(self.away_team.team_name) + " " + str(self.away_score) + " " + str(self.home_team.team_name) + " " + str(self.home_score) + "\n"
                        + str(self.team_with_possession.team_name) + " ball at the " + self.describe_yard_line() + " " + self.down + " and " + str(self.distance)
                        + "\n" + str(self.time_remaining) + " in quarter " + str(self.current_quarter))
        else:
            return (str(self.away_team.team_name) + " " + str(self.away_score) + " " + str(self.home_team.team_name) + " " + str(self.home_score) + "\n"
                        + str(self.team_with_possession.team_name) + " kickoff from the " + self.describe_yard_line()
                        + "\n" + str(self.time_remaining) + " in quarter " + str(self.current_quarter))
    def switch_possession(self):
        teams = [self.home_team, self.away_team]
        teams.remove(self.team_with_possession)
        self.team_with_possession = teams[0]
        self.down_counter = 1
        self.down = "1st"
        self.distance = 10
    def get_team_without_possession(self):
        if self.team_with_possession == self.home_team:
            return self.home_team
        return self.away_team
    def set_to_kickoff(self):
        self.yard_line = 35
        if self.team_with_possession == self.away_team:
            self.yard_line = 65
        self.distance = 0
        self.down_counter = 0
        self.down = "kickoff"
    def update_records(self):
        if self.game_is_over:
            if self.away_score > self.home_score:
                self.away_team.num_wins += 1
                self.home_team.num_losses += 1
            elif self.home_score > self.away_score:
                self.home_team.num_wins += 1
                self.away_team.num_losses += 1
            else:
                self.home_team.num_ties += 1
                self.away_team.num_ties += 1
            # record the scores of the game in the team objects
            self.away_team.points_for.append(self.away_score)
            self.away_team.yards_for.append(self.away_yards)
            self.away_team.points_allowed.append(self.home_score)
            self.away_team.yards_allowed.append(self.home_yards)

            self.home_team.points_for.append(self.home_score)
            self.home_team.yards_for.append(self.home_yards)
            self.home_team.points_allowed.append(self.away_score)
            self.home_team.yards_allowed.append(self.away_yards)

    def update_state(self, yardage, turnover = False, two_point_try = False, is_kick_good = None, time_elapsed = 0.5, punt = False):
        if self.game_is_over:
            return
        if self.down == "PAT":
            opponent_points_scored = 0
            if yardage <= -98:
                if turnover:
                    # kick 2 / pick 2
                    opponent_points_scored = 2
                else:
                    # 1 point safety (never happened in NFL but in rules)
                    opponent_points_scored = 1
            if self.team_with_possession == self.away_team:
                self.home_score += opponent_points_scored
            else:
                self.away_score += opponent_points_scored
            if opponent_points_scored == 0:
                points_scored = 0
                if two_point_try and yardage >= self.distance:
                    points_scored = 2
                if not two_point_try and is_kick_good:
                    points_scored = 1
                if self.team_with_possession == self.away_team:
                    self.away_score += points_scored
                else:
                    self.home_score += points_scored
            self.set_to_kickoff()
        elif self.down == "kickoff":
            self.down = "1st"
            self.down_counter = 1
            if self.team_with_possession == self.home_team:
                self.yard_line = 100 - yardage
            else:
                self.yard_line = yardage
            if not turnover:
                self.switch_possession()
        # case for field goals
        elif is_kick_good != None:
            if is_kick_good:
                if self.team_with_possession == self.home_team:
                    self.home_score += 3
                else:
                    self.away_score += 3
                self.set_to_kickoff()
            else:
                # missed field goal
                if self.home_team == self.team_with_possession:
                    self.yard_line -= 8
                else:
                    self.yard_line += 8
                self.switch_possession()
        elif punt == True:
            self.switch_possession()
            if self.team_with_possession == self.home_team:
                self.yard_line -= yardage
            else:
                self.yard_line += yardage
            # handle touchbacks
            if self.yard_line <= 0:
                self.yard_line = 20
            if self.yard_line >= 100:
                self.yard_line = 80



        elif turnover == False:
            if self.team_with_possession == self.home_team:
                self.yard_line += yardage
                # for plays from scrimmage, add yardage, keeping the distance to a
                # touchdown as the maximum
                self.home_yards += min(yardage, self.yards_to_goal())
            else:
                self.yard_line -= yardage
                self.away_yards += min(yardage, self.yards_to_goal())
            if yardage >= self.distance:
                print(self.team_with_possession.abbreviation + " first down!")
                self.down = "1st"
                self.down_counter = 1
                self.distance = 10
            else:
                self.distance -= yardage
                self.down_counter += 1
                if self.down_counter <= 4:
                    self.down = downs_map[self.down_counter]
                else:
                    print("Turnover on downs!")
                    self.switch_possession()
        else:
            print("Forced turnover!")
            if self.team_with_possession == self.home_team:
                self.yard_line += yardage
            else:
                self.yard_line -= yardage
            self.switch_possession()
        
        if self.yard_line <= 0:
            if self.team_with_possession == self.away_team:
                print(self.away_team.abbreviation + " touchdown!")
                self.away_score += 6
                self.team_with_possession = self.away_team
                self.down = "PAT"
                self.down_counter = 0
                self.distance = 2
                self.yard_line = 2
            else:
                print(self.away_team.abbreviation + " scores a safety!")
                self.away_score += 2
                self.down_counter = 0
                self.down = "kickoff"
            if self.current_quarter == 5:
                print("Game over")
                self.game_is_over = True
                self.update_records()
        if self.yard_line >= 100:
            if self.team_with_possession == self.home_team:
                print(self.home_team.abbreviation + " touchdown!")
                self.home_score += 6
                self.team_with_possession = self.home_team
                self.down = "PAT"
                self.down_counter = 0
                self.distance = 2
                self.yard_line = 98
            else:
                print(self.home_team.abbreviation + " scores a safety!")
                self.home_score += 2
                self.down_counter = 0
                self.down = "kickoff"
            if self.current_quarter == 5:
                print("Game over")
                self.game_is_over = True
                self.update_records()
        if time_elapsed >= self.time_remaining:
            if self.current_quarter == 4:
                print("End of regulation")
                if self.away_score == self.home_score:
                    print("Overtime!")
                    self.current_quarter = 5
                    self.time_remaining = self.quarter_length
                else:
                    self.game_is_over = True
                    self.update_records()
            elif self.current_quarter == 2:
                print("Halftime!")
                # setup the second half kickoff
                teams = [self.home_team, self.away_team]
                teams.remove(self.coin_toss_winner)
                self.team_with_possession = teams[0]
                self.set_to_kickoff()
                self.current_quarter += 1
                self.time_remaining = self.quarter_length

            elif self.current_quarter == 5:
                print("End of overtime!")
                self.game_is_over = True
                self.update_records()
            else:
                self.current_quarter += 1
                self.time_remaining = self.quarter_length
        elif self.down != "PAT":
            # decrement time remaining if it's not a point after attempt
            # and the quarter is not over.
            self.time_remaining -= time_elapsed

    def get_state_vector(self, posteam_mapping = {"home": 0, "away": 1}):
        """describe game state as a vector with columns as follows: ['posteam_type', 'yardline_100', 'quarter_seconds_remaining', 'down',
       'half_seconds_remaining', 'game_seconds_remaining', 'goal_to_go',
       'ydstogo', 'score_differential']"""
        posteam = posteam_mapping["away"]
        if self.team_with_possession == self.home_team:
            posteam = posteam_mapping["home"]
        quarter_seconds_remaining = self.time_remaining * 60
        game_seconds_remaining = max(0, (4 - self.current_quarter)) * 15 * 60 + quarter_seconds_remaining
        half_seconds_remaining = game_seconds_remaining % (30 * 60)
        goal_to_go = 0
        if self.yards_to_goal() <= self.distance:
            self.goal_to_go = 1
        score_differential = self.home_score - self.away_score
        if self.team_with_possession == self.away_team:
            score_differential = - score_differential
        sample = pd.DataFrame(columns=['posteam_type', 'yardline_100', 'quarter_seconds_remaining', 'down',
            'half_seconds_remaining', 'game_seconds_remaining', 'goal_to_go',
            'ydstogo', 'score_differential'])
        sample.loc[0] = [posteam, self.yard_line, quarter_seconds_remaining, self.down_counter, half_seconds_remaining, game_seconds_remaining, goal_to_go, self.distance, score_differential]
        return sample
    


if __name__ == "__main__":
    game = GameState(Team("Minnesota"), Team("Green Bay", "GB"))
    print(game)
    game.update_state(30)
    print(game)
    game.update_state(2)
    print(game)
    game.update_state(9)
    print(game)
    game.update_state(-10, True)
    print(game)
    game.update_state(40)
    print(game)
    game.update_state(2, two_point_try=True)
    print(game)
    game.update_state(30)
    print(game)



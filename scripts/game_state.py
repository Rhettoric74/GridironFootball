from team import Team
import random

downs_map = {1:"1st", 2:"2nd", 3:"3rd", 4:"4th"}
class GameState:
    def __init__(self, home_team = Team("Home team"), away_team = Team("Away team")):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.coin_toss_winner = random.choice([self.home_team, self.away_team])
        self.team_with_posession = self.coin_toss_winner
        self.down = "kickoff"
        self.down_counter = 0
        self.distance = 0
        self.yard_line = 35
        if self.team_with_posession == self.away_team:
            self.yard_line = 65
    def describe_yard_line(self):
        if self.yard_line < 50:
            return self.home_team.abbreviation + " " + str(self.yard_line)
        elif self.yard_line > 50:
            return self.away_team.abbreviation + " " + str(100 - self.yard_line)
        else:
            return "50"
    def __repr__(self):
        if self.down != "kickoff":
            return (str(self.away_team) + " " + str(self.away_score) + " " + str(self.home_team) + " " + str(self.home_score) + "\n"
                        + str(self.team_with_posession) + " ball at the " + self.describe_yard_line() + " " + self.down + " and " + str(self.distance))
        else:
            return (str(self.away_team) + " " + str(self.away_score) + " " + str(self.home_team) + " " + str(self.home_score) + "\n"
                        + str(self.team_with_posession) + " kickoff from the " + self.describe_yard_line())
    def switch_possession(self):
        teams = [self.home_team, self.away_team]
        teams.remove(self.team_with_posession)
        self.team_with_posession = teams[0]
        self.down_counter = 1
        self.down = "1st"
        self.distance = 10
    def update_state(self, yardage, turnover = False, two_point_try = False, is_kick_good = False):
        if self.down == "PAT":
            opponent_points_scored = 0
            if yardage <= -98:
                if turnover:
                    # kick 2 / pick 2
                    opponent_points_scored = 2
                else:
                    # 1 point safety (never happened in NFL but in rules)
                    opponent_points_scored = 1
            if self.team_with_posession == self.away_team:
                self.home_score += opponent_points_scored
            else:
                self.away_score += opponent_points_scored
            if opponent_points_scored == 0:
                points_scored = 0
                if two_point_try and yardage >= self.distance:
                    points_scored = 2
                if not two_point_try and is_kick_good:
                    points_scored = 1
                if self.team_with_posession == self.away_team:
                    self.away_score += points_scored
                else:
                    self.home_score += points_scored

        if self.down == "kickoff":
            self.down = "1st"
            self.down_counter = 1
            if self.team_with_posession == self.home_team:
                self.yard_line = 100 - yardage
            else:
                self.yard_line = yardage
            if not turnover:
                self.switch_possession()

        elif turnover == False:
            if self.team_with_posession == self.home_team:
                self.yard_line += yardage
            else:
                self.yard_line -= yardage
            if yardage >= self.distance:
                print(self.team_with_posession.abbreviation + " first down!")
                self.down = "1st"
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
            if self.team_with_posession == self.home_team:
                self.yard_line += yardage
            else:
                self.yard_line -= yardage
            self.switch_possession()
        if self.yard_line <= 0:
            print(self.away_team.abbreviation + " touchdown!")
            self.away_score += 6
            self.team_with_posession = self.away_team
            self.down = "PAT"
            self.down_counter = 0
            self.distance = 2
            self.yard_line = 2
        if self.yard_line >= 100:
            print(self.home_team.abbreviation + " touchdown!")
            self.home_team += 6
            self.team_with_posession = self.home_team
            self.down = "PAT"
            self.down_counter = 0
            self.distance = 2
            self.yard_line = 98





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



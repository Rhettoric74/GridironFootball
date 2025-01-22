from team import Team
import game_state
import random
import numpy as np
import time
def check_for_triples(rolls):
        """returns a number if the given list of rolls contains "triples".
        Returns negative 1 if there are no triples in the list."""  
        counts = {}
        for roll in rolls:
            if roll not in counts:
                counts[roll] = 1
            else:
                counts[roll] += 1
        for number, count in counts.items():
            if count >= 3:
                return number
        return -1
def check_for_doubles(rolls):
    """returns a number if the given list of rolls contains "triples".
    Returns negative 1 if there are no triples in the list."""  
    counts = {}
    for roll in rolls:
        if roll not in counts:
            counts[roll] = 1
        else:
            counts[roll] += 1
    for number, count in counts.items():
        if count == 2:
            return number
    return -1
class DiceGame:
    def __init__(self, home_team, away_team, dice_number = 2, offensive_dice_faces = 10, defensive_dice_faces = 6):
        self.home_team = home_team
        self.away_team = away_team
        self.game_state = game_state.GameState(self.home_team, self.away_team, 15)
        self.dice_number = dice_number
        self.offensive_dice_faces = offensive_dice_faces
        self.defensive_dice_faces = defensive_dice_faces
    
    def play_from_scrimmage(self):
        turnover = False
        offensive_rolls = [random.randint(1, self.offensive_dice_faces) for i in range(self.dice_number)]
        defensive_rolls = [random.randint(1, self.defensive_dice_faces) for i in range(self.dice_number)]
        offensive_doubles = check_for_doubles(offensive_rolls)
        defensive_doubles = check_for_doubles(defensive_rolls)
        yards_gained = np.sum(offensive_rolls) - np.sum(defensive_rolls)
        if offensive_doubles > 0 and defensive_doubles < 0:
            yards_gained += 10
        elif offensive_doubles > 0 and defensive_doubles > 0:
            yards_gained = 10 * (offensive_doubles - defensive_doubles)
            if yards_gained <= 0:
                turnover = True
        self.game_state.update_state(yards_gained, turnover, time_elapsed=0.4)
    def field_goal_try(self):
        return random.randint(1, 50) + 15 - self.game_state.yards_to_goal() >= 0
    def kick_field_goal(self):
        self.game_state.update_state(0, is_kick_good=self.field_goal_try(), time_elapsed=0.1)
    def punt(self):
        self.game_state.update_state(30 + random.randint(1, 10) + random.randint(1, 10), punt=True, time_elapsed=0.2)
    def kickoff(self):
        # TODO: come up with a dice model for how to proper kickoffs.
        # so far this function just assumes you always get an NFL-rules touchback
        self.game_state.update_state(30, time_elapsed=0)
    def play_fourth_down(self):
        if self.game_state.yards_to_goal() <= 35:
            self.kick_field_goal()
        elif random.randint(1, 10) > self.game_state.distance + (self.game_state.yards_to_goal() // 10):
            self.play_from_scrimmage
        else:
            self.punt()
    def kick_pat(self):
        kick = random.randint(1, 10) > 1
        self.game_state.update_state(0, is_kick_good=kick)
    def simulate_game(self):
        while not self.game_state.game_is_over:
            if self.game_state.down == "kickoff":
                self.kickoff()
            elif self.game_state.down_counter in [1, 2, 3]:
                """ if self.game_state.current_quarter in [2, 4] and self.game_state.time_remaining <= 0.5 and self.game_state.away_score - self.game_state.home_score <= -3:
                    self.kick_field_goal()
                else: """
                self.play_from_scrimmage()
            elif self.game_state.down_counter == 4:
                self.play_fourth_down()
            elif self.game_state.down == "PAT":
                self.kick_pat()
            print(self.game_state)
            print()
            time.sleep(1)
if __name__ == '__main__':
    game = DiceGame(Team("Minnesota"), Team("Green Bay", "GB"))
    game.simulate_game()
    print(game.game_state)






        

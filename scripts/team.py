

class Team:
    def __init__(self, team_name, abbreviation = None, mascot = None, division = None, conference = None):
        self.team_name = team_name
        if abbreviation == None:
            self.abbreviation = self.team_name[:3].upper()
        else:
            # cap team name abbreviations at three characters
            self.abbreviation = abbreviation[:3]
        self.mascot = mascot
        self.num_wins = 0
        self.num_losses = 0
        self.num_ties = 0
        self.schedule = []
        self.points_for = []
        self.points_allowed = []
        self.division = division
        self.conference = conference
    def __repr__(self):
        return str(self.team_name)
class Player:
    def __init__(self, player_tuple):
        self.player_id = player_tuple[0]
        self.full_name = player_tuple[1]
        self.team = player_tuple[2]
        self.position = player_tuple[3]
        self.games_played = player_tuple[4]
        self.goals = player_tuple[5]
        self.assists = player_tuple[6]
        self.points = player_tuple[7]
        self.plus_minus = player_tuple[8]
        self.penalty_minutes = player_tuple[9]

""""" SELECT player_id, full_name, team,
 position, games_played, goals, assists, points, 
 plus_minus, penalty_minutes"""
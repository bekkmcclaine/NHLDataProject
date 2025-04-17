import sqlite3
from http.server import BaseHTTPRequestHandler
from NHLPlayerClasses import Player

class NHLDataRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.lower().startswith("/players"):
            self.do_player_detail()
        elif self.path.lower() == "/pittsburgh_penguins":
            self.do_pittsburgh_penguins()
        else:
            self.do_main_index()


    def do_main_index(self):
        with open('templates/PlayerIndex.html') as index_file:
            template = index_file.read()

        players = self.fetch_player_list()
        player_list_html = ""
        for player in players:
            player_list_html += f"<li><a href='/players/{player.player_id}'>{player.full_name}</a></li>\n"


        response = template.replace("{{player_list_items}}", player_list_html)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))


    def do_player_detail(self):
        player_id = self.path.split("/")[-1]
        player = self.fetch_player_detail(player_id)
        with open('templates/PlayerDetail.html') as detail_file:
            template = detail_file.read()

        response = template.replace("{{player_name}}", player.full_name)
        response = response.replace("{{position}}", player.position)

        plays_html = f"""
            <li>Team: {player.team}</li>
            <li>Games Played: {player.games_played}</li>
            <li>Goals: {player.goals}</li>
            <li>Assists: {player.assists}</li>
            <li>Points: {player.points}</li>
            <li>+/-: {player.plus_minus}</li>
            <li>Penalty Minutes: {player.penalty_minutes}</li>
        """
        response = response.replace("{{plays}}", plays_html)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))


    def do_pittsburgh_penguins(self):
        print("Request received for Pittsburgh Penguins page")
        with open('templates/PittsburghPenguins.html') as penguins_file:
            template = penguins_file.read()

        players = self.fetch_penguins_players()
        penguins_player_list_html = ""
        for player in players:
            penguins_player_list_html += f"<li><a href='/players/{player.player_id}'>{player.full_name}</a></li>\n"

        response = template.replace("{{penguins_player_list}}", penguins_player_list_html)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))


    def fetch_player_list(self):
        conn = sqlite3.connect("data/nhl_team_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT player_id, full_name, team, position, games_played, 
            goals, assists, points, plus_minus, penalty_minutes 
            FROM players """)
        contents = cursor.fetchall()
        conn.close()
        return [Player(row) for row in contents]


    def fetch_player_detail(self, player_id):
        conn = sqlite3.connect("data/nhl_team_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT player_id, full_name, team, position, games_played, 
            goals, assists, points, plus_minus, penalty_minutes 
            FROM players as p 
            WHERE p.player_id = ?""",(player_id,))
        row = cursor.fetchone()
        conn.close()
        return Player(row)


    def fetch_penguins_players(self):
        conn = sqlite3.connect("data/nhl_team_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT player_id, full_name, team, position, games_played, goals, 
            assists, points, plus_minus, penalty_minutes 
            FROM players
            WHERE team = 'PIT'""")
        contents = cursor.fetchall()
        conn.close()

        print(f"Fetched Penguins Players: {contents}")
        return [Player(row) for row in contents]

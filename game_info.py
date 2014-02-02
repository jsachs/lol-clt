import json, time, re
from api import LoLAPI

champs_dict = {1: u'Annie',
               2: u'Olaf', 
               3: u'Galio', 
               4: u'TwistedFate', 
               5: u'XinZhao', 
               6: u'Urgot', 
               7: u'Leblanc', 
               8: u'Vladimir', 
               9: u'FiddleSticks', 10: u'Kayle', 11: u'MasterYi', 12: u'Alistar', 13: u'Ryze', 14: u'Sion', 15: u'Sivir', 16: u'Soraka', 17: u'Teemo', 18: u'Tristana', 19: u'Warwick', 20: u'Nunu', 21: u'MissFortune', 22: u'Ashe', 23: u'Tryndamere', 24: u'Jax', 25: u'Morgana', 26: u'Zilean', 27: u'Singed', 28: u'Evelynn', 29: u'Twitch', 30: u'Karthus', 31: u'Chogath', 32: u'Amumu', 33: u'Rammus', 34: u'Anivia', 35: u'Shaco', 36: u'DrMundo', 37: u'Sona', 38: u'Kassadin', 39: u'Irelia', 40: u'Janna', 41: u'Gangplank', 42: u'Corki', 43: u'Karma', 44: u'Taric', 45: u'Veigar', 48: u'Trundle', 50: u'Swain', 51: u'Caitlyn', 53: u'Blitzcrank', 54: u'Malphite', 55: u'Katarina', 56: u'Nocturne', 57: u'Maokai', 58: u'Renekton', 59: u'JarvanIV', 60: u'Elise', 61: u'Orianna', 62: u'MonkeyKing', 63: u'Brand', 64: u'LeeSin', 67: u'Vayne', 68: u'Rumble', 69: u'Cassiopeia', 72: u'Skarner', 74: u'Heimerdinger', 75: u'Nasus', 76: u'Nidalee', 77: u'Udyr', 78: u'Poppy', 79: u'Gragas', 80: u'Pantheon', 81: u'Ezreal', 82: u'Mordekaiser', 83: u'Yorick', 84: u'Akali', 85: u'Kennen', 86: u'Garen', 89: u'Leona', 90: u'Malzahar', 91: u'Talon', 92: u'Riven', 96: u'KogMaw', 98: u'Shen', 99: u'Lux', 101: u'Xerath', 102: u'Shyvana', 103: u'Ahri', 104: u'Graves', 105: u'Fizz', 106: u'Volibear', 107: u'Rengar', 110: u'Varus', 111: u'Nautilus', 112: u'Viktor', 113: u'Sejuani', 114: u'Fiora', 115: u'Ziggs', 117: u'Lulu', 119: u'Draven', 120: u'Hecarim', 121: u'Khazix', 122: u'Darius', 126: u'Jayce', 127: u'Lissandra', 131: u'Diana', 133: u'Quinn', 134: u'Syndra', 143: u'Zyra', 154: u'Zac', 157: u'Yasuo', 222: u'Jinx', 236: u'Lucian', 238: u'Zed', 254: u'Vi', 266: u'Aatrox', 267: u'Nami', 412: u'Thresh'}

def map_champ(champ_id):
    return champs_dict.get(champ_id)

def title_case(string):
    word_list = re.split('_', string)       #re.split behaves as expected
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word.capitalize())
    return " ".join(final)

class LoLGameInfo(object):
    """Class for formatting and displaying game information"""
    def __init__(self, summoner_name=''):
        self.summoner_name = summoner_name
        self.api = LoLAPI('4fad4bde-dfd3-4d2f-8f70-024cbb917b31')

    def get_most_recent_game(self, games):
        """Takes a list of game dictionaries.
           Returns the most recently played game from the games JSON
        """
        game_id = 0
        recent_game = object
        for game in games['games']:
            if game['gameId'] > game_id:
                game_id = game['gameId']
                recent_game = game
        return recent_game

    def summoner_info(self, players):
        """Gets summoner information for players in a game
           Returns a dictionary of the form {id: {name: name, level: lvl}, ...}
        """
        self.player_dict = {}
        player_string = ''
        for player in players:
            player_string += str(player['summonerId']) + ","
        player_names = self.api.get_summoner_by_id(player_string)
        for player_id, info in player_names.iteritems():
            self.player_dict[player_id] = {'name': info['name'],
                                           'level': info['summonerLevel']}
        return self.player_dict

    def current_game_info(self):
        """Gets game and summoner info for a game in progress
           Returns a my_team list and an enemy_team list
           Team lists are of the form [{'name': 'SummonerName', 'champion': 'ChampionName', 'level': lvl}, ...]
        """
        games = self.api.get_game(self.summoner_name)
        current_game = self.get_most_recent_game(games)
        my_team_id = current_game['teamId']
        my_player_info = {'name': self.summoner_name,
                          'level': str(current_game.get('level')),
                          'champion': map_champ(current_game.get('championId'))}
        current_players = current_game['fellowPlayers']
        player_dict = self.summoner_info(current_players)
        my_team = []
        my_team.append(my_player_info)
        enemy_team = []
        for player in current_players:
            player_info = {'name': player_dict.get(str(player['summonerId'])).get('name'),
                           'level': player_dict.get(str(player['summonerId'])).get('level'),
                           'champion': map_champ(player['championId'])}
            if player['teamId'] == my_team_id:
                my_team.append(player_info)
            else:
                enemy_team.append(player_info)
        return my_team, enemy_team

    def team_info(self):
        pass

    def print_current_game_info(self):
        """Prints game and summoner info for a game in progress"""
        my_team, enemy_team = self.current_game_info()
        print
        print "My Team"
        print "---------------------------"
        player = my_team[0]
        print '\033[1m' + player.get('name'),'|',\
              "Level", player.get('level'),\
              "|", player.get('champion')
        for player in my_team[1:]:
            print '\033[0m' + player.get('name'),'|',\
                  "Level", player.get('level'),\
                  "|", player.get('champion')

        print "\nEnemy Team"
        print "---------------------------"
        for player in enemy_team:
            print player.get('name'),'|',\
                  "Level", player.get('level'),\
                  "|", player.get('champion')

    def summoner_stats(self):
            """Gets basic aggregated stats for a summoner"""
            stats = self.api.get_stats_summary(self.summoner_name)
            return stats

    def print_unranked_summoner_stats(self):
            stats = self.summoner_stats()['playerStatSummaries']
            for dto in stats:
                if dto['playerStatSummaryType'] == 'Unranked':
                    wins = dto['wins']
                    agg = dto['aggregatedStats']
                    break
            print "UNRANKED"
            print "---------------------------"
            print "Wins:", wins
            for item in agg:
                print title_case(str(item['name'])) + ": " + str(item['count'])





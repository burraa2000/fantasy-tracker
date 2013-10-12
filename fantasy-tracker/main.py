import ConfigParser
from yahoo_oauth_handler import YahooHandler
import json

if __name__ =='__main__':
    print "Starting your server"
    config_parser=ConfigParser.ConfigParser()
    config_parser.read("init.cfg")
    
    authHandlerYahoo=YahooHandler(config_parser)
    
    print "Getting your league info:"
    jsonResponse=authHandlerYahoo.get_user_leagues('nfl')
    
    games=jsonResponse['fantasy_content']['users']['0']['user'][1]['games']
    for i in range(0,int(games['count'])):
        game = games[str(i)]['game']
        game_key = game[0]['game_key']
        game_id = game[0]['game_id']
        leagues=game[1]['leagues']
        for i in range(0,int(leagues['count'])):
            league_name=leagues[str(i)]['league'][0]['name']
            league_id=leagues[str(i)]['league'][0]['league_id']
            print league_name, league_id
    
    
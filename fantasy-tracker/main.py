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
    

    
    
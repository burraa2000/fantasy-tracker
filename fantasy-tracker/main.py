import ConfigParser
from yahoo_oauth_handler import YahooHandler

if __name__ =='__main__':
    print "Starting your server"
    config_parser=ConfigParser.ConfigParser()
    config_parser.read("init.cfg")
    
    authHandlerYahoo=YahooHandler(config_parser)
    
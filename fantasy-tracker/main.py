from flask import Flask
import ConfigParser
from yahoo_oauth_handler import YahooHandler

app=Flask(__name__)

@app.route('/')
def initialize():
    print "Starting your server"
    config_parser=ConfigParser.ConfigParser()
    config_parser.read("init.cfg")
    authHandlerYahoo=YahooHandler(config_parser)
    print "Getting your league info:"
    leagues=authHandlerYahoo.get_user_leagues('nfl')
    print leagues
    
@app.route('/login_handler')
def handle_login():
    pass
    
    

if __name__ =='__main__':
    app.run()

    
    
from flask import Flask, redirect, url_for, request
import ConfigParser
from yahoo_oauth_handler import YahooHandler

app=Flask(__name__)




@app.route('/')
def initialize():
    print "Starting your server"
    return redirect(authHandlerYahoo.auth_url) 

  
    
@app.route('/handle_login')
def handle_login():
    authHandlerYahoo.authorize_and_return_session(request.args['oauth_verifier'])
    return 'success!!!'

if __name__ =='__main__':
    config_parser=ConfigParser.ConfigParser()
    config_parser.read("init.cfg")
    authHandlerYahoo=YahooHandler(config_parser)
    app.run()
    

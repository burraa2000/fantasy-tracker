from flask import Flask, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
import ConfigParser
import yahoo_oauth_handler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)



class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True)
    access_token=db.Column(db.String(40))
    access_token_secret=db.Column(db.String(40))
    
    def __init__(self, username, access_token, access_token_secret):
        self.username=username
        self.access_token,self.access_token_secret=access_token, access_token_secret
    
    def __repr__(self):
        return '<User %r>' % self.username
    
class League(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    game=db.Column(db.String(10), primary_key=True)
    user_id=db.Column(db.String(80), db.ForeignKey('user.id'))
    
    def __init__(self, game, username):
        self.game, self.username= game, username


@app.route('/')
def initialize():
    # if user cookie is valid then redirect to homepage.
    # else redirect to yahoo login when click link "login to yahoo"
    print "Starting your server"
    return redirect(authHandlerYahoo.auth_url) 
   
@app.route('/handle_login')
def handle_login():
    # redirect to homepage if login is successful
    session = authHandlerYahoo.authorize_and_return_session(request.args['oauth_verifier'])
    user=User(None, session.access_token, session.access_token_secret)
    db.session.add(user)
    db.session.commit()
    leagues = authHandlerYahoo.get_user_leagues('nfl')
    return str(leagues)

@app.route('/home')
def homepage():
    # List your teams
    # Add teams for tracking to database
    #
    pass


if __name__ == '__main__':
    config_parser = ConfigParser.ConfigParser()
    config_parser.read("init.cfg")
    authHandlerYahoo = yahoo_oauth_handler.YahooHandler(config_parser)
    app.run(debug=True)







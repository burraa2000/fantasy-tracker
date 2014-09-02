#!/usr/bin/python

from flask import Flask, redirect, url_for, request, render_template, session
from flask.ext.sqlalchemy import SQLAlchemy
import ConfigParser
from yahoo_oauth_handler import YahooHandler
import constants

app = Flask(__name__)
app.secret_key='not_so_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True)
    password=db.Column(db.String(40))
    credentials=db.relationship('Credential', backref='user', lazy='lazy')
    
    def __init__(self, username, password):
        self.username=username
        self.password=password
    def __repr__(self):
        return '<User %r>' % self.username

class Credential(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    site=db.Column(db.String(40))
    token_secret=db.Column(db.String(80))
    
    def __init__(self, site, token_secret):
        self.site=site
        self.token_secret=token_secret
    
class League(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    game=db.Column(db.String(10), primary_key=True)
    user_id=db.Column(db.String(80), db.ForeignKey('user.id'))
    
    def __init__(self, game, username):
        self.game, self.username= game, username


############ END DB STUFF

@app.route('/')
def initialize():
    return render_template('homepage.html')
   
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method =='POST':
        user=User(request.form['email'], request.form['password'])
        session['name']=request.form['email']
        try:
            if(user is None):
                raise TypeError
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('homepage'))
        except:
            return render_template('register.html', error=True)
    else:
        return render_template('register.html')

@app.route('/auth_yahoo')
def auth_yahoo():
    y_handler= YahooHandler(config_parser)
    return redirect(y_handler.auth_url)
    

@app.route('/login', methods=['GET','POST'])
def login():
    print request.method
    if request.method == 'POST':
        user=User.query.filter_by(username=request.form['email']).first()
        session['name']=user.username
        if(user != None):
            return redirect(url_for('homepage'))
        return 'user not found'
    return render_template('login.html')

@app.route('/handle_login')
def handle_login():
    session = authHandlerYahoo.authorize_and_return_session(request.args['oauth_verifier'])
    user=User.query.filter_by(username=session['name']).first()
    user.credentials.add(Credential(constants.YAHOO, session.client_secret))
    print session.client_secret
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/home')
def homepage():
    return render_template('index.html', login=session['name'])
    
    
    
def leagues():
    leagues= authHandlerYahoo.get_user_leagues('nfl')
    for i in leagues:
        pass
    return str(leagues)


if __name__ == '__main__':
    config_parser = ConfigParser.ConfigParser()
    config_parser.read("init.cfg")
    authHandlerYahoo = YahooHandler(config_parser)
    app.run(debug=True)







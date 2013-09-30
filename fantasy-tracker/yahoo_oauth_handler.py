'''
Created on Sep 29, 2013

@author: eric
'''

import constants
from rauth import OAuth1Service
import webbrowser

class YahooHandler(object):
    '''
    classdocs
    '''
    REQUEST_TOKEN_URL = "https://api.login.yahoo.com/oauth/v2/get_request_token"
    AUTHORIZE_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'
    ACCESS_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_token'
#     BASE_URL = 'https://api.login.yahoo.com/oauth/v2/'
    BASE_URL = 'http://fantasysports.yahooapis.com/fantasy/v2/'

    def __init__(self,config_parser):
        '''
        Constructor
        '''
        self._service=self.createService(config_parser)
        request_token, request_token_secret = self._service.get_request_token(data = { 'oauth_callback': "oob" })
        print request_token, request_token_secret
        auth_url=self._service.get_authorize_url(request_token)
        webbrowser.open(auth_url)
        oauth_verifier=raw_input("Enter verifier code from the website:")
        self._session=self._service.get_auth_session(request_token, request_token_secret, data = {'oauth_verifier':oauth_verifier})
        self.persist()
        print "Session Created successfully."
        
    def make_request(self,request_url):
        response=self._session.get(request_url,
                                   params={'format':'json'})
        return response.json()
    
    def createService(self,config_parser):
        return OAuth1Service(consumer_key=config_parser.get('YahooAuth', 'CONSUMER_KEY'),
                      consumer_secret=config_parser.get('YahooAuth', 'CONSUMER_SECRET'),
                      name='yahoo',
                      access_token_url=self.ACCESS_TOKEN_URL,
                      authorize_url=self.AUTHORIZE_URL,
                      request_token_url=self.REQUEST_TOKEN_URL,
                      base_url=self.BASE_URL,
                    )
        
    def persist(self):
        print "Attempting to persist."
        
    def get_user_leagues(self,game_code):
        request_url=''.join([self.BASE_URL,'users;use_login=1/games;game_keys=',game_code,'/leagues'])
        return self.make_request(request_url)
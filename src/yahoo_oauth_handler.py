'''
Created on Sep 29, 2013

@author: eric
'''

import constants
from rauth import OAuth1Service

class RequestFail(Exception):
    pass


class YahooHandler(object):
    '''
    classdocs
    '''
    REQUEST_TOKEN_URL = "https://api.login.yahoo.com/oauth/v2/get_request_token/"
    AUTHORIZE_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'
    ACCESS_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_token'
#     BASE_URL = 'https://api.login.yahoo.com/oauth/v2/'
    BASE_URL = 'http://fantasysports.yahooapis.com/fantasy/v2/'

    def __init__(self, config_parser, callback='oob'):
        '''
        Constructor
        '''
        self._service = self.createService(config_parser)
        print self._service.consumer_key
        print self._service.consumer_secret
#         self.request_token, self.request_token_secret = self._service.get_request_token(data={ 'oauth_callback': "http://127.0.0.1:5000/handle_login" })
        self.request_token, self.request_token_secret = self._service.get_request_token(data={ 'oauth_callback': "http://127.0.0.1:5000/handle_login" })
        self.auth_url = self._service.get_authorize_url(self.request_token)
        print "Session Created successfully."
        
    def make_request(self, request_url):
        response = self._session.get(request_url,
                                   params={'format':'json'})
        jsonresponse = response.json()
        if 'error' in jsonresponse.keys():
            raise RequestFail('bad request:' + request_url)
        return jsonresponse
    
    def createService(self, config_parser):
        return OAuth1Service(consumer_key=config_parser.get('YahooAuth', 'CONSUMER_KEY'),
                      consumer_secret=config_parser.get('YahooAuth', 'CONSUMER_SECRET'),
                      name='yahoo',
                      access_token_url=self.ACCESS_TOKEN_URL,
                      authorize_url=self.AUTHORIZE_URL,
                      request_token_url=self.REQUEST_TOKEN_URL,
                      base_url=self.BASE_URL
                    )
        
    def persist(self):
        print "Attempting to persist."
    
    def authorize_and_return_session(self, verifier):
        print self.request_token, self.request_token_secret
        self._session = self._service.get_auth_session(self.request_token, self.request_token_secret, data={'oauth_verifier':verifier})
        return self._session
    
    
    
    
    
    ## Get leagues that you are in
    def get_user_leagues(self, game_code):
        request_url = ''.join([self.BASE_URL, 'users;use_login=1/games;game_keys=', game_code, '/leagues'])
        jsonResponse = self.make_request(request_url)
        games = jsonResponse['fantasy_content']['users']['0']['user'][1]['games']
        list_leagues = []
        for i in range(0, int(games['count'])):
            game = games[str(i)]['game']
            leagues = game[1]['leagues']
            for i in range(0, int(leagues['count'])):
                league_name = leagues[str(i)]['league'][0]['name']
                league_id = leagues[str(i)]['league'][0]['league_id']
                list_leagues.append((league_id, league_name))
        return list_leagues


    ## Get players that you own.

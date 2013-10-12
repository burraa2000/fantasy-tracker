'''
Created on Sep 29, 2013

@author: eric
'''

import constants
from rauth import OAuth1Service
import webbrowser

class RequestFail(Exception):
    pass


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
        auth_url=self._service.get_authorize_url(request_token)
        webbrowser.open(auth_url)
        oauth_verifier=raw_input("Enter verifier code from the website:")
        self._session=self._service.get_auth_session(request_token, request_token_secret, data = {'oauth_verifier':oauth_verifier})
        self.persist()
        print "Session Created successfully."
        
    def make_request(self,request_url):
        response=self._session.get(request_url,
                                   params={'format':'json'})
        jsonresponse=response.json()
        if 'error' in jsonresponse.keys():
            raise RequestFail('bad request:'+ request_url)
        return jsonresponse
    
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
        jsonResponse=self.make_request(request_url)
        games=jsonResponse['fantasy_content']['users']['0']['user'][1]['games']
        list_leagues=[]
        for i in range(0,int(games['count'])):
            game = games[str(i)]['game']
#             game_key = game[0]['game_key']
#             game_id = game[0]['game_id']
            leagues=game[1]['leagues']
            for i in range(0,int(leagues['count'])):
                league_name=leagues[str(i)]['league'][0]['name']
                league_id=leagues[str(i)]['league'][0]['league_id']
                list_leagues.append((league_id,league_name))
        return list_leagues
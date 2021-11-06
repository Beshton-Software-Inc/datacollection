from jsonlogging import *
import ast  
import logging
import time 
import json 
import base64
import collections
import contextlib
import sys
import wave
import os
import webrtcvad
import boto3
import requests
from requests.auth import HTTPBasicAuth 
from pydub import AudioSegment
import base64
from datetime import datetime
from datetime import timedelta

LOG = logging.getLogger()
WORKFIT_API_BASE_URL = os.getenv('WORKFIT_API_BASE_URL', "https://api.uscentral1-0.cint.vcra.co")
WORKFIT_API_TOKEN_URL = os.getenv('WORKFIT_API_TOKEN_URL',"https://api.uscentral1-0.cint.vcra.co/oauth/token")
# WORKFIT_API_BASE_URL = os.getenv('WORKFIT_API_BASE_URL', "https://api.uswest2-0.cstage.vcra.co")
# WORKFIT_API_TOKEN_URL = os.getenv('WORKFIT_API_TOKEN_URL',"https://api.uswest2-0.cstage.vcra.co/oauth/token")
OAUTH_CONFIG = {
    'client_id': os.getenv('WORKFIT_API_CLIENT_ID','5b91b1fac98454c81388563a1df2882d896df6ee715054b08fccd26bd4945bca'),
    'client_secret': os.getenv('WORKFIT_API_CLIENT_SECRET','d43f538869bfc3127b42e46bdc19923604106a17123156ab26460c52edb3c634'),
    # 'client_id': os.getenv('WORKFIT_API_CLIENT_ID','bdcf3a4fc50f551d92ca77e3e06ec731f24fe4f77537590dd174ac5e69c88559'),
    # 'client_secret': os.getenv('WORKFIT_API_CLIENT_SECRET','fe6da7da3ecdff97ac07aca4ba8a9ab09fc3767ac367d141632510ed129b1eca'),
    'grant_type': 'client_credentials',
    'scope': 'admin',
}


class wrapi:
    def __init__(self):
        self.__token__ = None
        self.__expires__ = datetime.utcnow() 
 
    def get_meeting_info(self, meeting_id,):
        try:
            LOG.info({"message": "get information for meeting %s" % (meeting_id,)})
            self.get_admin_token()
            headers = {'Authorization': 'Bearer ' +  self.__token__}
            response = requests.get(WORKFIT_API_BASE_URL + '/v1/meetings/' + meeting_id, headers=headers, timeout=5)
            if int(response.status_code/100) != 2:
                LOG.error({"message":"call wrapi get meeting info failed. default to trainable=False, ensemble=True "} )
                return False, True, None, "unknown", "unknown", None, None
            #now two boolean flags replaced the percentage:
            # trainable = int(response.json()["trainable_shard_percent"]) > 0
            # LOG.info({"message": response.json})
            full_trainable = response.json()["trainable_support_full_training_data"]
            partial_trainable = response.json()["trainable_support_partial_training_data"]
            
            trainable = partial_trainable or full_trainable
            ensemble = (response.json()["enable_ensemble"])
            start_at_utc = response.json()["start_at_utc"]
            meeting_source = response.json()["source"]
            language = response.json()["language"]
            sharder = response.json()["sharder"]
            status = response.json()["status"]
            LOG.info({"message":"call wrapi get meeting info success. trainable=%s,ensemble=%s, sharder=%s lang=%s status=%s" %(trainable, ensemble, sharder, language, status)} )
            return (trainable, ensemble, start_at_utc, meeting_source, language, sharder, status)
        except Exception as ex:
            LOG.warn({"message":"failed to post to wrapi: %s" % (ex,) })
            return (None, None, None, "unknown", "unknown", None, None)

    def get_admin_token(self):
        if self.__token__ == None or self.__expires__ < (datetime.utcnow() + timedelta(seconds=5)):
            response = requests.post(WORKFIT_API_TOKEN_URL, json=OAUTH_CONFIG)
            if response.status_code != 200:
                LOG.error({"message":"call wrapi get token failed. "})
                raise Exception('Failed to get admin token')
            self.__token__=response.json()['access_token']
            self.__expires__ = datetime.utcnow() + timedelta(seconds = response.json()["expires_in"])
            
    def post_to_wrapi(self, meeting_id, sts):
        try:
            self.get_admin_token()
            headers = {'Authorization': 'Bearer ' +  self.__token__}
            try:
                response = requests.put(WORKFIT_API_BASE_URL + '/v1/meetings/' + meeting_id,\
                    headers=headers, json=sts, timeout=5)
                if int(response.status_code/100) != 2:
                    LOG.error({"message":"call wrapi update meeting status failed. "} )
                    raise("Failed call wrapi")
                return True
            except Exception as ex: #give it another try if failed.
                response = requests.put(WORKFIT_API_BASE_URL + '/v1/meetings/' + meeting_id,\
                    headers=headers, json=sts, timeout=5)
                if int(response.status_code/100) != 2:
                    LOG.error({"message":"call wrapi update meeting status failed. "} )
                    return False
                return True
        except Exception as ex:
            LOG.warn({"message":"failed to post to wrapi: %s" % (ex,) })
            return False

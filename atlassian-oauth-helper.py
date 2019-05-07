#!/usr/bin/env python3

import argparse
import requests
import requests_oauthlib
from requests_oauthlib import OAuth1Session
import sys

parser = argparse.ArgumentParser(description='Atlassian OAuth helper')
parser.add_argument('BASEURL', help='The base URL (with context) of \
                    your JIRA/Confluence instance. e.g. \
                    "https://www.example.com/confluence"')
parser.add_argument('CONSUMER', help='The consumer key specified \
                    when the Jira/Confluence application link was set \
                    up.')
parser.add_argument('KEYFILE', help='The private RSA key used to set \
                    up your Jira/Confluence application link.')
args = parser.parse_args()

client_key = args.CONSUMER
base_url = '{}/plugins/servlet/oauth/'.format(args.BASEURL)

try:
    client_secret = open(args.KEYFILE).read()
except FileNotFoundError:
    print('Unable to open RSA key. Check path/permissions to file.')
    sys.exit()

#########################################
# OAuth Stage 1: Obtain a request token #
#########################################

oauth = OAuth1Session(client_key, signature_method='RSA-SHA1',
                      rsa_key=client_secret, callback_uri='oob')
try:
    fetch_response = oauth.fetch_request_token(base_url + 'request-token')
except requests.exceptions.ConnectionError:
    print(('Unable to resolve host or connection refused. '
          'Check URL and context is correct.'))
    sys.exit()
except requests.exceptions.Timeout:
    print(('Connection timed out. Is your Jira/Confluence '
           'instance available/reachable?'))
    sys.exit()
except requests_oauthlib.oauth1_session.TokenRequestDenied:
    print(('Authorization failed. Is your application link '
           'configured correctly?'))
    sys.exit()
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

#################################################
# OAuth Stage 2: Obtain authorization from user #
#################################################

authorization_url = oauth.authorization_url(base_url + 'authorize')
print(('Click on the following link, and log in with the user you '
       'want to use for this application. Make a note of the code '
       'JIRA spits out, and then come back here.'))
print(authorization_url + '\n')
verifier = input('Paste the verification code here: ')

##########################################
# OAuth Stage 3: Request an access token #
##########################################

oauth = OAuth1Session(client_key, signature_method='RSA-SHA1',
                      rsa_key=client_secret,
                      resource_owner_key=resource_owner_key,
                      resource_owner_secret=resource_owner_secret,
                      verifier=verifier)
try:
    oauth_token = oauth.fetch_access_token(base_url + 'access-token')
except requests_oauthlib.oauth1_session.TokenRequestDenied:
    print('Authorization failed. Verification code incorrect?')
    sys.exit()
resource_owner_key = oauth_token.get('oauth_token')
resource_owner_secret = oauth_token.get('oauth_token_secret')

print('OAuth key: ' + resource_owner_key)
print('OAuth secret: ' + resource_owner_secret)


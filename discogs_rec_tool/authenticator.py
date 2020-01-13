import sys
import discogs_client
from discogs_client.exceptions import HTTPError

USER_AGENT = 'discogs_search_tool'

def run_oauth():
    if personal_token_check():
        access_token = get_personal_token()
        return discogs_client.Client(USER_AGENT, user_token=access_token)
    else:
        return new_client_authorization()


def personal_token_check():
    has_personal_token = ''
    while has_personal_token.lower() != 'y' and has_personal_token.lower() != 'n':
        has_personal_token = input('Do you have a personal access token? [y/n]: ')

    if has_personal_token == 'y':
        return True
    return False


def get_personal_token():
    try:
        f = open('personal_access_token.txt', 'r')
        access_token = f.readline().strip()
        return access_token
    except FileNotFoundError:
           return input('Enter personal access token: ')
    else:
        return False


def new_client_authorization():
    CONSUMER_KEY = 'dRWuEIUFudONhVsYyoPa'
    CONSUMER_SECRET = 'YBREVPKyCdoUBUdvYerSHruZMMcENONj'
    d = discogs_client.Client(USER_AGENT)
    d.set_consumer_key(CONSUMER_KEY, CONSUMER_SECRET)
    token, secret, url = d.get_authorize_url()

    print(' ==Request Token== ')
    print(f'    * ouath_token        = {token}')
    print(f'    * ouath_token_secret = {secret}')
    print()
    print(f'Retrieve authentication token from: {url}')

    accepted = ''
    while accepted.lower() != 'y':
        print()
        accepted = input('Token ready? [y/n] :')

    oauth_verifier = input('Verification code: ')

    try:
        access_token, access_secret = d.get_access_token(oauth_verifier)
    except HTTPError:
        print('Unable to authenticate.')
        sys.exit(1)

    return d

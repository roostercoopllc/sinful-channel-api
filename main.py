import os
import yaml
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope

with open('channel-rewards.yml', 'r', encoding='utf-8') as fi:
    conf = yaml.load(fi, Loader=yaml.SafeLoader)

# Twitch specific stuff.
twitch = Twitch(conf['clientId'], conf['clientSecrets'])
twitch.authenticate_app([])

# OAuth token
app_auth = twitch.get_app_token()
print(f'App Token: {app_auth}')
target_scope = [AuthScope.CHANNEL_MANAGE_REDEMPTIONS, AuthScope.CHANNEL_READ_REDEMPTIONS]
user_auth = UserAuthenticator(twitch, target_scope, force_verify=False)
token, refresh_token = user_auth.authenticate()
twitch.set_user_authentication(token, target_scope, refresh_token)
print(f'Token: {token}, Refresh_Token: {refresh_token}')
conf['user_token'] = token
conf['refresh_token'] = refresh_token

# Methods that do work
def sync_rewards():
    pass

if __name__ == '__main__':
    print('Channel Points Thing is running')
    print(app_auth)


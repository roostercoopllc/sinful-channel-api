import os
import yaml
from twitchAPI.twitch import Twitch

with open('channel-rewards.yml', 'r', encoding='utf-8') as fi:
    conf = yaml.load(fi, Loader=yaml.SafeLoader)

# Twitch specific stuff.
twitch = Twitch(conf['clientId'], conf['clientSecrets'])
twitch.authenticate_app([])

# OAuth token
app_auth = twitch.get_app_token()

def sync_rewards():
    pass

if __name__ == '__main__':
    print('Channel Points Thing is running')
    print(app_auth)


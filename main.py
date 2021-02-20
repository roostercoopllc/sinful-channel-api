import os
import uuid
import yaml
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from twitchAPI.pubsub import PubSub
from pprint import pprint
from uuid import UUID

with open('channel-rewards.yml', 'r', encoding='utf-8') as fi:
    conf = yaml.load(fi, Loader=yaml.SafeLoader)

def callback_whisper(uuid: UUID, data: dict) -> None:
    print('got callback for UUID ' + str(uuid))
    pprint(data)


# Twitch specific stuff.
twitch = Twitch(conf['clientId'], conf['clientSecrets'])
twitch.authenticate_app([])
target_scope = [AuthScope.CHANNEL_MANAGE_REDEMPTIONS, AuthScope.CHANNEL_READ_REDEMPTIONS, AuthScope.WHISPERS_READ, AuthScope.WHISPERS_EDIT]

# OAuth token
app_auth = twitch.get_app_token()
print(f'App Token: {app_auth}')
user_auth = UserAuthenticator(twitch, target_scope, force_verify=False)
token, refresh_token = user_auth.authenticate()
twitch.set_user_authentication(token, target_scope, refresh_token)
user_id = twitch.get_users(logins=['Sinfathisar19'])['data'][0]['id']
print(f'Token: {token}, Refresh_Token: {refresh_token}')
conf['userToken'] = token
conf['refreshToken'] = refresh_token

pubsub = PubSub(twitch)
pubsub.start()
uuid = pubsub.listen_whispers(user_id, callback_whisper)
input('press ENTER to close...')
pubsub.unlisten(uuid)
pubsub.stop()

# Methods that do work
def sync_rewards():
    pass

if __name__ == '__main__':
    print('Channel Points Thing is running')


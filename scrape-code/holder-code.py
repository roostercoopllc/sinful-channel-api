import obspython as obs
from twitch import TwitchHelix


## Finding Source Object
# source_object = obs.obs_get_source_by_name(source_name)
# print(f'Source Object: {source_object}')

scenes = obs.obs_frontend_get_scenes()
# print(f'Scene Objects: {scenes}')
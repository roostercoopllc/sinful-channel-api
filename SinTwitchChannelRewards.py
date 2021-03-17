#!/usr/bin/env python
# title             : SinTwitchChannelRewards.py
# description       : Uses channel rewards to mess with the broadcaster
# author            : icantiemyshoe 
# date              : 2021 02 24
# version           : 0.1
# dependencies      : - Python 3.6 (https://www.python.org/)
# notes             : Follow this step for this script to work:
#                   : Python:
#                   :   1. Install python (v3.6 and 64 bits, this is important)
#                   :   2. Install requirements (python -m pip install -r requirements.txt)
#                   : OBS:
#                   :   1. Go to Tools › Scripts
#                   :   2. Click the "Python Settings" tab
#                   :   3. Select your python install path
#                   :   4. Click the "Scripts" tab
#                   :   5. Click the "+" button and add this script
#                   :   6. etc.
#                   :
# python_version    : 3.6
# ==============================================================================
import asyncio
import time
import random

import obspython as obs
import rotatescreen
import keyboard
import requests
from obswebsocket import obsws, events  # noqa: E402
from threading import Thread

import debugpy
import websocket

# Working Methods
def screen_flip(duration, angle):
    screen = rotatescreen.get_primary_display()
    screen.rotate_to(angle)
    time.sleep(duration)
    screen.rotate_to(0)

def crazy_keys(duration):
    # Currently this could remap some of the movement keys
    key_list = ['a', 's', 'd', 'w']
    available_list = ['a', 's', 'd', 'w']
    for k in key_list: 
        print('this is my method')
        chosen_key = random.choice(available_list)
        keyboard.remap_key(k, chosen_key)
        available_list.pop(available_list.index(chosen_key))
    time.sleep(duration)
    keyboard.unhook_all()

def camera_whirl():
    screen = rotatescreen.get_primary_display()
    start_pos = screen.current_orientation

    for i in range(1, 5):
        pos = abs((start_pos - i*90) % 360)
        screen.rotate_to(pos)
        time.sleep(1.5)

def mic_mix():
    pass

def grey_grumpkin():
    pass

def brightness_blast():
    pass

def total_chaos(duration):
    screen_flip(duration, 180)
    crazy_keys(duration)
    mic_mix()
    
# Configuration to load with script
live = True
debug_mode = False
twitch_client = None
user_id = ''
client_id = '' 
oauth_token = ''
#TODO do some shit what we talked about
scene_name = ''
scene_object = None
scene_item = None
source_name = ''
source_object = None
screen_flip_reward_name = ''
crazy_keys_reward_name = ''
screen_flip_duration = 120
screen_flip_angle = 180
crazy_keys_duration = 120
total_chaos_duration = 120
# Request specific stuff
URL_BASE = 'https://api.twitch.tv/helix'
# WS_URL = 'wss://pubsub-edge.twitch.tv'
WS_URL = 'localhost'
WS_PORT = 8765 # 80 # 443 # '8765'

# OBS specific scripts
def script_defaults(settings):
    global debug_mode
    if debug_mode: print("[Debug] Loaded Defaults")

    # Authorization Settings
    obs.obs_data_set_default_bool(settings, "debug_mode", debug_mode)
    obs.obs_data_set_default_string(settings, "user_id", user_id)
    obs.obs_data_set_default_string(settings, "client_id", client_id)
    obs.obs_data_set_default_string(settings, "oauth_token", oauth_token)

    # Variable names
    obs.obs_data_set_default_string(settings, "scene_name", scene_name)
    obs.obs_data_set_default_string(settings, "source_name", source_name)
    obs.obs_data_set_default_string(settings, "screen_flip_reward_name", screen_flip_reward_name)
    obs.obs_data_set_default_string(settings, "crazy_keys_reward_name", crazy_keys_reward_name)
    obs.obs_data_set_default_int(settings, "screen_flip_duration", screen_flip_duration)
    obs.obs_data_set_default_int(settings, "screen_flip_angle", screen_flip_angle)
    obs.obs_data_set_default_int(settings, "crazy_keys_duration", crazy_keys_duration)
    obs.obs_data_set_default_int(settings, "total_chaos_duration", screen_flip_duration)

def script_description():
    return "<b>Redeem rewards from twich channel</b>" + \
    "<hr/>" + \
    "Create your Client-ID here:<br/><a href=\"https://dev.twitch.tv/console/apps/create\">Twitch Dev</a>" # + \
#    "<br/>" + \
#    "Create yout Oauth-Token here (you need channel_read and channel_editor permission):<br/><a href=\"https://twitchtokengenerator.com/quick/8hkFXMYaO0\">twitchtokengenerator.com</a>" + \
#    "<hr/>"

def script_update(settings):
    global user_id
    global client_id
    global oauth_token

    global scene_name
    global scene_object
    global scene_item
    global source_name
    global source_object
    global screen_flip_reward_name
    global crazy_keys_reward_name
    global screen_flip_duration
    global screen_flip_angle
    global crazy_keys_duration
    global total_chaos_duration

    user_id = obs.obs_data_get_string(settings, 'user_id')
    client_id = obs.obs_data_get_string(settings, 'client_id')
    oauth_token = obs.obs_data_get_string(settings, "oauth_token")

    # Reward Settings
    scene_name = obs.obs_data_get_string(settings, "scene_name")
    source_name = obs.obs_data_get_string(settings, "source_name")
    screen_flip_reward_name = obs.obs_data_get_string(settings, "screen_flip_reward_name")
    crazy_keys_reward_name = obs.obs_data_get_string(settings, "crazy_keys_reward_name")
    screen_flip_duration = obs.obs_data_get_int(settings, "screen_flip_duration")
    screen_flip_angle = obs.obs_data_get_int(settings, "screen_flip_angle")
    crazy_keys_duration = obs.obs_data_get_int(settings, "crazy_keys_duration")
    total_chaos_duration = obs.obs_data_get_int(settings, "total_chaos_duration")
        
    scenes = obs.obs_frontend_get_scenes()
    # print(f'Scene Objects: {scenes}')

    ## Finding Scene Object
    for scene in scenes:
        name = obs.obs_source_get_name(scene)
        if name == scene_name:
            scene_object = obs.obs_scene_from_source(scene)
            # print(f'Scene Object: {scene_object}')

    scene_items = obs.obs_scene_enum_items(scene_object)
    obs_trans_info = obs.obs_transform_info()

    for item in scene_items:
        check_source = obs.obs_sceneitem_get_source(item)
        name = obs.obs_source_get_name(check_source)
        if name == source_name:
            revert(item, obs_trans_info)
            # invert(item, obs_trans_info)
            # scene_item = obs.obs_sceneitem_get_info(item)

def script_properties():
    global debug_mode
    if debug_mode: print("[Debug] Loaded Defaults")

    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "user_id", "User ID", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "client_id", "Client ID", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "oauth_token", "Oauth Token", obs.OBS_TEXT_DEFAULT )
    # obs.obs_properties_add_editable_list(props, "twitch", "List of Rewards;Time to Reward;Cool Down", obs.OBS_EDITABLE_LIST_TYPE_STRINGS, obs.OBS_EDITABLE_LIST_TYPE_INT, obs.OBS_EDITABLE_LIST_TYPE_INT)
    
    obs.obs_properties_add_text(props, "scene_name", "Scene Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "source_name", "Source Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_rewards_name", "Screen Flip Rewards name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_reward_name", "Crazy Key Rewards Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_duration", "Screen Flip Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_angle", "Screen Flip Angle [0,90,180,270]", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_duration", "Crazy Keys Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "total_chaos_duration", "Total Chaos Duration (Seconds)", obs.OBS_TEXT_DEFAULT)

    return props

def script_save(settings):
    global debug_mode
    if debug_mode: print("[Debug] Saved properties.")
    script_update(settings)

def script_load(settings):
    global debug_mode

    if debug_mode: print("[TS] Loaded script.")

    # obs.timer_add(just_flip_thing, 5)

    if len(oauth_token) > 0 and len(client_id) > 0:
        # obs.timer_add(set_twitch, check_frequency * check_frequency_to_millisec)
        pass 

def script_unload():
    global debug_mode
    if debug_mode: print("[TS] Unloaded script.")

    # obs.timer_remove(set_twitch)
    
def query_rewards():
    uri = f'{URL_BASE}/channel_points/custom_rewards?broadcaster_id={user_id}'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}"
    }
    return requests.get(uri, headers=headers).json()

def invert(item, trans_info):
    obs.obs_sceneitem_get_info(item, trans_info)
    trans_info.__setattr__('rot', 180)
    trans_info.__setattr__('alignment', 10)
    obs.obs_sceneitem_set_info(item, trans_info)

def revert(item, trans_info):
    obs.obs_sceneitem_get_info(item, trans_info)
    trans_info.__setattr__('rot', 0)
    trans_info.__setattr__('alignment', 5)
    obs.obs_sceneitem_set_info(item, trans_info)

# Twitch Specific Work
"""
async def keep_alive(ws):
    asyncio.sleep(10)
    print('pinging')
    pong_waiter = await ws.ping()
"""

async def handle_reward_redemption(message):
    print(f"Got message: {message}")

def channel_thread():
    ws = obsws(WS_URL, WS_PORT, '')
    ws.register(handle_reward_redemption)
    # ws.register(keep_alive(ws))
    ws.connect()

rewards_thread = Thread(target=channel_thread)
rewards_thread.start()
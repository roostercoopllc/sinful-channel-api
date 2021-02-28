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
import time
import random

import obspython as obs
from twitch import TwitchHelix
import rotatescreen
import keyboard


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
client_secret = ''
oauth_token = ''
#TODO do some shit what we talked about
scene_flip_name = ''
screen_flip_reward_name = ''
crazy_keys_reward_name = ''
screen_flip_duration = 120
screen_flip_angle = 180
crazy_keys_duration = 120
total_chaos_duration = 120

# OBS specific scripts
def script_defaults(settings):
    global debug_mode
    if debug_mode: print("[Debug] Loaded Defaults")

    # Authorization Settings
    obs.obs_data_set_default_bool(settings, "debug_mode", debug_mode)
    obs.obs_data_set_default_string(settings, "user_id", user_id)
    obs.obs_data_set_default_string(settings, "client_id", client_id)
    obs.obs_data_set_default_string(settings, "client_secret", client_secret)

    # Variable names
    obs.obs_data_set_default_string(settings, "scene_flip_name", scene_flip_name)
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
    global client_secret

    global scene_flip_name
    global screen_flip_reward_name
    global crazy_keys_reward_name
    global screen_flip_duration
    global screen_flip_angle
    global crazy_keys_duration
    global total_chaos_duration

    user_id = obs.obs_data_get_string(settings, 'user_id')
    client_id = obs.obs_data_get_string(settings, 'client_id')
    client_secret = obs.obs_data_get_string(settings, "client_secret")

    # Reward Settings
    scene_flip_name = obs.obs_data_get_string(settings, "scene_flip_name")
    screen_flip_reward_name = obs.obs_data_get_string(settings, "screen_flip_reward_name")
    crazy_keys_reward_name = obs.obs_data_get_string(settings, "crazy_keys_reward_name")
    screen_flip_duration = obs.obs_data_get_int(settings, "screen_flip_duration")
    screen_flip_angle = obs.obs_data_get_int(settings, "screen_flip_angle")
    crazy_keys_duration = obs.obs_data_get_int(settings, "crazy_keys_duration")
    total_chaos_duration = obs.obs_data_get_int(settings, "total_chaos_duration")

def script_properties():
    global debug_mode
    if debug_mode: print("[Debug] Loaded Defaults")

    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "user_id", "User ID", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "client_id", "Client ID", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "client_secret", "Client Secret", obs.OBS_TEXT_DEFAULT )
    # obs.obs_properties_add_editable_list(props, "twitch", "List of Rewards;Time to Reward;Cool Down", obs.OBS_EDITABLE_LIST_TYPE_STRINGS, obs.OBS_EDITABLE_LIST_TYPE_INT, obs.OBS_EDITABLE_LIST_TYPE_INT)
    
    obs.obs_properties_add_text(props, "scene_flip_name", "Scene Name to Flip", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_rewards_name", "Screen Flip Rewards name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_reward_name", "Crazy Key Rewards Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_duration", "Screen Flip Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_angle", "Screen Flip Angle [0,90,180,270]", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_duration", "Crazy Keys Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "total_chaos_duration", "Total Chaos Duration (Seconds)", obs.OBS_TEXT_DEFAULT)

    return props

def script_save(settings):
    global debug_mode
    global client_id
    global client_secret
    global oauth_token
    global twitch_client

    if debug_mode: print("[Debug] Saved properties.")
    
    # user id: 475702983

    subscription_types = "channel.channel_points_custom_reward_redemption.update"
    if client_id is not None and client_secret is not None:
        twitch_client = TwitchHelix(client_id=client_id, client_secret=client_secret, scopes=["channel:read:redemptions","",""])

    script_update(settings)

def script_load(settings):
    global debug_mode
    global twitch_settings

    if debug_mode: print("[TS] Loaded script.")

    if len(oauth_token) > 0 and len(client_id) > 0:
        # obs.timer_add(set_twitch, check_frequency * check_frequency_to_millisec)
        pass 

    twitch_settings = obs.obs_frontend_get_scene_names()

def script_unload():
    global debug_mode
    if debug_mode: print("[TS] Unloaded script.")
    
    obs.timer_remove(set_twitch)
     
def set_twitch():
    pass
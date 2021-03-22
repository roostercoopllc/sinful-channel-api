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
import json

import obspython as obs
import rotatescreen
import keyboard
import requests

import debugpy

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
    
# Configuration to load with script
debug_mode = False
user_id = ''
client_id = '' 
oauth_token = ''
scene_name = ''
scene_object = None
scene_item = None
transform_object = None
source_name = ''
source_object = None

screen_flip_reward_title = ''
screen_flip_reward_id = None
screen_flip_duration = 120
screen_flip_angle = 180
screen_flip_cost = 1000
screen_flip_cooldown = 5

crazy_keys_reward_title = ''
crazy_keys_reward_id = None
crazy_keys_duration = 120
crazy_keys_cost = 1500
crazy_keys_cooldown = 5

total_chaos_reward_title = ''
total_chaos_reward_id = None
total_chaos_duration = 120
total_chaos_cost = 5000
total_chaos_cooldown = 5

# OBS specific scripts
def script_defaults(settings):
    global debug_mode
    if debug_mode: print("[Debug] Loaded Defaults")

    # Authorization Settings
    obs.obs_data_set_default_bool(settings, "debug_mode", debug_mode)
    obs.obs_data_set_default_string(settings, "user_id", user_id)
    obs.obs_data_set_default_string(settings, "client_id", client_id)
    obs.obs_data_set_default_string(settings, "oauth_token", oauth_token)

    # Source Objects
    obs.obs_data_set_default_string(settings, "scene_name", scene_name)
    obs.obs_data_set_default_string(settings, "source_name", source_name)
    
    # Screen Flip Data
    obs.obs_data_set_default_string(settings, "screen_flip_reward_title", screen_flip_reward_title)
    obs.obs_data_set_default_int(settings, "screen_flip_duration", screen_flip_duration)
    obs.obs_data_set_default_int(settings, "screen_flip_angle", screen_flip_angle)
    obs.obs_data_set_default_int(settings, "screen_flip_cost", screen_flip_angle)
    obs.obs_data_set_default_int(settings, "screen_flip_cooldown", screen_flip_angle)
    
    # Crazy Keys Data
    obs.obs_data_set_default_string(settings, "crazy_keys_reward_title", crazy_keys_reward_title)
    obs.obs_data_set_default_int(settings, "crazy_keys_duration", crazy_keys_duration)
    obs.obs_data_set_default_int(settings, "crazy_keys_cost", crazy_keys_duration)
    obs.obs_data_set_default_int(settings, "crazy_keys_cooldown", crazy_keys_duration)
    
    # Total Chaos Data
    obs.obs_data_set_default_string(settings, "total_chaos_reward_title", total_chaos_reward_title)
    obs.obs_data_set_default_int(settings, "total_chaos_duration", total_chaos_duration)
    obs.obs_data_set_default_int(settings, "total_chaos_cost", total_chaos_duration)
    obs.obs_data_set_default_int(settings, "total_chaos_cooldown", total_chaos_duration)

def script_description():
    return "<b>Redeem rewards from twich channel</b>" + \
    "<hr/>" + \
    "Create your Client-ID here:<br/><a href=\"https://dev.twitch.tv/console/apps/create\">Twitch Dev</a>"

def script_update(settings):
    global user_id
    global client_id
    global oauth_token

    global scene_name
    global scene_object
    global scene_item

    global source_name
    global source_object

    global transform_object

    global screen_flip_reward_title
    global screen_flip_reward_id
    global screen_flip_duration
    global screen_flip_angle
    global screen_flip_cost
    global screen_flip_cooldown

    global crazy_keys_reward_title
    global crazy_keys_reward_id
    global crazy_keys_duration
    global crazy_keys_cost
    global crazy_keys_cooldown
    
    global total_chaos_reward_title
    global total_chaos_reward_id
    global total_chaos_duration
    global total_chaos_cost
    global total_chaos_cooldown

    user_id = obs.obs_data_get_string(settings, 'user_id')
    client_id = obs.obs_data_get_string(settings, 'client_id')
    oauth_token = obs.obs_data_get_string(settings, "oauth_token")

    # Reward Settings
    scene_name = obs.obs_data_get_string(settings, "scene_name")
    source_name = obs.obs_data_get_string(settings, "source_name")

    # Screen Flip Settings
    screen_flip_reward_title = obs.obs_data_get_string(settings, "screen_flip_reward_title")
    screen_flip_reward_id = obs.obs_data_get_string(settings, "screen_flip_reward_id")
    screen_flip_duration = obs.obs_data_get_int(settings, "screen_flip_duration")
    screen_flip_angle = obs.obs_data_get_int(settings, "screen_flip_angle")
    screen_flip_cost = obs.obs_data_get_int(settings, "screen_flip_cost")
    screen_flip_cooldown = obs.obs_data_get_int(settings, "screen_flip_cooldown")

    # Crazy Keys Settings
    crazy_keys_reward_title = obs.obs_data_get_string(settings, "crazy_keys_reward_title")
    crazy_keys_reward_id = obs.obs_data_get_string(settings, "crazy_keys_reward_id")
    crazy_keys_duration = obs.obs_data_get_int(settings, "crazy_keys_duration")
    crazy_keys_cost = obs.obs_data_get_int(settings, "crazy_keys_cost")
    crazy_keys_cooldown = obs.obs_data_get_int(settings, "crazy_keys_cooldown")

    # Total Chaos Settings
    total_chaos_reward_title = obs.obs_data_get_string(settings, "total_chaos_reward_title")
    total_chaos_reward_id = obs.obs_data_get_string(settings, "total_chaos_reward_id")
    total_chaos_duration = obs.obs_data_get_int(settings, "total_chaos_duration")
    total_chaos_cost = obs.obs_data_get_int(settings, "total_chaos_cost")
    total_chaos_cooldown = obs.obs_data_get_int(settings, "total_chaos_cooldown")

    ## Finding Scene Object
    scenes = obs.obs_frontend_get_scenes()
    transform_object = obs.obs_transform_info()

    for scene in scenes:
        name = obs.obs_source_get_name(scene)
        if name == scene_name:
            scene_object = obs.obs_scene_from_source(scene)
            scene_items = obs.obs_scene_enum_items(scene_object)

            for item in scene_items:
                check_source = obs.obs_sceneitem_get_source(item)
                name = obs.obs_source_get_name(check_source)

def script_properties():
    global debug_mode
    if debug_mode: print("[Debug] Loaded Defaults")

    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "user_id", "User ID", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "client_id", "Client ID", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "oauth_token", "Oauth Token", obs.OBS_TEXT_DEFAULT )
    
    # Source Objects
    obs.obs_properties_add_text(props, "scene_name", "Scene Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "source_name", "Source Name", obs.OBS_TEXT_DEFAULT)

    # Screen Flip Properties
    obs.obs_properties_add_text(props, "screen_flip_rewards_title", "Screen Flip Rewards Title", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_duration", "Screen Flip Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_angle", "Screen Flip Angle [0,90,180,270]", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_cost", "Screen Flip Cost (Points)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_cooldown", "Screen Flip Cooldown (Minutes)", obs.OBS_TEXT_DEFAULT)

    # Crazy Keys Properties
    obs.obs_properties_add_text(props, "crazy_keys_reward_title", "Crazy Key Rewards Title", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_duration", "Crazy Keys Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_cost", "Crazy Keys Cost (Points)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_cooldown", "Crazy Keys Cooldown (Minutes)", obs.OBS_TEXT_DEFAULT)

    # Total Chaos Properties
    obs.obs_properties_add_text(props, "total_chaos_reward_title", "Total Chaos Rewards Title", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "total_chaos_duration", "Total Chaos Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "total_chaos_cost", "Total Chaos Cost (Points)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "total_chaos_cooldown", "Total Chaos Cooldown (Minutes)", obs.OBS_TEXT_DEFAULT)

    obs.obs_properties_add_button(props, "button1", "Update the Script", make_the_rewards)
    
    return props

def script_save(settings):
    global debug_mode
    if debug_mode: print("[Debug] Saved properties.")
    script_update(settings)

def script_load(settings):
    global debug_mode

    if debug_mode: print("[TS] Loaded script.")

    if len(oauth_token) > 0 and len(client_id) > 0:
        # obs.timer_add(set_twitch, check_frequency * check_frequency_to_millisec)
        pass 

def script_unload():
    global debug_mode
    if debug_mode: print("[TS] Unloaded script.")

    # obs.timer_remove(set_twitch)

# OBS Sources Formatting
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

# Twitch Channel Rewards work
def make_the_rewards(props, prop, *args, **kwargs):
    global screen_flip_reward_id
    global crazy_keys_reward_id    
    global total_chaos_reward_id
    print('This is clicking at least')
    if screen_flip_reward_id is not None:
        pass
    else:
        pass

    if crazy_keys_reward_id is not None:
        pass
    else:
        pass

    if total_chaos_reward_id is not None:
        pass
    else:
        pass 

def get_custom_rewards():
    uri = f'https://api.twitch.tv/helix/channel_points/custom_rewards?broadcaster_id={user_id}'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/json"
    }
    rewards_requests = requests.get(uri, headers=headers).json()
    return rewards_requests

def create_custom_rewards(title, cost, cooldown):
    uri = f'https://api.twitch.tv/helix/channel_points/custom_rewards?broadcaster_id={user_id}'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "title": title,
        "cost": cost,
        "is_enabled": True,
        "is_global_cooldown_enabled": True,
        "global_cooldown_seconds": cooldown * 60
    })
    create_request = requests.post(uri, headers=headers, data=data).json()
    return create_request

def update_custom_rewards(id, title, cost, cooldown):
    uri = f'https://api.twitch.tv/helix/channel_points/custom_rewards?broadcaster_id={user_id}&id={id}'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "title": title,
        "cost": cost,
        "is_enabled": True,
        "is_global_cooldown_enabled": True,
        "global_cooldown_seconds": cooldown * 60
    })
    update_request = requests.patch(uri, headers=headers, data=data).json()
    return update_request

def poll_for_redemptions(reward_id):
    uri = f'https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions?broadcaster_id={user_id}&reward_id={reward_id}&status=UNFULFILLED'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/json"
    }
    redemptions_request = requests.get(uri, headers=headers).json()
    return redemptions_request

def fulfill_rewards(reward_id, redemption_id):
    uri = f'https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions?broadcaster_id=${user_id}&reward_id=${reward_id}&id={redemption_id}'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "status": "FULFILLED"
    })
    fulfill_request = requests.patch(uri, headers=headers, data=data).json()
    return fulfill_request

# Crap code
def obs_screen_flip(duration, angle):
    while True:
        time.sleep(duration)
        print(f'Screen Flip Method: {duration}, {angle}')
        screen = rotatescreen.get_primary_display()
        print('Screen Flip')
        invert(scene_item, transform_object)
        screen.rotate_to(angle)
        time.sleep(duration)
        screen.rotate_to(0)
        print('Screen Flip Back')
        revert(scene_item, transform_object)

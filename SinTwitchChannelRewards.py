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
import json
from threading import Thread
from datetime import datetime

import obspython as obs
from requests.api import head, request
import rotatescreen
import keyboard
import requests

import debugpy

# Working Methods
def screen_flip(duration, angle):
    invert(scene_item, transform_object)
    screen = rotatescreen.get_primary_display()
    screen.rotate_to(angle)
    time.sleep(duration)
    screen.rotate_to(0)
    revert(scene_item, transform_object)

def crazy_keys(duration):
    # Currently this could remap some of the movement keys
    key_list = ['a', 's', 'd', 'w']
    available_list = ['a', 's', 'd', 'w']
    for k in key_list: 
        chosen_key = random.choice(available_list)
        keyboard.remap_key(k, chosen_key)
        available_list.pop(available_list.index(chosen_key))
    time.sleep(duration)
    keyboard.unhook_all()

def total_chaos(duration):
    crazy_keys(duration)
    invert(scene_item, transform_object)
    screen_flip(duration, 180)
    revert(scene_item, transform_object)
    
# Future Rewards
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

# Configuration to load with script
LIVE = False

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

transform_object = None

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
    obs.obs_data_set_default_int(settings, "screen_flip_cost", screen_flip_cost)
    obs.obs_data_set_default_int(settings, "screen_flip_cooldown", screen_flip_cooldown)
    
    # Crazy Keys Data
    obs.obs_data_set_default_string(settings, "crazy_keys_reward_title", crazy_keys_reward_title)
    obs.obs_data_set_default_int(settings, "crazy_keys_duration", crazy_keys_duration)
    obs.obs_data_set_default_int(settings, "crazy_keys_cost", crazy_keys_cost)
    obs.obs_data_set_default_int(settings, "crazy_keys_cooldown", crazy_keys_cooldown)
    
    # Total Chaos Data
    obs.obs_data_set_default_string(settings, "total_chaos_reward_title", total_chaos_reward_title)
    obs.obs_data_set_default_int(settings, "total_chaos_duration", total_chaos_duration)
    obs.obs_data_set_default_int(settings, "total_chaos_cost", total_chaos_cost)
    obs.obs_data_set_default_int(settings, "total_chaos_cooldown", total_chaos_cooldown)

def script_description():
    return "<b>Redeem rewards from twich channel</b>" + \
    "<hr/>" + \
    "Create your Client-ID here:<br/><a href=\"https://dev.twitch.tv/console/apps/create\">Twitch Dev</a>"

def script_update(settings):
    global LIVE
    global debug_mode
    global user_id
    global client_id
    global oauth_token

    global scene_name
    global scene_object
    global scene_item

    global source_name
    global source_object

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

    global transform_object

    user_id = obs.obs_data_get_string(settings, 'user_id')
    client_id = obs.obs_data_get_string(settings, 'client_id')
    oauth_token = obs.obs_data_get_string(settings, "oauth_token")

    # Reward Settings
    scene_name = obs.obs_data_get_string(settings, "scene_name")
    source_name = obs.obs_data_get_string(settings, "source_name")

    # Screen Flip Settings
    screen_flip_reward_title = obs.obs_data_get_string(settings, "screen_flip_reward_title")
    screen_flip_reward_id = obs.obs_data_get_string(settings, "screen_flip_reward_id")
    screen_flip_duration = int(obs.obs_data_get_string(settings, "screen_flip_duration"))
    screen_flip_angle = int(obs.obs_data_get_string(settings, "screen_flip_angle"))
    screen_flip_cost = int(obs.obs_data_get_string(settings, "screen_flip_cost"))
    screen_flip_cooldown = int(obs.obs_data_get_string(settings, "screen_flip_cooldown"))

    # Crazy Keys Settings
    crazy_keys_reward_title = obs.obs_data_get_string(settings, "crazy_keys_reward_title")
    crazy_keys_reward_id = obs.obs_data_get_string(settings, "crazy_keys_reward_id")
    crazy_keys_duration = int(obs.obs_data_get_string(settings, "crazy_keys_duration"))
    crazy_keys_cost = int(obs.obs_data_get_string(settings, "crazy_keys_cost"))
    crazy_keys_cooldown = int(obs.obs_data_get_string(settings, "crazy_keys_cooldown"))

    # Total Chaos Settings
    total_chaos_reward_title = obs.obs_data_get_string(settings, "total_chaos_reward_title")
    total_chaos_reward_id = obs.obs_data_get_string(settings, "total_chaos_reward_id")
    total_chaos_duration = int(obs.obs_data_get_string(settings, "total_chaos_duration"))
    total_chaos_cost = int(obs.obs_data_get_string(settings, "total_chaos_cost"))
    total_chaos_cooldown = int(obs.obs_data_get_string(settings, "total_chaos_cooldown"))

    # Set Debug mode
    debug_mode = obs.obs_data_get_bool(settings, "debug_mode")
    LIVE = obs.obs_data_get_bool(settings, "LIVE")

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
                if name == source_name:
                    scene_item = item

    # Making sure that the Oauth Token is valid
    token_status = validate_token()
    if 'login' in token_status.keys() and LIVE:
        print('You have successfully authenticated, redemptions will be read as they appear')
        redemption_thread = Thread(target=loop_over_award_redemptions)
        redemption_thread.start()
    elif LIVE:
        print('Please refresh oauth token')
    elif 'login' not in token_status.keys():
        print('The Oauth Token has expired or is invalid')
    else:
        print('Oauth Token is valid, ready to redeem rewards')

def script_properties():
    global debug_mode
    global screen_flip_reward_id
    global crazy_keys_reward_id
    global total_chaos_reward_id
    if debug_mode: print("[Debug] Loaded Defaults")

    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "user_id", "User ID", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "client_id", "Client ID", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "oauth_token", "Oauth Token", obs.OBS_TEXT_DEFAULT )
    
    # Source Objects
    obs.obs_properties_add_text(props, "scene_name", "Scene Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "source_name", "Source Name", obs.OBS_TEXT_DEFAULT)

    # Screen Flip Properties
    obs.obs_properties_add_text(props, "screen_flip_reward_id", "Screen Flip Rewards Id (Leave blank if not created)", obs.OBS_TEXT_DEFAULT)
    # obs.obs_property_set_visible(screen_flip_reward_id, False)
    obs.obs_properties_add_text(props, "screen_flip_reward_title", "Screen Flip Rewards Title", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_duration", "Screen Flip Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_angle", "Screen Flip Angle [0,90,180,270]", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_cost", "Screen Flip Cost (Points)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "screen_flip_cooldown", "Screen Flip Cooldown (Minutes)", obs.OBS_TEXT_DEFAULT)

    # Crazy Keys Properties
    obs.obs_properties_add_text(props, "crazy_keys_reward_id", "Crazy Keys Rewards Id (Leave blank if not created)", obs.OBS_TEXT_DEFAULT)
    # obs.obs_property_set_visible(crazy_keys_reward_id, False)
    obs.obs_properties_add_text(props, "crazy_keys_reward_title", "Crazy Key Rewards Title", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_duration", "Crazy Keys Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_cost", "Crazy Keys Cost (Points)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "crazy_keys_cooldown", "Crazy Keys Cooldown (Minutes)", obs.OBS_TEXT_DEFAULT)

    # Total Chaos Properties
    obs.obs_properties_add_text(props, "total_chaos_reward_id", "Total Chaos Rewards Id (Leave blank if not created)", obs.OBS_TEXT_DEFAULT)
    # obs.obs_property_set_visible(total_chaos_reward_id, False)
    obs.obs_properties_add_text(props, "total_chaos_reward_title", "Total Chaos Rewards Title", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "total_chaos_duration", "Total Chaos Duration (Seconds)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "total_chaos_cost", "Total Chaos Cost (Points)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "total_chaos_cooldown", "Total Chaos Cooldown (Minutes)", obs.OBS_TEXT_DEFAULT)

    obs.obs_properties_add_button(props, "button1", "Update the reward values", make_the_rewards)
    obs.obs_properties_add_bool(props,"LIVE","Redeem Rewards")
    obs.obs_properties_add_bool(props,"debug_mode","Debug Mode")

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
    global LIVE
    LIVE = False
    revert(scene_item, transform_object)
    if debug_mode: print("[TS] Unloaded script.")

# OBS Sources Formatting
def invert(item, trans_info):
    if trans_info is not None:
        obs.obs_sceneitem_get_info(item, trans_info)
        trans_info.__setattr__('rot', screen_flip_angle)
        trans_info.__setattr__('alignment', 10)
        obs.obs_sceneitem_set_info(item, trans_info)
    else:
        if debug_mode: print(f'Transform Object: {transform_object}')

def revert(item, trans_info):
    if trans_info is not None:
        trans_info = obs.obs_transform_info()
        obs.obs_sceneitem_get_info(item, trans_info)
        trans_info.__setattr__('rot', 0)
        trans_info.__setattr__('alignment', 5)
        obs.obs_sceneitem_set_info(item, trans_info)
    else:
        if debug_mode: print(f'Transform Object: {transform_object}')

# Twitch Channel Rewards work
def make_the_rewards(props, prop, *args, **kwargs):
    global screen_flip_reward_id
    global crazy_keys_reward_id    
    global total_chaos_reward_id
    if debug_mode: print('Attempting to Create or Update the Rewards')
    # Screen Flip Reward Registration
    if screen_flip_reward_id is not None:
        my_reward = create_custom_rewards(screen_flip_reward_title, screen_flip_cost, screen_flip_cooldown)
        if len(my_reward) > 0:
            screen_flip_reward_id = my_reward[0]['id']
        else:
            if debug_mode: print(f'Screen Flip Reward Failed: {my_reward}')
    else:
        update_custom_rewards(screen_flip_reward_id, screen_flip_reward_title, screen_flip_cost, screen_flip_cooldown)
    # Crazy Key Reward Registration
    if crazy_keys_reward_id is not None:
        if len(my_reward) > 0:
            my_reward = create_custom_rewards(crazy_keys_reward_title, crazy_keys_cost, crazy_keys_cooldown)
            crazy_keys_reward_id = my_reward[0]['id']
        else:
            if debug_mode: print(f'Crazy Keys Reward Failed: {my_reward}')
    else:
        update_custom_rewards(crazy_keys_reward_id, crazy_keys_reward_title, crazy_keys_cost, crazy_keys_cooldown)
    # Total Chaos Rewards Registration
    if total_chaos_reward_id is not None:
        if len(my_reward) > 0:
            my_reward = create_custom_rewards(total_chaos_reward_title, total_chaos_cost, total_chaos_cooldown)
            total_chaos_reward_id = my_reward[0]['id']
        else:
            if debug_mode: print(f'Total Chaos Reward Failed: {my_reward}')
    else:
        update_custom_rewards(total_chaos_reward_id, total_chaos_reward_title, total_chaos_cost, total_chaos_cooldown)

def validate_token():
    uri = 'https://id.twitch.tv/oauth2/validate'
    headers = {
        'Authorization': f'Bearer {oauth_token}'
    }
    valid_token = requests.get(uri, headers=headers).json()
    if debug_mode: print(f'valid token request: {valid_token}')
    return valid_token

def get_custom_rewards():
    uri = f'https://api.twitch.tv/helix/channel_points/custom_rewards?broadcaster_id={user_id}'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/json"
    }
    rewards_requests = requests.get(uri, headers=headers).json()['data']
    if debug_mode: print(f'rewards request: {rewards_requests}')
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
    create_request = requests.post(uri, headers=headers, data=data).json()['data']
    if debug_mode: print(f'create request: {create_request}')
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
    update_request = requests.patch(uri, headers=headers, data=data).json()['data']
    if debug_mode: print(f'update request: {update_request}')
    return update_request

def poll_for_redemptions(reward_id):
    uri = f'https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions?broadcaster_id={user_id}&reward_id={reward_id}&status=UNFULFILLED'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/json"
    }
    redemptions_request = requests.get(uri, headers=headers).json()
    if 'data' in redemptions_request.keys():
        return redemptions_request
    if debug_mode: print(f'redemptions request: {redemptions_request}')
    return []

def fulfill_rewards(reward_id, redemption_id):
    if debug_mode: print(f'Fulfilling the rewards with the following information: User Id - {user_id}; Reward Id - {reward_id}; Redemption Id {redemption_id}')
    uri = f'https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions?broadcaster_id=${user_id}&reward_id=${redemption_id}&id={reward_id}'
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "status": "FULFILLED"
    })
    fulfill_request = requests.patch(uri, headers=headers, data=data).json()
    if debug_mode: print(f'fulfill request: {fulfill_request}')
    return fulfill_request

def triage_rewards(reward_type, reward_list):
    if debug_mode: print(f'Reward Type: {reward_type}')
    if debug_mode: print(f'{reward_type} Reward Type: {reward_list}')
    if reward_list['data'].__len__() > 0:
        lucky_reward = reward_list['data'][0]['reward']
        lucky_id = reward_list['data'][0]['id']
        if reward_type == 'screen flip':
            if debug_mode: 
                print(f'Screen Flip Method: {screen_flip_duration}, {screen_flip_angle}')
                print(f'Scene Item: {scene_item}, Transformation Object: {transform_object}')
            invert(scene_item, transform_object)
            screen_flip(screen_flip_duration, screen_flip_angle)
            revert(scene_item, transform_object)
        elif reward_type == 'crazy_keys':
            if debug_mode: print(f'Crazy Keys Method: {crazy_keys_duration}')
            crazy_keys(crazy_keys_duration)
        elif reward_type == 'total_chaos':
            if debug_mode: print(f'Total Chaos Method: {total_chaos_duration}')
            total_chaos(total_chaos_duration)
        # The auto-fulfillment cannot be accomplished automatically because of the following error
        # fulfill request: {'error': 'Unauthorized', 'status': 401, 'message': 'incorrect user authorization'}
        # fulfill_rewards(lucky_id, lucky_reward['id'])
    else:
        print(f'No {reward_type} rewards at this time')

def loop_over_award_redemptions():
    while LIVE:
        time.sleep(30)
        print(f'Looking for rewards {datetime.now()}')
        sf_redemptions = poll_for_redemptions(screen_flip_reward_id)
        triage_rewards('screen flip', sf_redemptions)
        ck_redemptions = poll_for_redemptions(crazy_keys_reward_id)
        triage_rewards('crazy_keys', ck_redemptions)
        tc_redemptions = poll_for_redemptions(total_chaos_reward_id)
        triage_rewards('total_chaos', tc_redemptions)

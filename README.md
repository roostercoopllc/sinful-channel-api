# Sinful-Channel-Points: Twitch Channel Points challenge
## Description
This repository houses the Submission for the https://twitchchannelpoints.devpost.com/ hackathon by Team Sin.

The full competition submission can be found here: https://devpost.com/software/ti-esrever-dna-ti-pilf-nwod-gnaht-ym-tup-i 


## Install


### Requirements 
* OBS (or other streaming content manager that can use python)
* Python3
* Twitch Affiliate or Partner status
* Twitch Channel Points enabled

### Dependancy install
Recommended using virtual environment

##### Windows install
```ps1
pip install virtualenv
python -m venv ./venv
./venv/Scripts/activate
pip install -r requirements.txt
# Need to perform post install (maybe)
python ./venv/Scripts/pywin32_postinstall.py -install
```

##### Linux install
```sh
pip install virtualenv
python -m venv ./venv
./venv/source/activate
pip install -r requirements.txt
```

## Use
* The steamer will be given control of which Features to turn on/off, the channel point price per redemption, the ability to 
* All Feature durations and costs can be determined by the Streamer (or Moderators)
* Feature duration and cost scales with points spent for redemption
* Feature redemptions can be given a global and user-level cooldown rate. Global would affect all users (to include the streamer and moderators), user-level would affect only the individual user who made the initial redemption
* Redeemed points will be deducted from the redeeming user following a confirmation on behalf of the Streamer or moderators; points may be refunded if the redemption is declined
* 

## User Features
* Screen Flip - Rotate the Streamer's screen horizontally, vertically, or both for a period of time (minimum value (seconds) | maximum value (seconds))
* Grey Grumpkin - Change the Streamer's display to gray scale for a period of time (minimum value (seconds) | maximum value (seconds))
* Brightness Blast - Increase the brightness of the Streamer's display for a period of time (minimum value (seconds) | maximum value (seconds))
* Crazy Keys - Switch the ASDW keys to be bound to UIOK where U is "right", I is "down", O is "left", and K is "up" for a period of time (minimum value (seconds) | maximum value (seconds))
* Camera Whirl - REQUIRES CAMERA OVERLAY ENABLED - Change the orientation and position of the Streamer's camera [Rotate (Left, Right), Mirror, Flip, Spin] for a period of time (minimum value (seconds) | maximum value (seconds))
* Mic Mute - Mute the Streamer's microphone for a period of time (minimum value (seconds) | maximum value (seconds))

### Possible Features (Unclear how difficult these are to implement)
* Difficulty Diversion - Change the difficulty level of the game being played (no more than 2 difficulty levels from the Streamer's current difficulty) for a period of time (minimum value (seconds) | maximum value (seconds))



## Super User Features (Streamer and/or Moderators)
* Channel point redemption feed present (module or other integration) within OBS (STREAMER) - The redemption feed will allow the Streamer to approve/decline redemptions from within OBS
* Channel Point redemption overlay - Allow the Streamer to add an overlay to display the most recent redemption and redeeming user


## Run the program
Can be run offline to sync rewards with live stream using API
```sh
python main.py
```

## Team 
- Team Captain: sinfathisar19
- Developer: icantiemyshoe
- Team Mascot: j_urby

## Special Thanks to:
- Teekeks: https://github.com/Teekeks/pyTwitchAPI
- Danny-Burrows: https://github.com/danny-burrows/rotate-screen
- Boppreh: https://github.com/boppreh/keyboard
- UpgradeQ: https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API#docs-and-code-examples 
- twitchApp TokenGenerator: https://twitchapps.com/tokengen/
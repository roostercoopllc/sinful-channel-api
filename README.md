# Sinful-Channel-Points: Twitch Channel Points challenge
## Description
This repository houses the Submission for the https://twitchchannelpoints.devpost.com/ hackathon by Team Sin.

The full competition submission can be found here: 

### Requirements 
* OBS Studios
* Python 3.6
* Twitch CLI - https://github.com/twitchdev/twitch-cli/blob/main/docs/token.md
* Twitch Affiliate or Partner status
* Twitch Channel Points enabled

### Install
```ps1
PS> pip install -r requirements.txt
```

## Use
* The steamer will be given control of which Features to turn on/off, the channel point price per redemption 
* All Feature durations and costs can be determined by the Streamer (or Moderators)
* Redeemed points will be deducted from the redeeming user following a confirmation on behalf of the Streamer or moderators; points may be refunded if the redemption is declined

## Features
* Screen Flip - Rotate the Streamer's screen horizontally, vertically, or both for a period of time (minimum value (seconds) | maximum value (seconds))
* Crazy Keys - Switch the WASD keys to be bound to a different key on WASD (minimum value (seconds) | maximum value (seconds))
* Camera Whirl - REQUIRES CAMERA OVERLAY ENABLED - Change the orientation and position of the Streamer's camera [Rotate (Left, Right), Mirror, Flip, Spin] for a period of time (minimum value (seconds) | maximum value (seconds))
* Total Chaos - Flip the screen, mix up the keys, make it pure chaos.

## Authentication
For your application, you need to have the twitch developer console Oauth Redirect be configured to return to http://localhost:3000

Configure your twitch cli client
```ps1
PS> twitch configure -i <client-id> -s <client-secret> 
```

Grab your user Oauth token
```ps1
PS> twitch token
PS> twitch token -u -s "channel:manage:redemptions channel:read:redemptions"
# Opening browser. Press Ctrl+C to cancel...
# 2021/03/15 10:16:45 User Access Token: fb115lv5e8lk7yn0gsd4arx9v25ia0 # This is the token to put in the Oauth Field
# Refresh Token: 0rpz6o3v5gsgf3tm76hxaxp1vsrhp54ck2hyl0fij9nxr7rx9q
# Expires At: 2021-03-15 17:53:58.4239375 +0000 UTC
# Scopes: [channel:manage:redemptions channel:read:redemptions]
```

## Team 
- Team Captain: sinfathisar19
- Developer: icantiemyshoe, evo
- Team Mascot: j_urby

## Special Thanks to:
- twitchDev: https://github.com/twitchdev/twitch-cli 
- Danny-Burrows: https://github.com/danny-burrows/rotate-screen
- Boppreh: https://github.com/boppreh/keyboard
- UpgradeQ: https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API#docs-and-code-examples 

## Future Features
* Grey Grumpkin - Change the Streamer's display to gray scale for a period of time (minimum value (seconds) | maximum value (seconds))
* Brightness Blast - Increase the brightness of the Streamer's display for a period of time (minimum value (seconds) | maximum value (seconds))
* Difficulty Diversion - Change the difficulty level of the game being played (no more than 2 difficulty levels from the Streamer's current difficulty) for a period of time (minimum value (seconds) | maximum value (seconds))
* Channel point redemption feed present (module or other integration) within OBS (STREAMER) - The redemption feed will allow the Streamer to approve/decline redemptions from within OBS
* Channel Point redemption overlay - Allow the Streamer to add an overlay to display the most recent redemption and redeeming user
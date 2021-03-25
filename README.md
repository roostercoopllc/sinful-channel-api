# Sinful-Channel-Points: Twitch Channel Points Hackathon
## Description
This repository houses the Submission for the https://twitchchannelpoints.devpost.com/ hackathon by Team Sin.

The full competition submission can be found here: https://devpost.com/software/ti-esrever-dna-ti-pilf-nwod-gnaht-ym-tup-i

### Requirements 
* OBS Studios Version 26.x.x or newer
* Python 3.6
* Twitch CLI - https://github.com/twitchdev/twitch-cli/blob/main/docs/token.md
* Twitch Affiliate or Partner status
* Twitch Channel Points enabled

### Install
```ps1
PS> pip install -r requirements.txt
```

## Use
* The steamer will be given control of which Features to turn on/off, the channel point price per redemption, and the duration of both the redemption and the cooldown for each of those redemptions. 
* Redeemed points will be deducted from the redeeming user following a confirmation on behalf of the Streamer or moderators; points may be refunded if the redemption is declined
* The Streamer must have a current version of OBS (Version 26.1.x or newer)
* The Streamer must be a Twitch Affiliate that has the ability to manage rewards in their dashboard.

#### Notes On Usage
* Currently, you need to have all fields marked **"Required"** filled out before "applying" the script.  To apply the script, click the "Update the Rewards" button.
* Clicking **"Update the Rewards"** will create the rewards if they have not previously been created on your Twitch dashbard.  
  * In order to submit field updates, you need to update the rewards ID fields for each Twitch reward.  
  * One easy way to find the reward IDs is to enable debug mode, and copy the IDs from the debug logs.  Once the ID fields have been populated, you can use the **"Update The Rewards"** button to update the rewards' respective information.
* Although the redemptions will populate within your Channel Points (https://dashboard.twitch.tv/u/your_user_name/viewer-rewards/channel-points) all modifications for screen flips, key modifications or Total Chaos **MUST** occur within the OBS dialog.
* **NOTE:** ***You must uncheck "Redeem Rewards" checkbox before closing OBS since we are running a subprocess outside of OBS and will orphan the process if it is not killed via that button or the task manager. (We think we fixed it, but sometimes it doesn't immediately die).***
  * If other problems occur, enable debug mode and view the script logs.

## Features
* Screen Flip - Rotate the Streamer's screen horizontally, vertically, or both for a period of time value in seconds
* Crazy Keys - Switch the WASD keys to be bound to a different key on WASD for a period of time value in seconds
* Total Chaos - Flip the screen, mix up the keys, make it pure chaos for a period of time value in seconds

## Authentication
1. Create an application

* Go to the Twitch Developer console (https://dev.twitch.tv/console/apps)
* Click on **"Register Your Application"**
  * Provide a name for your Application
  * Enter http://localhost:3000 as your OAuth Redirect URL and click **"Add"** to submit this Redirect URL
  * Select a category that best fits your Application and click **"Create"**

2. Retrieve the Application's **Client ID** and **Client Secret** -- **These will be needed and used to authenticate your application to run properly from within OBS**
* On the Application you've just created, click **"Modify"**
* Locate your **"Client ID"**
* Create a **"Client Secret"** by clicking **"New Secret"**
* Click **"Save"**

3. Configure your twitch cli client:
```ps1
PS> twitch configure -i <client-id> -s <client-secret> 
```

4. To grab your user Oauth token: 
```ps1
PS> twitch token
PS> twitch token -u -s "channel:manage:redemptions channel:read:redemptions"
# Opening browser. Press Ctrl+C to cancel...
# 2021/03/15 10:16:45 User Access Token: fb115lv5e8lk7yn0gsd4arx9v25ia0 # This is the token to put in the Oauth Field
# Refresh Token: 0rpz6o3v5gsgf3tm76hxaxp1vsrhp54ck2hyl0fij9nxr7rx9q
# Expires At: 2021-03-15 17:53:58.4239375 +0000 UTC
# Scopes: [channel:manage:redemptions channel:read:redemptions]
```

## Adding the Python Script to OBS
1. Open OBS and locate your Python installation file
* Click on **Tools > Scripts** 
* Click on the **"Python Settings"** tab and **"Browse"** to locate the installation path for your Python version 3.6 -- This may default to exist within your Local AppData folder  - ***%AppData/Local/Programs/Python***

2. Load a new Python Script
* On the **Tools > Scripts** menu, click on the **"Scripts"** tab and the "+" in the bottom left of the screen to browse for your channel rewards Python script (.py)
* Select the appropriate channel rewards Python script (.py)

## Populating the Script within OBS and your rewards within Twitch
1. Locate your User ID
2. Insert your Client ID (taken from your Application's Twitch Developers Console -- https://dev.twitch.tv/console/apps)
3. Insert or create a new OAuth Token 
* Create a new token:
```ps1
PS> twitch token
PS> twitch token -u -s "channel:manage:redemptions channel:read:redemptions"
# Opening browser. Press Ctrl+C to cancel...
# 2021/03/15 10:16:45 User Access Token: fb115lv5e8lk7yn0gsd4arx9v25ia0 # This is the token to put in the Oauth Field
# Refresh Token: 0rpz6o3v5gsgf3tm76hxaxp1vsrhp54ck2hyl0fij9nxr7rx9q
# Expires At: 2021-03-15 17:53:58.4239375 +0000 UTC
# Scopes: [channel:manage:redemptions channel:read:redemptions]
```
4. Provide the Scene name OBS will be referencing -- **This is Case Sensitive**
5. Provide the Source Name to be modified -- **This is Case Sensitive** -- This is what allows the screen flips to be seen viewers and not just the Streamer
6. Populate values for your Rewards *(excluding the Rewards ID when you first create your Rewards)*
7. Click **"Update the reward values"** button -- This will populate these newly created Rewards within your Twitch Channel Points and create an ID for your Rewards
8. OPTIONAL: Provide Rewards IDs for the newly created Rewards
* To generate an ID
  * Open the Scripts dialog -- **Tools > Scripts**
  * Scroll to the bottom of the redemption options list (right side of the **"Scripts"** tab) and turn on **"Debug Mode"**
  * Click the refresh arrows (two arrows on the bottom left of the **"Scripts"** tab)
  * Open the "**Script Log"** and locate your Reward IDs 
 
 ## Allowing Redemptions to occur
 1. Open the Scripts dialog -- **Tools > Scripts**
 2. Click on the **"Scripts"** tab
 3. Scroll to the bottom of the redemption options list (right side of the **"Scripts"** tab) and turn ***ON*** **"Redeem Rewards"** -- This will now begin the python script's process of looking for rewards within the Rewards Redemption queue on Twitch. 
 
 ## Stopping Rewards Redemptions
 1. Open the Scripts dialog -- **Tools > Scripts**
 2. Click on the **"Scripts"** tab
 3. Scroll to the bottom of the redemption options list (right side of the **"Scripts"** tab) and turn ***OFF*** **"Redeem Rewards"** -- This will stop the python script's process of looking for rewards within the Rewards Redemption queue on Twitch.
 
 ## Team 
- Team Captain: sinfathisar19
- Developer: evo, icantiemyshoe 
- Team Mascot: j_urby

## Special Thanks to:
- twitchDev: https://github.com/twitchdev/twitch-cli 
- Danny-Burrows: https://github.com/danny-burrows/rotate-screen
- Boppreh: https://github.com/boppreh/keyboard
- UpgradeQ: https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API#docs-and-code-examples 

## Future Features
* Camera Whirl - REQUIRES CAMERA OVERLAY ENABLED - Change the orientation and position of the Streamer's camera [Rotate (Left, Right), Mirror, Flip, Spin] for a period of time value in seconds
* Grey Grumpkin - Change the Streamer's display to gray scale for a period of time (minimum value (seconds) | maximum value (seconds))
* Brightness Blast - Increase the brightness of the Streamer's display for a period of time (minimum value (seconds) | maximum value (seconds))
* Difficulty Diversion - Change the difficulty level of the game being played (no more than 2 difficulty levels from the Streamer's current difficulty) for a period of time (minimum value (seconds) | maximum value (seconds))
* Channel point redemption feed present (module or other integration) within OBS (STREAMER) - The redemption feed will allow the Streamer to approve/decline redemptions from within OBS
* Channel Point redemption overlay - Allow the Streamer to add an overlay to display the most recent redemption and redeeming user

## Known Bugs
* If OBS is closed while the screen is flipped, the scene will be stuck in the flipped position. This can be fixed by right clicking the scene item and editing the transformation back to the Rotation of 0 and Positional Alignment of Top Left.
  * Right click the effected Source
  * Select Transform > Edit Transform (or Press Ctrl + E)
  * Position X & Y should be set to 0
  * Positional Alignment should be set to **"Top Left"**
* If the screen flips without OBS open, you likely have an abandoned chiled process that you will need to kill from the task manager.

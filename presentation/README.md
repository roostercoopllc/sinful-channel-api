# Flips & Total Chaos

## Inspiration
Remember playing with your friends and they were beating you...what did you do? Tried to get even and win by messing with their controller (unplugging it), standing in front of their side of the tv, switching off the internet, etc. This integration allows you to better mess with your favorite streamers while they are doing what they do best.

## What it does
The script is intended to be imported into OBS Studios and facilitate the redemption of twitch rewards in 3 specific types of rewards. The script facilitates the streamer to flip the screen the game is being played on in unison with the source that displays that screen in OBS. It also facilitates the mixing of keys that are used for directions in a first-person shooter game. Lastly, coordinates performing the two above functions at the same time; giving the feeling of total chaos to the streamer, and unique enjoyment for the fans.

The screen can be rotated at a 90, 180, 270-degree orientation depending on what the streamer wants. There are also functions for full barrel rolls (but requires some more configuration and developement). 

The keys are currently hardcoded (I know, shame on us), but takes the regular WASD keys and momentarily hooks the keystrokes and reassigns them to a different key. For Example, W could become D. However, its fully randomized to where W could stay W, while A becomes D. This becomes especially fun when a streamer plays a single game for a longer period and has high degrees of muscle memory that they cannot rely on anymore.

Obviously, Total Chaos is just that, your orientation is completely mixed up, and your keys will not even be able to be used in a direct orientation to the screen. 

## How we built it
The widget is a single script that is designed to be integrated into OBS Studios 26.1.1. The script is written in python 3.6 since the obs python SWIG wrapper is anchored to that python version. We are also using the twitch-cli to generate the oauth token and expect the streamer to be responsible for the generation, refreshing and revoking of the token. We developed on Visual Studios Code, and referrenced python packages pytwitchAPI and python-twitch-client but did not end up using them since they did not have python 3.6 support for the PubSub api.

## Challenges we ran into
The biggest challenge was to decide the workflow for how points were redeemed while on host devices. The two major user stories we were trying to do decide between was if the rewards should be auto redeemed via the PubSub of the API or if the integration should allow for the streamer to decide when or if they accept the change in the game play. While it would obviously be hilarious if the streamer would have to adapt for the auto redeem, but we discussed that it would be better to allow for the streamer to give a verbal shoutout for the point redemptions while making sure that the points are redeemed for the most entertainment value that would be available. 

We chose the later options because there are times when, for example, if there is a long travel time between tasks or missions, you obviously would want the fan to get the most chaos they could by redeeming it when the streamer gets into a good spot for a valid run. Conversly, the Streamer may be ending the stream after getting to a certain spot when the reward is redeemed, and the fan would not get the full value of the time for the chaos. It is best to just refund the points or leave the rewards unredeemed in the queue for the next stream. 

However, there isn't a really good reward integration inside of obs so we kinda just kludged something together to make it usable for Sinfathisar, and produce a working demo for the event.

However, the auto redemptions would be a future feature where we describe it below, because this feature would be good for performers. 

## Accomplishments that we're proud of
We are proud of being able to coordinate the development effort in only our spare time and across different continants and time zones. 

We are pretty proud of the video also. 

This was also the first time that icantiemyshoe used a SWIG wrapper for python. So, the fact that we were able to sync the device operations with what was reflected on the stream. This really made icantiemyshoe think more about how to integrate online performances with IOT devices and real-world events. 

## What we learned
We also found out that since icantiemyshoe's developer account was not a twitch affiliate, him (and the other developers) were not able to test locally with the point redemptions and had to schedule time with the single affiliate account (Sinfathisar19) to see if the points channel integrations were able to function properly. Obviously, it definitely slowed down development with all of our schedules.

We also desired to manage all the rewards through a simple POST request instead of having to subscribe for the pubsub.

## What's next for Flips and Total Chaos
We had the following as stretch goals and likely explore these some time in the future.
1. Help your friends make your streamer's experience far more challenging. Work together to block streamer's abilities. But, this comes with a cost - it's a gamble for your points every time! 
2. Have a stream of chaos where all redemption costs and cooldowns are reduced. Your viewers will go wild making you lose your mind. 
3. Control your streamer's lighting on their keyboard, their nanoleaf array or other RGB lighting setup. Create a Raspberry Pi companion that controls devices in the set of the streamer. Rewards can be used with the device to change the lighting, music (speed, volume, etc.), or any kind of animatronics that we may make to mess with Sinfathisar. 
4. Visualizations for performers and non-game streamers. It would be fun to allow for a Bonaroo-like experience where the stream video can have the color, orientation, or filters be controlled by redeeming rewards. For example, I could have the reward where the screen will Kaleidoscope and turn rainbow that will enhance the viewing experience of the electronica DJ I want to listen to. This will allow the DJ to keep performing but allow the viewers to experience unique views. 

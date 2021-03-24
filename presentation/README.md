# Flips & Total Chaos

## Inspiration
We created this integration based on old memories of trying to find ways to even the score when playing video games.  Most gamers can relate to playing video games with a friend that you were always losing to.  In retaliation, we would unplug their controller, maybe block the TV or find some other way of evening the score.  Well with our new Twitch integration, we aim to allow a streamer's subscribers to bring the same level of "evening the playing field", forcing the streamer to prove their talents LIVE!


OLD

Remember playing with your friends and they were beating you...what did you do? Tried to get even and win by messing with their controller (unplugging it), standing in front of their side of the tv, switching off the internet, etc. This integration allows you to better mess with your favorite streamers while they are doing what they do best.

OLD


## What it does
The script is intended to be imported into OBS Studios to facilitate the redemption of 3 specific types of Twitch rewards. The first reward causes the streamer's display to flip 180 degrees, in unison with the source that displays that screen in OBS. The second reward results in the mixing of keys that are typically used for directional controls in a first-person shooter game (W,A,S,D). The third reward combines the two, performing both functions at the same time; giving the feeling of total chaos to the streamer, and a unique enjoyment for the fans.

The screen flip reward can be customized to rotate the screen either 90, 180, or 270 degrees.  There are also functions to enable barrel rolls (but will require more configuration and development).


OLD

The screen can be rotated at a 90, 180, 270-degree orientation depending on what the streamer wants. There are also functions for full barrel rolls (but requires some more configuration and developement). 

OLD

The keys are currently hardcoded (I know, shame on us), but takes the regular WASD keys and momentarily hooks the keystrokes and reassigns them to a different key. For Example, W could become D, A would become S. However, it's fully randomized to where W could stay W, while A becomes D. This becomes especially fun when a streamer plays a single game for a longer period and has high degrees of muscle memory that they cannot rely on anymore.

Obviously, Total Chaos is just that, your orientation is changed, and your keys will not even be able to be used in a direct orientation to the screen.

## How we built it
The widget is a single script that is designed to be integrated into OBS Studios 26.1.1. The script is written in Python 3.6 since the OBS Python SWIG wrapper is anchored to that Python version. We are also using twitch-cli to generate the oauth token and require the streamer to be responsible for its generation, refreshing, and revoking of the token. This integration was developed with Visual Studio Code, and originally referenced Python packages pytwitchAPI and python-twitch-client but could not utilize them since they did not have Python 3.6 support for the PubSub API.

## Challenges we ran into
Unfortunately, it was not possible to develop for the channel, outside of direct help from an affiliated broadcaster, since there no testing mechanism was made available for hackathon participants.  For example, icantiemyshoe would receive the following when trying to develop locally since he was not able to post channel points with his broadcaster account.

```sh
req = requests.post(url, headers=headers, data=body)
# {'error': 'Forbidden', 'status': 403, 'message': 'channel points are not available for the broadcaster'}
```

This made development difficult, because we didn't want any development errors to hurt his brand by "pushing straight to prod".


The biggest challenge was to decide the workflow for how points were redeemed while on host devices. The two major user stories we were trying to decide between was:

* Should the rewards be auto-redeemed via the PubSub or time query of the API
* Should the integration allow for the streamer to decide when or if they accept the change in the game play

While it would be better to allow for the streamer to give a verbal shoutout for point redemptions, making sure that the points are redeemed for the most entertainment value is paramount. Obviously, the entertainment value is increased if the streamer has to adapt to the redemption of rewards on-the-fly, so that was the route we chose.

While we did not chose the latter, we understand that there are times when manual redemption control is preferred.  For example, if there is a long travel time between tasks or missions, you obviously would want the subscribers to get the most chaos they could by redeeming it when the streamer gets into a more opportune position. Conversely, the streamer may be ending the stream after getting to a certain spot when the reward is redeemed, and the fan would not get the full value of the time for the chaos. It would be best to just refund the points or leave the rewards unredeemed to remain in the queue for the next stream.

UPDATE: After user testing, we discovered that Twitch does not currently allow for rewards to be manually accepted by the streamer, before actually performing the reward functionality.

However, there isn't a really good reward integration inside of OBS so we had to make it work as best as possible so it could be usable for Sinfathisar, and produce a working demo for the event.

## Accomplishments that we're proud of
We are proud of being able to coordinate the development effort in only our spare time, across different continents and time zones.

We are also pretty proud of the quality and content of the demo video.

This was also the first time that icantiemyshoe used a SWIG wrapper for Python. So, the fact that we were able to sync the device operations with what was reflected on the stream, provided a unique learning experience. This really made icantiemyshoe think more about how to integrate online performances with IOT devices and real-world events. 


FIX OR REMOVE

Another challenge that turned into an accomplishment that we can be proud of; was working with OBS's API's, which 

FIX OR REMOVE

## What we learned
We discovered that since icantiemyshoe's developer account was not at the Twitch affiliate level, he (and the other developers) were not able to test locally with the point redemptions and had to schedule time with our only available affiliate account (Sinfathisar19) to perform testing of our channel integrations. Obviously, it significantly slowed down development, having to align all of our schedules.

## What's next for Flips and Total Chaos
We have the following as stretch goals and may explore these in the future.
1. Help your friends make your streamer's experience far more challenging!  Work together to block streamer's abilities. But, this comes with a cost - it's a gamble for your points every time! 
2. Have a stream of chaos where all redemption costs and cooldowns are reduced. Your subscribers will go wild making you lose your mind.
3. Control your streamer's lighting on their keyboard, their nanoleaf array, or other RGB lighting setup. Create a Raspberry Pi companion that controls devices that in the subscriber's field of view. Rewards can be used with the device to change the lighting, music (speed, volume, etc.), or any kind of animatronics that we may make to mess with Sinfathisar. 
4. Visualizations for performers and non-game streamers: It would be fun to allow for a Bonaroo-like experience where the video stream can have the color, orientation, or filters be controlled by redeeming rewards. For example, subscribers could cause the screen to have a Kaleidoscope effect, or adjust the color scheme, to enhance the viewing experience of the subscriber. This will allow the performer to keep streaming, but allows the subscribers to participate in a unique experience. 

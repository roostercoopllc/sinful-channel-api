#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import time

async def hello():
    uri = "ws://localhost:8765"
    while True:
        async with websockets.connect(uri) as websocket:
            await asyncio.sleep(5)
            await websocket.send('Testing')
            print(f"> {'Testing'}")
            greeting = await websocket.recv()
            print(f"< {greeting}")

async def twitch_hello():
    uri = "ws://localhost:8765"
    while True:
        async with websockets.connect(uri) as websocket:
            await asyncio.sleep(7)
            await websocket.send('Twitch')
            print(f"> {'Testing'}")
            greeting = await websocket.recv()
            print(f"< {greeting}")

async def twitch_ping():
    uri = "wss://pubsub-edge.twitch.tv"
    async with websockets.connect(uri) as websocket:
        pong_waiter = await websocket.ping()
        print("> ping")
        await pong_waiter # greeting = await websocket.recv()
        print(f"< pong")
        
# asyncio.get_event_loop().run_until_complete(hello())
loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(hello())
    asyncio.ensure_future(twitch_hello())
    loop.run_forever()
except KeyboardInterrupt:
    print('Keyboard thing')
finally:
    print("Closing Loop")
    loop.close()
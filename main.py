from spotify import get_spotify, get_now_playing_info, get_playing_name, get_playing_url
import discord
from discord.ext import tasks
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open('config.yml', 'r') as f:
    config = load(f.read(), Loader=Loader)

client = discord.Client()
lock = True
spotify = get_spotify(config)
last_playing_name = ''


@tasks.loop(seconds=5)
async def check_spotify():
    global lock
    global last_playing_name
    if lock:
        lock = False
        raw_playing_data = await get_now_playing_info(spotify)
        if raw_playing_data:
            playing_name = get_playing_name(raw_playing_data)
            if not last_playing_name or last_playing_name != playing_name:
                last_playing_name = playing_name
                channel = client.get_channel(815076312611291196)
                await channel.send(f'{playing_name}\n{get_playing_url(raw_playing_data)}')
        lock = True


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    check_spotify.start()


client.run(config['discord_bot_token'])

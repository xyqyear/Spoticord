from spotify import get_spotify, get_now_playing_info, parse_playing_name, get_playing_url
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
            playing_name = parse_playing_name(raw_playing_data)
            if playing_name and (not last_playing_name or last_playing_name != playing_name):
                last_playing_name = playing_name
                channel = client.get_channel(config['channel_id'])
                print(f'[Debug] Playing: {playing_name}')
                await channel.send(f'{playing_name}\n{get_playing_url(raw_playing_data)}')
                print(f'[Debug] Discord message sent.')
        lock = True


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    check_spotify.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == 815076312611291196:
        if message.content == '!debug':
            debug_message = f'lock={lock}, last_playing_name={last_playing_name}'
            print(debug_message)
            await message.channel.send(debug_message)
        elif message.content == '!trigger':
            raw_playing = spotify.currently_playing()
            print(raw_playing)
        elif message.content.startswith('!say '):
            await message.channel.send(message.content[5:])


client.run(config['discord_bot_token'])

from discord.ext import commands
import discord

from codecs import open
import yaml

from os import listdir
import locale
from time import time

locale.setlocale(locale.LC_ALL, '')

with open('config.yaml', 'r', encoding='utf8') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(config['bot']['prefix']), case_insensitive=True)

        self.prefix = config['bot']['prefix']
        self.presence = config['bot']['presence']
        self.presence_activity = config['bot']['presence_activity']
        self.api_keys = config.get('api', {})
        self.emoji = config.get('emoji', {})
        self.misc = config.get('misc', {})
        self.database = config['database']


bot = Bot()

activities = {
    'playing': 0,
    'listening': 2,
    'watching': 3
}
if bot.presence_activity.lower() in activities:
    activity_type = activities[bot.presence_activity]
else:
    activity_type = 0


@bot.event
async def on_ready():
    if not hasattr(bot, 'uptime'):
        bot.uptime = time()

    for file in listdir('cogs'):
        if file.endswith('.py'):
            name = file[:-3]
            bot.load_extension(f'cogs.{name}')

    print(f'\nBrukernavn:      {bot.user.name}')
    print(f'ID:              {bot.user.id}')
    print(f'Version:         {discord.__version__}')
    print('...............................................................\n')
    await bot.change_presence(activity=discord.Activity(type=activity_type, name=bot.presence),
                              status=discord.Status.online)


bot.run(config['bot']['token'], bot=True, reconnect=True)

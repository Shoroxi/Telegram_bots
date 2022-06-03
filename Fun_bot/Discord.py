import time

import aiohttp
import discord
import telebot
from discord.ext import commands

import loadconfig

tg = telebot.TeleBot(loadconfig.__telegramtoken__)
tg_group_id = loadconfig.__tg_group_id__
my_id = loadconfig.__my_id__

# -----------------------------------------------------------------------
# -------------------------------DISCORD---------------------------------
# -----------------------------------------------------------------------
__version__ = '1.3.1'
description = ''' бот, разработанный с discord.py\n'''
dbot = commands.Bot(command_prefix="~", description=description)

@dbot.event
async def on_ready():
    if dbot.user.id == 290560071803600898:
        dbot.dev = True
    else:
        dbot.dev = False

    # for guild in dbot.guilds:
    #     for role in guild.roles:
    #         print(guild.name, role.id, role.name)

    print('Logged in as')
    print(f'Bot-Name: {dbot.user.name}')
    print(f'Bot-ID: {dbot.user.id}')
    print(f'Dev Mode: {dbot.dev}')
    print(f'Discord Version: {discord.__version__}')
    print(f'Bot Version: {__version__}')
    dbot.AppInfo = await dbot.application_info()
    print(f'Owner: {dbot.AppInfo.owner}')
    print('------')
    dbot.startTime = time.time()
    dbot.botVersion = __version__

@dbot.event
async def on_message(message):
    # сообщение бота
    if message.author.tg:
        return
    # сообщение в личку
    if isinstance(message.channel, discord.DMChannel):
        await message.author.send(':x: Извините, но я не принимаю команды через прямые сообщения! Пожалуйста, '
                                  'используйте меня в канале `#флуд-ботинкам`!')
        return
    if dbot.dev and not await dbot.is_owner(message.author):
        return
    # пинг бота
    if dbot.user.mentioned_in(message) and message.mention_everyone is False:
        if 'help' in message.content.lower():
            await message.channel.send('Полный список всех команд здесь: ')
        else:
            await message.add_reaction('👀') # :eyes:
    # -----------------------------------------------------------------------
    # TELEGRAM
    if message.attachments in loadconfig.__discord_channels__:
        attachers = ""
        for attachment in message.attachments:
            attachers += f"{attachment} "
        print(f'{message.content} {attachers}')
        to_tg = f"Сообщение: {message.content} \nИз: {message.channel.name} \nОт: {message.author.name}"
        tg.send_photo(tg_group_id, photo=f'{attachers}', caption=to_tg)
    else:
        print(f"{message.content}")
        to_tg = f"Сообщение: {message.content} \nИз: {message.channel.name} \nОт: {message.author.name}"
        tg.send_message(tg_group_id, text=to_tg)

    await dbot.process_commands(message)

@commands.command(aliases=['пинг'], hidden=False)
async def ping(self, ctx):
    """ Pong! """
    before = time.monotonic()
    before_ws = int(round(self.dbot.latency * 1000, 1))
    message = await ctx.send("🏓 Pong")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

@commands.command(aliases=['кот'])
async def cat(self, ctx):
        """ Рандомный кот """
        async with aiohttp.ClientSession() as session:
            async with session.get('http://aws.random.cat/meow') as r:
                # 200 -> everything fine.
                if r.status == 200:
                    content = await r.json()
                    vid = content['file'].replace('\ ', ' ')
                    embed = discord.Embed(title='Держи котейку')
                    embed.set_image(url=vid)
                    await ctx.send(embed=embed)
            await session.close()

@commands.command(aliases=['собака'])
async def dog(self, ctx):
        """ Рандомная собака """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://random.dog/woof") as r:
                if r.status == 200:
                    dog_link = await r.text()
                    vid = "https://random.dog/" + dog_link
                    embed = discord.Embed(title='Держи собачку')
                    embed.set_image(url=vid)
                    await ctx.send(embed=embed)
        await session.close()


if __name__ == '__main__':
    dbot.run(loadconfig.__discordtoken__)

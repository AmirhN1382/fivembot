import os
## pip install discord.py
import discord
import asyncio
import time
## pip install requests
import requests as rq
from discord.ext import commands
from discord.ext import tasks

## Setup
client = commands.Bot(command_prefix=['^'])
client.remove_command('help')

## Config
class config:
    serverIP = "" #IP:PORT | Example: 87.98.246.41:30120
    guildID = 0 #Your Discord Server ID, must be int. | Example: 721939142455459902
    Token = "" #Your Discord Bot Token

## Events
@client.event
async def on_ready():
    print('Bot Is Ready!')
    print('IF you have any problems, add me in discord, i will help you.!')
    print('AmirhN#1337')
    client.my_current_task = live_status.start()

## Players Count Function // Callable Everywhere, returns number
def pc():
    try:
        resp = rq.get('http://'+config.serverIP+'/players.json').json()
        return(len(resp))
    except:
        return('N/A')

## Say Commands
@client.command(pass_content=True, aliases=['s'])
@commands.has_permissions(administrator=True) 
async def say(ctx, *, text):
    
    try:
        await ctx.message.delete()
        timenow = time.strftime("%H:%M")
        embed=discord.Embed(title="FiveMBot City Bot", description=" ", color=0xfff705)
        embed.set_author(name="FiveMBot", url="http://mastercity.ir/", icon_url="https://cdn.discordapp.com/attachments/624670013793763330/809442452695547984/unknown.png")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Message:", value=text, inline=False)
        embed.set_footer(text=f"{ctx.message.author} | FiveM Bot | {timenow}")
        await ctx.send(embed=embed)
    except Exception as err:
        print(err)
    
@client.command(pass_context=True, aliases=['hs'])
@commands.has_permissions(administrator=True) 
async def hsay(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

## Players Lookup
@client.command(aliases=['playerid', 'loid', 'server'])
@commands.has_permissions(administrator=True) 
async def pid(ctx, pids):
    
    if not pid:
        await ctx.send('<@{}>, Please Specify A In-Game Player ID!')
        return
    resp = rq.get('http://'+config.serverIP+'/players.json')
    for _ in resp.json():
        if _['id'] == int(pids):
            pembed = discord.Embed(title='PlayerID Query Seccessful!', color=discord.Color.dark_green())
            pembed.add_field(name='Steam Name : {}\nIn-Game ID : {}'.format(_['name'], _['id']), value='Ping : {}'.format(_['ping']), inline=False)
            [pembed.add_field(name=args.split(':')[0].capitalize(), value=args.split(':')[1], inline=False) for args in _['identifiers']]

            await ctx.send(embed=pembed)
        else:
            pass

## DiscordID Lookup
@client.command(aliases=['discord', 'did', 'whois'])
@commands.has_permissions(administrator=True) 
async def discord_identifier(ctx, disid: int=None):
    
    if not disid:
        await ctx.send('<@{}>, Please Specify A DiscordID!'.format(ctx.message.author.id))
        return
    try:
        obj = await client.fetch_user(disid)
        if not obj:
            await ctx.send('User `{}` Not Found!'.format(disid))
        else:
            dembed = discord.Embed(title='DiscrdID Identifier Query Successful!', descrption='API Returted Values :', color=discord.Color.dark_gold())
            dembed.add_field(name='Discord Username :', value=obj)
            dembed.add_field(name='DiscordID :', value=obj.id)
            dembed.set_image(url=obj.avatar_url)
            await ctx.send(embed=dembed)
    except Exception as err:
        print(err)
    
## Server run
@client.command()
@commands.has_permissions(administrator=True) 
async def run(ctx):
    
    await ctx.message.delete()
    content = "~~@everyone~~"
    timenow = time.strftime("%H:%M")
    embed=discord.Embed(title="Server Run Shod", description="Server Run Shod Guys! Mitonid join shid =)", color=0xff1414)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/624670013793763330/809442452695547984/unknown.png")
    embed.add_field(name="✅ Paste this in f8 ✅", value=f"join {config.serverIP}", inline=False)
    embed.set_footer(text=f"{timenow}")
    await ctx.send(embed=embed, content=content)
    
## Help Command
@client.command()
@commands.has_permissions(administrator=True) 
async def help(ctx):
    
    embed=discord.Embed(title="FiveMBot Bot", description="FiveMBot Bot Commands List", color=0xfff700)
    embed.set_author(name="Welcome To FiveMBot", url="http://mastercity.ir/", icon_url="https://cdn.discordapp.com/attachments/624670013793763330/809442452695547984/unknown.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/624670013793763330/809442452695547984/unknown.png")
    embed.add_field(name="Prefix = ^", value="You Have to use ^ before every ^command :)", inline=False)
    embed.add_field(name="^players", value="Server Online Players List", inline=False)
    embed.add_field(name="^pid", value="LookUp PlayerID From Online Players List", inline=False)
    embed.add_field(name="^whois", value="Lookup Discord ID", inline=False)
    embed.add_field(name="^say", value="Say Something as BOT in Embed Message with your name", inline=False)
    embed.add_field(name="^hsay", value="Say Something as BOT [Hidden Mode]", inline=False)
    embed.add_field(name="^run", value="Server run shod Embed", inline=False)
    embed.set_footer(text="Made With 💖 by AmirhN#1337")
    await ctx.send(embed=embed)
    
## Players Command
@client.command()
@commands.has_permissions(administrator=True) 
async def players(ctx):
    
    timenow = time.strftime("%H:%M")
    resp = rq.get('http://'+config.serverIP+'/players.json').json()
    total_players = len(resp)
    if len(resp) > 25:
        for i in range(round(len(resp) / 25)):
            embed = discord.Embed(title='FiveMBot Bot', description='Server Players', color=discord.Color.blurple())
            embed.set_footer(text=f'Total Players : {total_players} | FiveMBot | {timenow}')
            count = 0
            for player in resp:
                embed.add_field(name=player['name'], value='ID : ' + str(player['id']))
                resp.remove(player)
                count += 1
                if count == 25:
                    break
                else:
                    continue

            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='FiveMBot Bot', description='Server Players', color=discord.Color.blurple())
        embed.set_footer(text=f'Total Players : {total_players} | FiveMBot | {timenow}')
        for player in resp:
            embed.add_field(name=player['name'], value='ID : ' + str(player['id']))
        await ctx.send(embed=embed)
    
## Live Status
@tasks.loop()
async def live_status(seconds=75):
    pcount = pc()
    Dis = client.get_guild(config.guildID) #Int

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'🐌 {pcount}')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'👥 {Dis.member_count}')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'AmirhN#1337')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'Anything U want')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'Anything U want')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)


client.run(config.Token)
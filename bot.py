import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from googletrans import Translator
import os

bot = commands.Bot(command_prefix='?t')
bot.remove_command('help')

"""ready message"""
@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='?tphelp/?tdhelp'))
    print('Translator v1.0 --')
    print('Successfully joined account: ' + bot.user.name)

"""server join message"""
@bot.event
async def on_server_join(server):
    f_message=0
    for channel in server.channels:
        if str(channel.permissions_for(server.me).send_messages) == "True" and str(channel.type)=="text" and f_message==0:
            embed = discord.Embed(title="I, the translator bot, have arrived", description="?tphelp for public message \n?tdhelp for direct message \n\n ----creator: willisburg#6234----")
            await bot.send_message(channel, embed=embed)
            f_message=1;

"""translating"""            
@bot.command(pass_context=True)
async def r(ctx, *arg):
    try:
        await bot.delete_message(ctx.message)
    except:
        a=0
        
    try:
        text = str(' '.join(arg))
    except:
        text = str(' '.join(arg)).encode("utf-8")
        
    translator = Translator()
    src=""
    dest=""
    text+=" "
    if(text.find('s-')!=-1):
        src=text[text.find('s-')+2:text.find(' ', text.find('s-'))]
        text=text.replace("s-"+src, "")
    if(text.find('d-')!=-1):
        dest=text[text.find('d-')+2:text.find(' ', text.find('d-'))]
        text=text.replace("d-"+dest, "")
    
    if dest=="" and src=="":
        startext=str(translator.translate(text))
    elif src=="":
        startext=str(translator.translate(text, dest=dest))
    elif dest=="":
        startext=str(translator.translate(text, src=src))
    else:
        startext=str(translator.translate(text, dest=dest, src=src))
        
    text=startext[startext.find("text=")+5:startext.find(", pronunciation=")]
    
    if(text.find("<@")!=-1 and text.find(">")!=-1):
        text=text.replace("<@ ", "<@!")
        
    embed=discord.Embed(title="", description=text)
    await bot.send_message(ctx.message.channel, "<@!"+str(ctx.message.author.id)+">: "+text)

"""public help message"""    
@bot.command(pass_context=True)
async def phelp(ctx):
    await bot.send_message(ctx.message.channel, "```[] ?tr 'text' s-'source language tag' d-'destination language tag' \n -translates a message \n -if source language tag is not provided it will be assigned automatically \n -if destination language tag is not provided it's automatically set as english(en) \n *do not use the apostrophe(') \n[] ?tinvite \n -sends a message to the message author with the auth to bot```")

"""direct help message"""
@bot.command(pass_context=True)
async def dhelp(ctx):
    await bot.send_message(ctx.message.author, "```[] ?tr 'text' s-'source language tag' d-'destination language tag' \n -translates a message \n -if source language tag is not provided it will be assigned automatically \n -if destination language tag is not provided it's automatically set as english(en) \n *do not use the apostrophe(') \n[] ?tinvite \n -sends a message to the message author with the auth to bot```")

"""invite to server"""
@bot.command(pass_context=True)
async def invite(ctx):
    await bot.send_message(ctx.message.author, "https://discordapp.com/oauth2/authorize?client_id=460891148668502026&permissions=8192&scope=bot")
    
bot.run(str(os.environ.get('BOT_TOKEN')))

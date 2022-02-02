from asyncio import events
import asyncio , sys , subprocess
from os import name
import discord
from discord import mentions
from discord import message
from discord.abc import User
from discord.ext import commands , tasks
from discord.ext.commands.bot import Bot
from discord.utils import get
from random import choice
from discord.voice_client import VoiceClient
import youtube_dl
import datetime
import requests
import time
import os


clinet = commands.Bot(command_prefix='dl.')

@clinet.event
async def on_ready():
    print('bot is online')

@clinet.command(name='-s' , help='get download link (spotify)')
async def spotify(ctx,name):
  link = requests.get(f'https://api.otherapi.tk/music?platform=spotify&type=search&query='+name).json()
  if name== '-h' :
    await ctx.send('database has all spotify musics')
    await ctx.send('`usage : ?dl-s songname`')
  else:

    try:
      await ctx.send('Your download link is ready ! '+'`'+link['music'][0]['download']+'`')
      await ctx.send('Artist :'+'`'+link['music'][0]['artist']+'`')
    except:
      if link['music'] == None or '':
        await ctx.send('something went wrong/song name may be wrong(enter song name exactly)')
      

@clinet.command(name='-y',help='get music file on discord (youtube)')
async def dlyu(ctx,*args):
  sentence=''
  for arg in args:
    sentence  +=arg+' '
    
  ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{sentence}.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',

    }],
} 
  
  result = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?q={sentence}&maxResults=1&key=AIzaSyAOw0wToDhyqx693bhLEkIk2TY4g8ec4n8').json()
  data = result
  data = data['items'][0]['id']['videoId']
  url = f'https://youtube.com/watch?v={data}'
  await ctx.send(url+' Is downloading ! please wait')
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
    await ctx.send('successfully downloaded')
    while True:
      try:
        await ctx.send(file=discord.File(f'./{sentence}.mp3'))
        time.sleep(4)
        os.remove(f'./{sentence}.mp3')
        break
      except:
        if os.path.getsize(f'./{sentence}.mp3') > 8000000:
          await ctx.send('File is Bigger than 8MB ')
          os.remove(f'./{sentence}.mp3')
          break
        else:
          pass



@clinet.command(name='search',help='search in youtube')
async def search(ctx , name=None,*,kind='music'):
  try:
    if name != None:
      result = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?q={name}&maxResults=1&type={kind}&key=AIzaSyAOw0wToDhyqx693bhLEkIk2TY4g8ec4n8').json()
      data = result['items']
      data = data[0]["id"]["videoId"]
      url = f'https://youtube.com/watch?v={data}'
      await ctx.send(f"""
      result : 
      {url}
      """)
    else:
      await ctx.send('`usage :>> ?search <name> <type=None>`')
  except:
    await ctx.send('something went wrong')

my_token = ''
clinet.run(my_token)

#creator instagram >> alimoio0

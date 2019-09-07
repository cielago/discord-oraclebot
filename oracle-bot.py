import sys
import json
import discord
import requests
import logging
from fuzzywuzzy import process

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='l5r-bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()
clientid = '619715320709382145'
clientsecret = ''
token = ''

#query = sys.argv[1]
url = 'https://api.oracleofthevoid.com/search'
imgurlbase = 'https://s3.us-east-2.amazonaws.com/oracle-l5r/'


def doSearch(inq):        
    query = inq
    qa = { "table": 'l5r',"querystring": query }
    r = requests.post(url,qa)
    n = []
    rd = {}
    for each in r.json()['hits']['hits']:
        n.append(str(each['_source']['formattedtitle']))
        rd[str(each['_source']['formattedtitle'])] = each
    match = process.extractOne(query,n)
    imagehash = str(rd[match[0]]['_source']['imagehash'])
    cardid = str(rd[match[0]]['_source']['cardid'])
    return imgurlbase+imagehash+"/printing_"+cardid+"_1_details.jpg"

@client.event
async def on_ready():
    logger.info('Logged in as')
    logger.info(client.user.name)
    logger.info(client.user.id)
    logger.info('------')

@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        help_text = "!oracle <cardname> looks up cards on https://preview.oracleofthevoid.com \n \n" +\
                    "Search as close to the full title of the card (ie Daigotsu Experience 3) as possible"
        await message.channel.send(help_text)
    if message.content.lower().startswith('!oracle'):
        command = message.content.split(' ')[1:]
        c2 = ' '.join(command)
        if len(command) < 1:
            await message.channel.send("I can look Old5r cards up for you, honourable samurai-san.")
        else:
            await message.channel.send(doSearch(c2))

client.run(token)

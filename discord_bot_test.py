# discord_bot_test.py

import discord
import os
import logging
import re
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import time
import hashlib
import struct
import json

client = discord.Client()

################################################################################
# set up the databases

# {'account_name': 'Gates Divorce', 'id_key': 'rngteger'}
db1 = TinyDB('databases/db1.json')
db1.truncate()

# { 'account_name': 'Gates Divorce',
#   'beneficiary': 'Bill Gates'
# }
db2 = TinyDB('databases/db2.json')
db2.truncate()

# { 'account_name': 'Gates Divorce',
#   'condition_name': 'doc1',
#   'beneficiary': 'Bill Gates'
#   'amount': 100
# }
db3 = TinyDB('databases/db3.json')
db3.truncate()

user_query = Query()

################################################################################
# support functions

# create new account id
def create_new_account_id ():
    m = hashlib.sha256()
    hash_string = int(time.time())
    hash_string = struct.pack(">i", hash_string)
    m.update(hash_string)
    return str(m.digest())


# add new account to # DEBUG:
def add_new_account(account_name):
    new_account_id = create_new_account_id()
    logging.warning(type(new_account_id))
    logging.warning(type(account_name))
    line_entry = {'account_name': str(account_name),'id_key': new_account_id}
    db1.insert(line_entry)
    # add the Trust as first beneficiary_name
    line_entry = {'account_name': str(account_name), 'beneficiary': "Trust Account"}
    db2.insert(line_entry)


# add new beneficiary to one account
def add_new_beneficiary(beneficiary_name, account_name):
    line_entry = {'account_name': str(account_name), 'beneficiary': str(beneficiary_name)}
    db2.insert(line_entry)


# add new condition for an account, only supports one beneficiary
def add_new_conditions(account_name, condition, beneficiary, amount):
    line_entry =  { 'account_name': account_name,
                    'condition': condition,
                    'beneficiary': beneficiary,
                    'amount': amount}
    db3.insert(line_entry)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    read_text = message.content
    logging.warning("Message content: {}".format(read_text))
    logging.warning(re.findall(r'"(.*?)"',message.content))


################################################################################
    if message.content.startswith('$help'):
        await message.channel.send('Hello!')
        await message.channel.send('These are the actions available to you')
        await message.channel.send('create trust account <account name>')
        await message.channel.send('show active accounts')
        await message.channel.send('add condition <condition> to <account name> for <beneficiary> for <dollars>')
        await message.channel.send('show rules for <account name>')
        await message.channel.send('add beneficiary <beneficiary name> to <account name>')
        await message.channel.send('show beneficiary for <account name>')
        await message.channel.send('clear condition <condition> for <account name>')
        await message.channel.send('settle trust account <account name>')
        await message.channel.send('show blockchain for account <account name>')


################################################################################
    if message.content.startswith('create trust account'):
        account_name = str(re.findall(r'"(.*?)"',read_text))
        # create database entry for new account
        add_new_account(account_name)
        # show new db entry
        new_account = db1.search(user_query.account_name == account_name)
        logging.warning(new_account)

        await message.channel.send('Initiating private blockchain')
        await message.channel.send('=============================')


################################################################################
    if message.content.startswith('show active accounts'):
        await message.channel.send('These are the active accounts')
        active_accounts = db1.all()
        if active_accounts == []:
            await message.channel.send("No active accounts")
        else:
            for item in active_accounts:
                ostr = "Account name: " + item['account_name']
                await message.channel.send(ostr)
                ostr = "ID: " + item['id_key']
                await message.channel.send(ostr)


################################################################################
    if message.content.startswith('show beneficiary '):

        # pull parameters from command line
        parameters = re.findall('"([^"]*)"', read_text)
        logging.warning(parameters)
        account_name = parameters[0]

        ostr = "Beneficiaries for" + parameters[0]
        await message.channel.send(ostr)
        active_bennies = db2.all()
        if active_bennies == []:
            await message.channel.send("No active beneficiaries")
        else:
            for item in active_bennies:
                bennies = db2.search(user_query.account_name == [account_name])
                ostr = "Beneficiary name: " + item['beneficiary']
                await message.channel.send(ostr)


################################################################################
    if message.content.startswith('add condition'):

        # pull parameters from command line
        parameters = re.findall('"([^"]*)"', read_text)
        logging.warning(parameters)

        await message.channel.send('Adding condition to...')


################################################################################
    if message.content.startswith('show conditions for'):
        await message.channel.send('Showing conditions for...')


################################################################################
    if message.content.startswith('add beneficiary'):
        parameters = re.findall('"([^"]*)"', read_text)
        logging.warning(parameters)
        add_new_beneficiary(parameters[0], parameters[1])
        ostr = "Adding beneficiary" + parameters[0] + " to " + parameters[1]
        await message.channel.send(ostr)

    if message.content.startswith('clear condition'):
        await message.channel.send('Clearing condition')
        await message.channel.send('Updating blockchain')

    if message.content.startswith('settle account'):
        await message.channel.send('Settling account')


client.run("ODQ1NDA0MzIyMDE1MzQ2Njg5.YKgeIQ.4jaOIRUHZfCvg7KsqlX07uchL0U")

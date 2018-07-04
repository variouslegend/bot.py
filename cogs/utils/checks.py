import discord
from discord.ext import commands
from . import Pyson

def is_owner():
    def predicate(ctx):
        author=ctx.message.author
        if author is ctx.message.server.owner:
            return True
    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        author=ctx.message.author
        if author is ctx.message.server.owner:
            return True
        if ('administrator',True) in author.server_permissions:
            return True
    return commands.check(predicate)

def is_coowner():
    'Checks if the message author is a co-owner of the server'
    def predicate(ctx):
        coowners = Pyson('cogs/data/config').data.get('coowners', [])
        author = ctx.message.author.id
        owner = ctx.message.server.owner.id
        if author in coowners or author == owner:
            return True
        return False
    return commands.check(predicate)
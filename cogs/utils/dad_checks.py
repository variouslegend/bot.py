import discord
from discord.ext import commands

dev=['Bot Dev']
mod=['Mods']+dev
tier3=['Blubber Buddies']+mod+dev
tier2=['Chubby Chaps']+tier3+mod+dev
tier1=['Seal Pups']+tier2+tier3+mod+dev


def is_tier_1():
    def predicate(ctx):
        author=ctx.message.author
        if author is ctx.message.server.owner:
            return True
        elif any(role.name in tier1 for role in author.roles):
            return True
        return False
    return commands.check(predicate)


def is_tier_2():
    def predicate(ctx):
        author=ctx.message.author
        if author is ctx.message.server.owner:
            return True
        elif any(role.name in tier2 for role in author.roles):
            return True
        return False
    return commands.check(predicate)

def is_tier_3():
    def predicate(ctx):
        author=ctx.message.author

        if author is ctx.message.server.owner:
            return True
        elif any(role.name in tier3 for role in author.roles):
            return True
        return False
    return commands.check(predicate)

def is_mod():
    def predicate(ctx):
        author=ctx.message.author

        if author is ctx.message.server.owner:
            return True
        elif any(role.name in mod for role in author.roles):
            return True
        return False
    return commands.check(predicate)

def is_dev():
    def predicate(ctx):
        author=ctx.message.author
        if author is ctx.message.server.owner:
            return True
        elif any(role.name in dev for role in author.roles):
            return True
        return False
    return commands.check(predicate)
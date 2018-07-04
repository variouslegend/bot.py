import random
import asyncio
import string
import discord
from discord.ext import commands
from .utils import Pyson, checks


class Subscribers:

    def __init__(self, bot):
        self.bot = bot
        self.keys = Pyson('cogs/data/keys', {'claimed': {}})

    @checks.is_admin()
    @commands.command()
    async def create(self, role: discord.Role = None):
        ': Create a key and a role to be assigend to a new subscriber'
        if role:
            key = None
            while not key:
                key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))
                if key in self.keys.data:
                    key = None
            self.keys.data[key] = role.id
            self.keys.save()
            await self.bot.whisper(f'Key: **{key}**\nRole: **{role.name}**')

    @commands.command(pass_context=True, aliases=['make'])
    async def claim(self, ctx, key: str = None):
        ': Claim your key to get your role'
        server = ctx.message.server
        author = ctx.message.author
        role = discord.utils.get(server.roles, id=self.keys.data.get(key))
        if not role:
            await self.bot.delete_message(ctx.message)
            await self.bot.say('```You have entered and invalid key.\nIf you think this is a mistake, please talk to one of our admins.```')
        else:
            await self.bot.delete_message(ctx.message)
            await self.bot.add_roles(author, role)
            await self.bot.reply(f' you have been assigned the role of {role.mention}! Thank you for your subscription!')
            del self.keys.data[key]
            if role.id not in self.keys.data['claimed']:
                self.keys.data['claimed'][role.id] = 0
            self.keys.data['claimed'][role.id] += 1
            self.keys.save()

    @checks.is_admin()
    @commands.command(pass_context=True, name='claimed')
    async def _claimed(self, ctx):
        ': Check claimed keys'
        server = ctx.message.server
        claimed = self.keys.data.get('claimed')
        msg = ''
        for role, amount in claimed.items():
            role = discord.utils.get(server.roles, id=role)
            msg += f'{role.mention} claimed keys: {amount}\n'
        if not msg:
            msg = 'No keys have been claimed'
        await self.bot.say(msg)

    @checks.is_admin()
    @commands.command(pass_context=True, name='move')
    async def _move(self, ctx, old_role: discord.Role = None, new_role: discord.Role = None):
        ': Move members with one role to another role'
        if old_role and new_role:
            server = ctx.message.server
            for member in server.members:
                if old_role in member.roles:
                    await self.bot.remove_roles(member, old_role)
                    await asyncio.sleep(.2)
                    await self.bot.add_roles(member, new_role)


def setup(bot):
    bot.add_cog(Subscribers(bot))

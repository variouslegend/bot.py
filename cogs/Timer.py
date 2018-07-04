import asyncio
import random
from datetime import datetime
import discord
from discord.ext import commands
from .utils import Pyson, checks


class Timer():

    def __init__(self, bot):
        self.bot = bot
        self.timers = Pyson('./cogs/data/timers', [])
        self.status = None
        self.coro_timers = {}
        self.bot.loop.create_task(self.load_timers())

    async def send_help(self, ctx):
        ctx.message.content = f'{ctx.prefix}help {ctx.invoked_with}'
        await self.bot.say('Invalid format')
        await self.bot.process_commands(ctx.message)

    async def on_ready(self):
        for server in self.bot.servers:
            self.raffle_channel = discord.utils.get(server.channels, name='raffles')
            if not self.raffle_channel:
                self.raffle_channel = await self.bot.create_channel(server, 'raffles')

    def time_format(self, time_string):
        try:
            date = datetime.strptime(time_string, '%Y-%m-%d %H:%M')
            return date
        except:
            return

    def time_convert(self, time, no_sec=False):
        time = int(time)
        mins, secs = divmod(time, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:01d}h {:02d}m {:02d}s'.format(hours, mins, secs)
        if no_sec == True:
            timeformat = '{:01d}h {:02d}m'.format(hours, mins)
        return timeformat

    def remove_timer(self, name):
        for timer in self.timers.data:
            if name == timer.get('name'):
                self.timers.data.remove(timer)
                self.timers.save()
        if name in self.coro_timers:
            try:
                self.coro_timers[name].cancel()
            except:
                pass
            del self.coro_timers[name]

    async def _timer(self, time, name):
        await self.bot.wait_until_ready()
        time = self.time_format(time)
        if not self.status:
            self.status = self.bot.loop.create_task(self.status_update())
        sleep = (time-datetime.utcnow()).total_seconds()
        if sleep > 0:
            await asyncio.sleep(sleep)
        self.remove_timer(name)
        await self.bot.send_message(self.raffle_channel, f'@everyone {name} starts now! Winners will be announced in the next 5 minutes')

    async def status_update(self):
        while len(self.timers.data) > 0:
            for timer in self.timers.data:
                endtime = timer.get('endtime')
                name = timer.get('name')
                endtime = self.time_format(endtime)
                time_left = (endtime-datetime.utcnow()).total_seconds()
                time_left = self.time_convert(time_left)
                await self.bot.change_presence(game=discord.Game(name=f'{name} - {time_left}'))
                await asyncio.sleep(10)
        self.status = None
        await self.bot.change_presence(game=None)

    async def load_timers(self):
        for timer in self.timers.data:
            endtime = timer.get('endtime')
            name = timer.get('name')
            coro = self.bot.loop.create_task(self._timer(endtime, name))
            self.coro_timers[name] = coro

    @checks.is_admin()
    @commands.command(pass_context=True)
    async def add_timer(self, ctx, date_time: str=None, name: str=None):
        '''
        : Add a timer
        Usage: add_timer "YYYY-MM-DD hh:mm" "timer name" (optional)
        Quotes are needed for time and timer names with more than one word
        '''
        if name:
            name = name.title()
        if not self.time_format(date_time):
            await self.bot.say(f'Incorrect time format! Format is military UTC:\nCurrent time: {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}')
            await self.send_help(ctx)
            return
        if any(timer.get('name') == name for timer in self.timers.data):
            await self.bot.say(f'**{name}** is already a timer')
            return
        while not name:
            name = f'Timer-{random.choice(range(0,10000))}'
            if name in self.timers.data:
                name = None
        coro = self.bot.loop.create_task(self._timer(date_time, name))
        self.coro_timers[name] = coro
        self.timers.data.append({
            'endtime': date_time,
            'name': name
        })
        self.timers.save()
        await self.bot.say(f'**{name}** has been added!')

    @checks.is_admin()
    @commands.command()
    async def cancel_timer(self, *, timer: str=None):
        ': Cancel a timer'
        timer = timer.title()
        if timer in self.coro_timers:
            self.remove_timer(timer)
            await self.bot.say(f'**{timer}** has been removed')

    @commands.command(name='timers')
    async def _timers(self):
        ': See a list of current timers'
        if not self.timers.data:
            await self.bot.say('No timers have been set!')
        else:
            now = datetime.utcnow()
            embed = discord.Embed(title='Timers')
            names = ''
            date_time = ''
            t_left = ''
            for timer in self.timers.data:
                names += timer.get('name')+'\n'
                endtime = self.time_format(timer.get('endtime'))
                time_left = (endtime-datetime.utcnow()).total_seconds()
                time_left = self.time_convert(time_left)
                date_time = timer.get('endtime')+'\n'
                t_left += time_left+'\n'
            if not names or not date_time:
                print(None)
                names = 'None'
                date_time = 'None'
            embed.add_field(name='Name', value=names)
            embed.add_field(name='Date and Time (UTC)', value=date_time)
            embed.add_field(name='Time Left', value=t_left)
            await self.bot.whisper(embed=embed)


def setup(bot):
    bot.add_cog(Timer(bot))

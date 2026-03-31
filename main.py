import discord, dotenv
from discord import app_commands
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from collections import defaultdict

from utils import get_uuid

dotenv.load_dotenv()

bot = discord.Client(intents=discord.Intents.all())
bot.tree = app_commands.CommandTree(bot, allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True), allowed_installs=app_commands.AppInstallContext(guild=True, dm_channel=True, private_channel=True))
scheduler = AsyncIOScheduler()
jobs = {}
last_gexp = defaultdict(lambda: -1)
AIDAN = 1364970345781526601

@bot.event
async def on_ready():
    global AIDAN
    AIDAN = await bot.fetch_user(AIDAN)
    print('BOT READY')


@bot.tree.command(name='track', description='Tracks changes in Hypixel user\'s Guild experience.')
async def track(interaction: discord.Interaction, user: str):
    from utils import notify
    await interaction.response.defer()
    uuid = await get_uuid(user)
    if uuid in jobs:
        await interaction.followup.send(f'User {user} already being tracked.')
        return

    jobs[user] = scheduler.add_job(notify, args=[uuid, user], trigger=CronTrigger(minute='*'))
    await interaction.followup.send(f'Now tracking {user}')

@bot.tree.command(name='untrack', description='Untracks changes in Hypixel user\'s Guild experience.')
async def untrack(interaction: discord.Interaction, user: str):
    if user not in jobs:
        await interaction.response.send_message(f'User {user} not currently being tracked.')
        return

    jobs[user].remove()
    del jobs[user]
    last_gexp[user] = -1
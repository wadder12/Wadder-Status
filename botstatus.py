import nextcord
from nextcord.ext import commands, tasks

intents = nextcord.Intents.default()
intents.members = True
import datetime


bot = commands.Bot(command_prefix='/', intents=nextcord.Intents.all())

main_bot_id =   # Replace with the ID of the main bot you want to monitor
status_channel_id =   # Replace with the ID of the channel you want to send status updates to
status_message_id = None
current_status = None
status_change_time = None

def log_status_change(new_status, duration=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("status_log.txt", "a") as log_file:
        if duration:
            log_file.write(f"{timestamp} - {new_status} (Duration: {duration})\n")
        else:
            log_file.write(f"{timestamp} - {new_status}\n")

@bot.event
async def on_ready():
    print(f"{bot.user} is now online.")
    check_bot_status.start()  # Start the loop to check bot status every minute

@tasks.loop(minutes=1)
async def check_bot_status():
    global status_message_id, current_status, status_change_time
    status_channel = bot.get_channel(status_channel_id)
    main_bot_member = None

    for guild in bot.guilds:
        main_bot_member = guild.get_member(main_bot_id)
        if main_bot_member:
            break

    new_status = ""
    embed_color = 0x000000
    emoji = ""

    if main_bot_member:
        if main_bot_member.status == nextcord.Status.offline:
            new_status = "Offline"
            embed_color = 0xFF0000
            emoji = "🔴"  # Red circle for offline
        else:
            new_status = "Online"
            embed_color = 0x00FF00
            emoji = "🟢"  # Green circle for online
    else:
        new_status = "Not Found"
        embed_color = 0xFFFF00
        emoji = "🟡"  # Yellow circle for not found

    if new_status != current_status:
        if status_change_time:
            duration = datetime.datetime.now() - status_change_time
            log_status_change(new_status, duration)
        else:
            log_status_change(new_status)

        status_change_time = datetime.datetime.now()
        current_status = new_status

        embed = nextcord.Embed(title=f"{emoji} Main Bot Status: {new_status}", color=embed_color)

        if status_message_id:
            status_message = await status_channel.fetch_message(status_message_id)
            await status_message.edit(embed=embed)
        else:
            status_message = await status_channel.send(embed=embed)
            status_message_id = status_message.id

bot.run("")  # Replace with your monitoring bot token
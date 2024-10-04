import logging
import discord
from dotenv import load_dotenv 
import os

load_dotenv('sensitive.env')

##discord server id your bot is in
dcid=os.getenv('DCID')
dguild= discord.Object(id=dcid)
dname="rise"
ddescription= "good ol test"
dtoken=os.getenv('DTOKEN')
print(dtoken)

#logging for debugging
logging.basicConfig(level=logging.INFO)


class cclient(discord.Client):
    def __init__(self):
        #setting up intents (what the bot has perms from discord API)

        intents= discord.Intents.default()

        intents.integrations= False
        intents.webhooks = False
        intents.invites= False
        intents.voice_states= False
        intents.presences=False
        intents.dm_messages=False

        
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=dguild)
            self.synced= True
        print(f"logged in as {self.user}")

client=cclient()
tree= discord.app_commands.CommandTree(client)

@tree.command(name=dname, description=ddescription,guild=dguild)
async def self (interact: discord.Interaction):
    await interact.response.send_message(f"I LIVE!!!!!")

client.run(dtoken)
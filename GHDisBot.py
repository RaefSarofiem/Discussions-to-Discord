import logging
import discord

##discord server id your bot is in
dcid=0
dguild= discord.Object(id=dcid)
dname="rise"
ddescription= "good ol test"
dtoken='token here'

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

        
        super().__init__(intents)
        self.synced = False

    async def on_ready(self):
        await self
        if not self.synced:
            await tree.sync(guild=dguild)
            self.synced= True
        print(f"logged in as {self.user}")

client=cclient()
tree= discord.app_commands.CommandTree(client)

@tree.command(name=dname, description=ddescription,guild=dguild)
async def self (interact: discord.Interaction, name: str):
    await interact.response.send_message(f"I LIVE!!!!!")

client.run(dtoken)
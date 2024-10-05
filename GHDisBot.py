import logging
import discord
from dotenv import load_dotenv 
import os

load_dotenv('sensitive.env')

##discord server id your bot is in
dcid=os.getenv('DCID')
dguild= discord.Object(id=dcid)
dname="launch_discussion"
ddescription= "start a private page to talk with a csa mentor"
dtoken=os.getenv('DTOKEN')


#ticket for creating a new channel, connecting text to discussions
class launchTicket(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label= "Ask a CSA Mentor", style=discord.ButtonStyle.green,custom_id="request-ticket" )
    #callback for checking button status
    async def ticket(self,interac: discord.Interaction, button: discord.ui.Button ):
        tick = discord.utils.get(interac.guild.text_channels, name=f"{interac.user.name}'s Ticket -- {interac.user.discriminator}")
        ## TODO: fix the multiple ticket issue (can just make as many tickets as you'd like with same name)
        if tick is not None: ##ticket is already created
            await interac.response.send_message(f"looks like you already have a discussion ticket open ({tick.mention}). If you want to make a" 
                                                "new discussion ticket, close the open one first. otherwise, continue using the open ticket"
                                                "to reply in the same discussion.", ephemeral = True)
        else:
            ## overwriting permissions for users to make a public channel
            ticket_overwrites = {
                #default role is @everyone
                interac.guild.default_role: discord.PermissionOverwrite(view_channel= False),
                interac.user: discord.PermissionOverwrite(view_channel= True, send_messages= True),
                #"me" is the bot
                interac.guild.me: discord.PermissionOverwrite(view_channel= True, send_messages=True, read_message_history= True)
            }
            #TODO: anti spam tool
            #TODO: button in room to end discussion (pop up menu with a command)
            
            channel = await interac.guild.create_text_channel(name=f"{interac.user.name}'s Ticket -- {interac.user.discriminator}",
            overwrites= ticket_overwrites, reason= (f"Ticket for {interac.user}") )
            await channel.send(f"{interac.user.mention} created a ticket")
            await interac.response.send_message((f"ticket made, you can go talk to CSA mentors at {channel.mention}"), ephemeral=True)


        
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
        self.added= False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=dguild)
            self.synced= True
        if not self.added:
            self.add_view(launchTicket())
            self.added=True
        print(f"logged in as {self.user}")

client=cclient()
tree= discord.app_commands.CommandTree(client)

@tree.command(name=dname, description=ddescription, guild=dguild)
async def   mentoring (interact: discord.Interaction):
    label= discord.Embed(title= "need to ask a CSA mentor a question? click the button to create a ticket!")
    await interact.channel.send (embed= label, view=launchTicket())
    await interact.response.send_message("Discussion launched", ephemeral= True)
    #await interact.response.send_message(f"I LIVE!!!!!")

client.run(dtoken)

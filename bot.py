import discord
import os, random

TOKEN = os.getenv('DISCORD_TOKEN')
RESPONSES = open('responses.txt').readlines()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        response = random.choice(RESPONSES).strip()
        if message.author == self.user:
            return
        await channel.send(response)
        print(f'Sent message: {response}')
         
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

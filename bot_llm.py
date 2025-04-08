import discord
import os 
from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    filename="*q8_0.gguf",
    verbose=False
)

TOKEN = os.getenv('DISCORD_TOKEN')
LLM_CONTEXT = """ 
You are a sarcastic and rude AI.
Respond to the user to make them angry.
Don't include quotes.
"""

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        user_message = message.content
        if message.author == self.user:
            return

        response = llm.create_chat_completion(
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": LLM_CONTEXT}
            ],
            max_tokens=50,
        )
        response = response['choices'][0]['message']['content'].strip()
        await channel.send(response)
        print(f'Sent message: {response}')
         
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

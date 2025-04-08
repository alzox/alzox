import discord
import os 
from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
    filename="*q8_0.gguf",
    verbose=False
)

TOKEN = os.getenv('DISCORD_TOKEN')
LLM_CONTEXT = """ 
"""
DONT_REPLY = [
    "Sorry, but I can't assist with that.",
    "I'm sorry, but I can't assist with that.",
    ""
]
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        user_message = message.content
        
        if message.author == self.user:
            return
        if len(user_message) == 1:
            print(f"User message is too short: {user_message}") 
            
            return

        response = llm.create_chat_completion(
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": LLM_CONTEXT}
            ],
            max_tokens=200,
        )
        response = response['choices'][0]['message']['content'].strip()
        
        if response in DONT_REPLY:
            print(f"Response is in DONT_REPLY: {response}")
            return
        
        await channel.send(response)
        print(f'Sent message: {response}')
         
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

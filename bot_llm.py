import discord
import os 
from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="bartowski/gemma-2-9b-it-GGUF",
    filename="*Q4_K_M.gguf",
    verbose=False,
    use_gpu=True,
    n_ctx=8192
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
        if len(user_message.split()) <= 1 and not user_message.startswith("!shadow"):
            print(f"User message is too short: {user_message}") 
            return
        elif user_message.startswith("!shadow"):
            user_message = "This is marriage counseling. Shadow how do you feel about Sonic cheating on you with Amy Rose?"
            print(f"User message: {user_message}")

        response = llm.create_chat_completion(
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": LLM_CONTEXT}
            ],
            temperature=0.7,
            top_p=0.9,
            frequency_penalty=0.0,
        )
        response = response['choices'][0]['message']['content'].strip()
        print(f"Response: {response}")
        if response in DONT_REPLY:
            response = "Get a load of this guy. :laughing:"
        
        await channel.send(response)
        print(f'Sent message: {response}')
         
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

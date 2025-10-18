# alzox 

## libraries used
```
discord.py
pip install -r requirements.txt
```

## set-up

1. Make an application at [https://discord.com/developers/applications](https://discord.com/developers/applications).
2. Get your token from the bot tab.
3. Enable "message content intent" in the same tab.
4. Add the token to local or global environment.
```
PS: $ENV:DISCORD_TOKEN="$TOKEN$"
CMD: set DISCORD_TOKEN=your_token_here
BASH: export DISCORD_TOKEN="$TOKEN$"
``` 
5. Run the file locally or host it somewhere.
```
python bot.py
```

## understanding discord's bot architecture

* Bot Token gets presented for a websocket
* Discord sends "interactions" via the websocket
* discord.py defines client server methods and configs
* discord.py uses Python's async/await built on-top of coroutines and non-blocking i/o

More resources about how discord runs can be found on their engineering [blog](https://discord.com/category/engineering)!

## modifying and adding features to bot.py

I have simple examples in bot.py that can be used as a starting template for bot commands. This is here to explain the main language feature and the interactions object.

* Decorators: They are function declarations, that either call the function or takes the function on the next-line as input.
* Interactions: Interaction is the main object discord.py passes into commands which contains the context of the message sent.

This is probably a really insufficient explanation, but google is a good friend and the documentation for discord.py is [here](https://discordpy-reborn.readthedocs.io/en/latest/index.html).

There are some pre-specified functions that you can implement with @bot.event like on_ready or on_command_error.

## running on start-up

To have your bot running while your computer is on everytime you can configure it to run on start-up. All it requires is you have set your DISCORD_TOKEN globally.

### window

Add and fill out the [discord_bot.bat]() with the correct file path to /Startup.

### linux 

There are multiple ways like configuring a systemd service or crontab. The easiest way is crontab -e.

```
crontab -e 
@reboot python file/to/bot.py &
```

### mac

Figuring this out.

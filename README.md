# ragebaiter
funny discord bot

## libraries used
```
discord.py
llama-cpp-python
pip install requirements.txt
```

## usage

1. make an application at https://discord.com/developers/applications
2. get your token from https://discord.com/developers/applications/$APPID$/bot
3. set message content intent enabled ^
4. generate a link from https://discord.com/developers/applications/$APPID$/oauth2
5. setenv to contain that token w/ name: DISCORD_TOKEN
```
PS: $ENV:DISCORD_TOKEN="$TOKEN$"
CMD: set DISCORD_TOKEN=your_token_here
BASH: export DISCORD_TOKEN="$TOKEN$"
``` 
6. run the file locally or host it somewhere

## understanding discord bot architecture

1. Bot Token is presented for a websocket
2. Discord sends events via the websocket
3. discord.py defines client methods and configs
4. Python's async/await that is built on-top of coroutines and non-blocking i/o
5. make something cool

## notes to self

* remember to await any operation that seems like i/o
* prompt engineering is really funny
* this makes me sad that most comment sections are just "this"

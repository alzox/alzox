# alzox 

## libraries used
```
discord.py
pip install -r requirements.txt
```

## set-up

1. make an application at https://discord.com/developers/applications
2. get your token from the bot tab
3. set message content intent enabled in the same tab
4. setenv to contain that token w/ name: DISCORD_TOKEN
```
PS: $ENV:DISCORD_TOKEN="$TOKEN$"
CMD: set DISCORD_TOKEN=your_token_here
BASH: export DISCORD_TOKEN="$TOKEN$"
``` 
5. run the file locally or host it somewhere

## understanding discord bot architecture

1. Bot Token is presented for a websocket
2. Discord sends "interactions" via the websocket
3. discord.py defines client server methods and configs
4. discord.py uses Python's async/await built on-top of coroutines and non-blocking i/o
5. Have a personal bot!

## modifying and adding features to the bot

* Decorators:
* Interactions:
* Documentation:

## running on start-up

* windows
* linux
* mac
* hiding terminal:

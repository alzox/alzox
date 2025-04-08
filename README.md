# ragebaiter
funny discord bot

## libraries used
```
discord.py
llama_cpp
```

## usage
```
get your token from https://discord.com/developers/applications/$APPID$/bot
set message content intent enabled ^
generate a link from https://discord.com/developers/applications/$APPID$/oauth2
run the file locally or host it somewhere
```


## understanding discord bot architecture

1. Bot Token is presented for a websocket
2. Discord sends events via the websocket
3. discord.py defines client methods and configs
4. Python's async/await that is built on-top of coroutines and non-blocking i/o
5. make something cool

## notes to self

* remember to await any operation that seems like i/o
* prmopt engineering is really funny
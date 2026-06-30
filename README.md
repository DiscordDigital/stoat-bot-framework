# stoat-bot-framework
A modular framework ready to be forked and turned into whatever you want. Makes use of stoat.py.

# How to use
Pretty simple, either download or fork this repository.

Then you can go into the mods folder, and delete modules that you don't need.

If you want to add functionality, you can create python files in that directory, which automatically get picked up during the start of `bot.py`.

On first launch, `bot.py` will create an `.env` file, which you need to edit.\
Insert the bot token into the file, and run `bot.py` again, then the bot should run.

## About modules
The modules require an instructor function, like this:
```python
async def instructor(bot, commands, **kwargs):
```

You can use `commands.Gear`, as well as bot to register events, as shown in the `onMessage`, `onMessageRename` and `onUserRemove` example mods.

It is also possible to register Gears, as shown in `onMessage`.

### About kwargs
`kwargs` is a variable that contains variables exposed in `.env`, so you can use them to configure the modules externally.

An example is the `ping` module, which displays a text from `.env`, specifically the `ping_text
` entry.

If you want to have multiple entries exposed in `modvars`, you can comma separate them like this:
```
economy_enabled=False
ping_text=Pong!
modvars=ping_text,economy_enabled
```

All exposed variables will become visible for all modules.\
The `token` and `bot_prefix` will not be included in `kwargs`.

### About kwargs["Client"]
This variable is also exposed to all modules. It contains an instance of `stoat.Client`.\
You can use this variable to interact with more complex endpoints, as shown in the `purge` module.

## About permissions
Please make sure you check for permissions according to your expectations of the bots behavior. Not only do you need to check if the user running the command is allowed to do it, you also need to check if the bot has the required permissions. An example on how to do it is shown in the `purge` module.

List of Permissions: https://stoatpy.readthedocs.io/en/latest/api/enums_and_flag_classes.html#stoat.Permissions
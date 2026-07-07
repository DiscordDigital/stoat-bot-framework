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

### About kwargs["Categories"]
In this variable are the display translations, as well as the keys for the gear categories, originating from categories.ini. It is used by the `help` module.

## About permissions
Please make sure you check for permissions according to your expectations of the bots behavior. Not only do you need to check if the user running the command is allowed to do it, you also need to check if the bot has the required permissions. An example on how to do it is shown in the `purge` module.

List of Permissions: https://stoatpy.readthedocs.io/en/latest/api/enums_and_flag_classes.html#stoat.Permissions

## About categories
This category system was built for the gears, you can add a category to a gear by adding the category property to the gear class. If you add a priority you can also alter the position of the category when the help command is used. If you don't use the same priority across multiple files containing gears with the same category, an average value will be determined. Commands outside of gears will be put in the misc category. If a gear has no category, it will also be put in misc.

If a category is used that is not inside categories.ini, then the text of the property is displayed in the help message.

A lower priority number means that it will appear first in the list. Misc has a priority of 100 by default.

Check out the `purge` module as an example on how to use categories and priorities. 
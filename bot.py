#!/usr/bin/env python3
from asyncio import run as asyncio_run
from dotenv import load_dotenv
from inspect import isclass
from os import getenv, listdir, path
from shutil import copy
from stoat import Client, ReadyEvent
from stoat.ext import commands

# Check if .env file exists, if not copy from template
if not path.isfile(path.dirname(__file__)+"/.env"):
    print(".env does not exist, creating it from .env.template.")
    copy(path.dirname(__file__)+"/.env.template", path.dirname(__file__)+"/.env")
    exit(1)

# Load .env file
load_dotenv()

# Read token from environment
token = getenv('token')

# Get bot prefix from environment
bot_prefix = getenv('bot_prefix')

# Load additional values from .env file, except token
# This gets passed to modules, as additional configuration options
modvars = getenv('modvars')

# Define empty dictionary for keyword arguments
modvarskw = {}

# Only run if the modvars variable returned something
if modvars:
    # Split by comma to get individual variables
    modvars = modvars.split(',')

    # For every custom option
    for var in modvars:
        # Skip token
        if var == 'token' or var == 'bot_prefix':
            continue
        # Insert variable into dictionary
        modvarskw[var] = getenv(var)

# Add a Client to modvarskw
modvarskw["Client"] = Client(token=token)

# Create MyBot class to register all modules
class MyBot(commands.Bot):
    # Print bot name to console
    async def on_ready(self, event: ReadyEvent) -> None:
        print(f'Logged in as {event.me.tag}!')

    # Register all modules located in the mods directory
    async def setup_hook(self) -> None:
        # Obtain all files located in mods folder
        modules = listdir("mods")

        # Iterate through the files in mods folder
        for module in modules:
            # Skip the __init__.py file and assure file is a python file
            if module.endswith(".py") and (module != "__init__.py"):
                # Obtain the moduleName by removing .py from filename
                moduleName = module.replace(".py","")

                # Print to console about module being loaded
                print("Loading " + module)

                # Load the instructor function into the loadMod variable
                loadMod = getattr(__import__("mods."+moduleName, fromlist=['instructor']), 'instructor')

                # Call loadMod to register the module
                await loadMod(bot, commands, **modvarskw)

# Set bot prefix
bot = MyBot(command_prefix=bot_prefix)

# Exit if no token is provided
if token == '<token here>':
    print("Please replace <token here> with your bots token in the .env file.")
    exit(1)

# Run the bot
bot.run(token)

# Cleanup Client
asyncio_run(modvarskw["Client"].http.cleanup())
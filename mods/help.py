from stoat import SendableEmbed

async def instructor(bot, commands, **kwargs):
    @bot.command(help="Shows all commands registered in the bot")
    async def help(ctx: commands.Context[commands.Bot]) -> None:
        output = ""

        # Positioning score for sort
        gearMeta = {}

        # Total amount a priority was added
        gearMetaCounts = {}

        # Command information, such as name and help
        gearMetaNames = {}

        # A list of commands that have been categorized, other commands will land in misc
        categorizedCommands = []

        for gearName in bot.gears:
            gear = bot.get_gear(gearName)
            if hasattr(gear, "category"):
                if hasattr(gear, "priority"):
                    priority = gear.priority
                else:
                    priority = 1
                if gear.category not in gearMeta:
                    gearMeta[gear.category] = 0
                
                gearMeta[gear.category] += priority
                
                if not gear.category in gearMetaCounts:
                    gearMetaCounts[gear.category] = 0

                gearMetaCounts[gear.category] += 1

                if not gear.category in gearMetaNames:
                    gearMetaNames[gear.category] = []
                
                for command in gear.walk_commands():
                    categorizedCommands.append(command.name)
                    gearMetaNames[gear.category].append({"name": command.name, "help": command.help})

        priorityScore = {}

        for key, value in gearMeta.items():
            priorityScore[key] = value / gearMetaCounts[key]

        priorityScore["misc"] = 100
 
        if "misc" not in gearMetaNames:
            gearMetaNames["misc"] = []

        for command in bot.walk_commands():
            if command.name in categorizedCommands:
                continue
            gearMetaNames["misc"].append({"name": command.name, "help": command.help})

        sortedCategories = {k: v for k, v in sorted(priorityScore.items(), key=lambda item: item[1])}

        i = 0
        for category in sortedCategories:
            if category in kwargs["Categories"]:
                output += kwargs["Categories"][category] + "\n"
            else:
                output += category + "\n"

            for command in gearMetaNames[category]:
                if not command["help"]:
                    helptext = "No help text provided."
                else:
                    helptext = command["help"]
                output += "**" + command["name"] + "** - " + helptext + "\n"
            
            output += "\n"
            i += 1

        output = output.rstrip()

        em = SendableEmbed(title="Help", color="#cccccc", description=output)

        await ctx.message.reply("", embeds=[em], mention=False)
async def instructor(bot, commands, **kwargs):
    @bot.command(help="Shows all commands registered in the bot")
    async def help(ctx: commands.Context[commands.Bot]) -> None:
        output = "=== Help ===\n"
        for cmd in bot.walk_commands():
            output += f"{cmd.name} - {cmd.help}\n"
        await ctx.message.reply(output)

async def instructor(bot, commands, **kwargs):
    @bot.command(help="Run this command to send a ping")
    async def ping(ctx: commands.Context[commands.Bot]) -> None:
        await ctx.message.reply(kwargs["ping_text"])

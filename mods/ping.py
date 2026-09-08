import json

async def instructor(bot, commands, apiEvent, **kwargs):
    @apiEvent.on("ping")
    async def handle_ping(data):
        pingData = json.loads(data)
        print("Response from API: " + pingData["data"]) # Hello World

    @bot.command(help="Run this command to send a ping")
    async def ping(ctx: commands.Context[commands.Bot]) -> None:
        await ctx.message.reply(kwargs["ping_text"])

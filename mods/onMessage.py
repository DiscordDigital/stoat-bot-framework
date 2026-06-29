from stoat import MessageCreateEvent

async def instructor(bot, commands, **kwargs):
    class MyGear(commands.Gear, name='MessageListener'):
        @commands.Gear.listener()
        async def on_message(self, event: MessageCreateEvent) -> None:
            msg = event.message
            author = msg.author

            if msg.content.casefold() == 'hello' and not author.bot:
                print(f'{author.tag} ran hello command')
                await msg.reply('Hello world!')
    await bot.add_gear(MyGear())
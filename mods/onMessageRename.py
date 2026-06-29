from stoat import MessageUpdateEvent

async def instructor(bot, commands, **kwargs):
    @bot.listen()
    async def on_message_edit(event: MessageUpdateEvent) -> None:
        if (before := event.before) and (after := event.after):
            print(f'{after.author.tag} edited a message: {before.content} => {after.content}')

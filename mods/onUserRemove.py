from stoat import ServerMemberRemoveEvent

async def instructor(bot, commands, **kwargs):
    class MyGear(commands.Gear, name='MemberRemoveEvent'):
        @commands.Gear.listener()
        async def on_remove(self, event: ServerMemberRemoveEvent) -> None:
            print(f'User with id {event.user_id} was removed from the server.')
    await bot.add_gear(MyGear())
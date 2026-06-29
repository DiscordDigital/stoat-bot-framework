async def instructor(bot, commands, **kwargs):
    @bot.command(help="Delete a specified number of messages from the channel")
    async def purge(ctx: commands.Context[commands.Bot]) -> None:
        # Get user as server member
        member = ctx.message.get_author_as_member()

        # Check if user can delete messages in that channel
        if not ctx.message.server.permissions_for(member).manage_messages:
            return

        # Get bot as server member
        botMember = await ctx.message.server.fetch_member(bot.user)

        # Get number from message
        args=ctx.message.content.split(" ")
        if len(args) == 2 and args[1].isdigit():
            num = int(args[1])
        else:
            await ctx.message.reply("Please specify the amount. (Maximum 100)")
            return

        # Abort if messages to be deleted are over 100        
        if num > 100:
            await ctx.message.reply("Can't delete more than 100 messages.")
            return
        
        # Check if bot can delete messages in that channel
        if not ctx.message.server.permissions_for(botMember).manage_messages:
            await ctx.message.reply("I don't have permission to delete messages.")
            return
        
        # Check if bot can view message history
        if not ctx.message.server.permissions_for(botMember).read_message_history:
            await ctx.message.reply("I don't have permission to view message history.")
            return

        # Obtaining messages to delete.
        messages = await ctx.message.channel.history(limit=num)
        for message in messages:
            # Delete message
            await message.delete()

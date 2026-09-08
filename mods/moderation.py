import re

async def instructor(bot, commands, apiEvent, **kwargs):
    class MyGear(commands.Gear, name='ModerationTools'):
        def __init__(self, bot):
            self.bot = bot
            self.category = 'moderation'
            self.priority = 10
            self.userPattern = re.compile(r'<@(.*?[^ ])>', flags=re.DOTALL)

        async def check_permission(self, ctx, **kwargs):
            if kwargs["botuser"]:
                # Server member from bot
                member = await ctx.message.server.fetch_member(bot.user)
            else:
                # Server member from user
                member = ctx.message.get_author_as_member()
            
            # Return bool
            return getattr(ctx.message.server.permissions_for(member), kwargs["permission"])

        @commands.command(help="Delete a specified number of messages from the channel")
        async def purge(self, ctx: commands.Context[commands.Bot]) -> None:
            # Get user as server member
            member = ctx.message.get_author_as_member()

            # Check if user can delete messages in that channel
            if not await self.check_permission(ctx, botuser=False, permission="manage_messages"):
                return

            # Get bot as server member
            botMember = await ctx.message.server.fetch_member(bot.user)

            # Get number from message
            args=ctx.message.content.split(" ")
            if len(args) == 2 and args[1].isdigit():
                num = int(args[1])
                num += 1
            else:
                await ctx.message.reply("Please specify the amount. (Maximum 100)")
                return

            # Abort if messages to be deleted are over 100        
            if num > 100:
                await ctx.message.reply("Can't delete more than 100 messages.")
                return

            # Check if bot can delete messages in that channel
            if not await self.check_permission(ctx, botuser=True, permission="manage_messages"):
                await ctx.message.reply("I don't have permission to delete messages.")
                return

            # Check if bot can view message history
            if not await self.check_permission(ctx, botuser=True, permission="read_message_history"):
                await ctx.message.reply("I don't have permission to view message history.")
                return

            # Obtaining messages to delete.
            messages = await ctx.message.channel.history(limit=num)
            await kwargs["Client"].http.delete_messages(ctx.message.channel, messages)
        
        @commands.command(help="Kicks one or more users from the server")
        async def kick(self, ctx: commands.Context[commands.Bot]) -> None:
            # Check if user can kick
            if not await self.check_permission(ctx, botuser=False, permission="kick_members"):
                return
            
            # Check if bot can kick
            if not await self.check_permission(ctx, botuser=True, permission="kick_members"):
                await ctx.message.reply("I don't have permission to kick members.")
                return
            
            # Obtain IDs from message
            patternMatches = self.userPattern.findall(ctx.message.content)

            # If no IDs were found
            if len(patternMatches) == 0:
                await ctx.message.reply("Please specify the user(s) with @.")
                return

            # For every id, attempt to kick user, if failed, collect id for output
            erroredIds = []
            for id in patternMatches:
                try:
                    user = await kwargs["Client"].fetch_user(id)
                    await kwargs["Client"].http.kick_member(ctx.message.server, user)
                    await ctx.message.reply(user.name + "#" + user.discriminator + " was kicked from the server.")
                except Exception:
                    erroredIds.append(str(id))
            
            # Output errors, if any happened
            if len(erroredIds) > 0:
                await ctx.message.reply("Failed to kick member with id(s): " + ", ".join(erroredIds))

    await bot.add_gear(MyGear(bot))

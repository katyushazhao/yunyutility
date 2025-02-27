import discord.app_commands as application
import discord.ext.commands as commands

import discord
import logging
import bot

class Debug(commands.GroupCog):
    def __init__(self, bot: bot.Bot, logger: logging.Logger):
        super().__init__()
        self.logger = logger
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return await self.bot.is_owner(interaction.user)

    @application.command(description="Synchronise application commands.")
    @application.describe(guild="The guild ID to sync to.")
    async def sync(self, interaction: discord.Interaction, guild: str | None):
        if guild is None:
            await self.bot.tree.sync()
            await interaction.response.send_message("Global commands synchronised.")
            self.logger.info("Global commands synchronised.")
        else:
            snowflake = discord.Object(guild)
            await self.bot.tree.sync(guild=snowflake)
            await interaction.response.send_message("Guild-specific commands synchronised.")
            self.logger.info("Guild-specific commands synchronised.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        self.logger.info("Global commands synchronised.")
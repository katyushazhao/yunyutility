from discord.ext import commands
from random import randint
from utilities import *
import youtube_dl
import validators
import asyncio
import discord
import os

ytformatopt = {
    "format": 'bestaudio/best',
    "outtmpl": '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"
}

ffmpegopt = {
    "options": "-vn"
}

class voice(commands.Cog):
    """Implements voice capabilities."""

    def __init__(self, bot):
        self.ytdl = youtube_dl.YoutubeDL(ytformatopt)
        self.mfold = "data/music/"
        self.queuectx = None
        self.queue = []
        self.bot = bot

    async def getstream(self, query: str):
        if not validators.url(query): query = f"ytsearch1:{query}"
        data = await self.bot.loop.run_in_executor(None, lambda: self.ytdl.extract_info(query, download=False))
        if "entries" in data: data = data["entries"][0]
        audio = await discord.FFmpegOpusAudio.from_probe(data["url"], options=ffmpegopt)
        return (audio, data)

    async def finaliser(self, error: Exception):
        if error: await ctx.send(f"Error caught during audio playback: {error}.")
        if len(self.queue) > 0: await self.playaudio(self.queue.pop())

    def finaliserstub(self, error: Exception):
        self.bot.loop.create_task(self.finaliser(error))

    async def playaudio(self, query: str):
        if not os.path.exists(self.mfold + query): audio, metadata = await self.getstream(query)
        else: audio = await discord.FFmpegOpusAudio.from_probe(self.mfold + query)
        if self.queuectx.voice_client.is_playing(): self.queuectx.voice_client.stop()
        self.queuectx.voice_client.play(audio, after=self.finaliserstub)

    @commands.command()
    async def stop(self, ctx):
        """Stop any audio from playing."""
        if ctx.voice_client: ctx.voice_client.stop()
        await ctx.send("Music stopped!", delete_after=5)

    @commands.command(aliases=["resume"])
    async def pause(self, ctx):
        """Pause/resume."""
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                await ctx.send("Audio paused :(", delete_after=10)
            elif ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                await ctx.send("Audio resumed :)", delete_after=10)

    @commands.command()
    async def queue(self, ctx):
        """Print out the current queue."""
        embed = getembed("Bakerbot: Global audio queue.", "jingle jam 2020")
        iterator = 0

        for query in self.queue:
            embed.add_field(name=f"#{iterator}", value=query)
            iterator += 1

        if len(self.queue) == 0: await ctx.send("Nothing in queue.", delete_after=10)
        else: await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        """Skips the current song."""
        self.queuectx = ctx
        if len(self.queue) > 0: await self.playaudio(self.queue.pop())
        else: await ctx.send("Audio queue empty.", delete_after=10)

    @commands.command()
    async def play(self, ctx, *, query: str):
        """Plays audio to a voice channel. Accepts both local filenames or YouTube URLs."""
        if len(self.queue) == 0 and not ctx.voice_client.is_playing():
            embed = getembed("Bakerbot: Now playing.", "jingle jam 2020")

            if not os.path.exists(self.mfold + query):
                audio, metadata = await self.getstream(query)
                embed.add_field(name="Remote audio source.", value=f"[{metadata['title']}]({metadata['webpage_url']})")
            else: embed.add_field(name="Local audio file.", value=query)

            self.queuectx = ctx
            await ctx.send(embed=embed)
            await self.playaudio(query)
        else:
            embed = getembed("Bakerbot: Adding to queue.", "jingle jam 2020")
            embed.add_field(name="Search term.", value=query)
            await ctx.send(embed=embed)
            self.queue.append(query)

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel."""
        if ctx.voice_client is not None: 
            if ctx.author.voice: await ctx.voice_client.move_to(ctx.author.voice.channel)
            else: await ctx.send("You are not connected to a voice channel.", delete_after=10)
        elif ctx.author.voice: await ctx.author.voice.channel.connect()
        else: await ctx.send("You are not connected to a voice channel.", delete_after=10)

    @commands.command(aliases=["dc"])
    async def disconnect(self, ctx):
        """Disconnects Bakerbot from any voice channels."""
        if ctx.voice_client: await ctx.voice_client.disconnect()
        await ctx.send("Voice client disconnected.", delete_after=10)

    @play.before_invoke
    async def ensureconnection(self, ctx):
        await self.join(ctx)

def setup(bot): bot.add_cog(voice(bot))

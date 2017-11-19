import asyncio
import functools
import discord
import discord.ext.commands as commands
import youtube_dl
from utils import config

config = config.Config('config/bot.json')
ROLES = config.get('roles')


class MusicError(commands.CommandError):
    pass


class Song(discord.PCMVolumeTransformer):

    def __init__(self, info, requester, channel):
        self.info = info
        self.requester = requester
        self.channel = channel
        super().__init__(discord.FFmpegPCMAudio(info['url']))

    def __str__(self):
        return f"{self.info['title']} from {self.info['creator'] or self.info['uploader']} (duration: {self.info['duration']}s)"


class GuildMusicState:

    def __init__(self, loop):
        self.playlist = asyncio.Queue(maxsize=50)
        self.voice_client = None
        self.loop = loop
        self.player_volume = 0.5
        self.skips = set()
        self.min_skips = 5

    @property
    def current_song(self):
        return self.voice_client.source

    @property
    def volume(self):
        return self.player_volume

    @volume.setter
    def volume(self, value):
        self.player_volume = value
        self.voice_client.source.volume = value

    def clear(self):
        self.playlist._queue.clear()

    async def stop(self):
        self.clear()
        if self.voice_client:
            self.voice_client.stop()
            await self.voice_client.disconnect()
        self.voice_client = None

    def is_playing(self):
        return self.voice_client and self.voice_client.is_playing()

    async def play_next_song(self, error=None):
        if error:
            await self.current_song.channel.send(f'An error has occurred while playing {self.current_song}: {error}')

        if not self.playlist.empty():
            next_song = self.playlist.get_nowait()
            next_song.volume = self.volume
            self.voice_client.play(next_song, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_song(error), self.loop).result())
            await next_song.channel.send(f'Now playing {next_song}')


class Music:

    def __init__(self, bot):
        self.bot = bot
        self.music_states = {}

    def __unload(self):
        for state in self.music_states.values():
            self.bot.loop.create_task(state.stop())

    def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command cannot be used in a private message.')
        return True

    async def __before_invoke(self, ctx):
        ctx.music_state = self.get_music_state(ctx.guild.id)

    async def __error(self, ctx, error):
        """Local command error handler."""
        if not isinstance(error, commands.CommandError):
            raise error

        try:
            await ctx.send(error)
        except discord.Forbidden:
            pass  # /shrug

    def get_music_state(self, guild_id):
        """Retrieves the MusicState from a guild id. Create it if needed."""
        state = self.music_states.get(guild_id)
        if not state:
            state = GuildMusicState(self.bot.loop)
            self.music_states[guild_id] = state
        return state

    @commands.command()
    async def info(self, ctx):
        """Displays the currently played song."""
        if ctx.music_state.is_playing():
            song = ctx.music_state.current_song
            await ctx.send(f'Playing {song}. Volume at {song.volume * 100}% in {ctx.music_state.voice_client.channel.mention}')
        else:
            await ctx.send('Not playing.')

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel=None):
        """Summons the bot to a voice channel.
        If no channel is given, summons it to your current voice channel.
        """
        if channel is None and not ctx.author.voice:
            raise MusicError('You are not in a voice channel nor specified a voice channel for me to join.')

        destination = channel or ctx.author.voice.channel

        if ctx.music_state.voice_client:
            ctx.music_state.voice_client.move_to(destination)
        else:
            ctx.music_state.voice_client = await destination.connect()

    @commands.command()
    async def play(self, ctx, *, song: str):
        """Plays a song or adds it to the playlist.
        Automatically searches with youtube_dl.
        List of supported sites :
        https://github.com/rg3/youtube-dl/blob/1b6712ab2378b2e8eb59f372fb51193f8d3bdc97/docs/supportedsites.md
        """
        voice_client = ctx.music_state.voice_client

        # Connect to the voice channel if needed
        if voice_client is None or not voice_client.is_connected():
            await ctx.invoke(self.join)
            voice_client = ctx.music_state.voice_client

        # Retrieve info from youtube
        ytdl_opts = {
            'default_search': 'auto',
            'format': 'webm[abr>0]/bestaudio/best',
            'prefer_ffmpeg': True,
            'quiet': True
        }
        ytdl = youtube_dl.YoutubeDL(ytdl_opts)
        partial = functools.partial(ytdl.extract_info, song, download=False)
        info = await self.bot.loop.run_in_executor(None, partial)
        if "entries" in info:
            info = info['entries'][0]  # Only pick the first song of a playlist

        # Add the song to the playlist
        source = Song(info, ctx.author, ctx.channel)
        try:
            ctx.music_state.playlist.put_nowait(source)
        except asyncio.QueueFull:
            raise MusicError('Playlist is full, try again later.')

        # Start playing or notify it's been added to the playlist
        if not ctx.music_state.is_playing():
            await ctx.music_state.play_next_song()
        else:
            await ctx.send(f'Queued {source} in position #{ctx.music_state.playlist.qsize()}')

    @commands.command()
    async def pause(self, ctx):
        if ctx.music_state.voice_client:
            ctx.music_state.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        if ctx.music_state.voice_client:
            ctx.music_state.voice_client.resume()

    @commands.command()
    @commands.has_any_role(*ROLES['admin'])
    async def stop(self, ctx):
        """Stops the player, clears the playlist and leaves the voice channel."""
        await ctx.music_state.stop()

    @commands.command()
    async def volume(self, ctx, volume: int=None):
        """Sets the volume of the player, scales from 0 to 100."""
        if volume < 0 or volume > 100:
            raise MusicError('The volume level has to be between 0 and 100.')
        ctx.music_state.volume = volume / 100

    @commands.command()
    @commands.has_any_role(*ROLES['admin'])
    async def clear(self, ctx):
        """Clears the playlist."""
        ctx.music_state.clear()

    @commands.command()
    async def skip(self, ctx):
        """Votes to skip the current song.
        To configure the minimum number of votes needed, use `minskips`
        """
        if ctx.author.id in ctx.music_state.skips:
            await ctx.message.add_reaction('\N{CROSS MARK}')
            raise MusicError('You already voted to skip that song')

        ctx.music_state.skips.add(ctx.author.id)
        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        if len(ctx.music_state.skips) > ctx.music_state.min_skips or ctx.author == ctx.music_state.current_song.requester:
            ctx.music_state.skips.clear()
            ctx.music_state.voice_client.stop()
            await ctx.music_state.play_next_song()

    @commands.command()
    @commands.has_any_role(*ROLES['admin'])
    async def next(self, ctx):
        """Plays the next song from the playlist"""
        if ctx.music_state.is_playing():
            ctx.music_state.voice_client.stop()
            await ctx.music_state.play_next_song()

    @commands.command()
    # @commands.has_permissions(manage_guild=True)
    @commands.has_any_role(*ROLES['admin'])
    async def minskips(self, ctx, number: int):
        """Sets the minimum number of votes to skip a song."""
        ctx.music_state.min_skips = number


def setup(bot):
    if not discord.opus.is_loaded():
        # mac: /usr/local/Cellar/opus/1.2.1/lib/libopus.0.dylib
        discord.opus.load_opus('opus')
    bot.add_cog(Music(bot))

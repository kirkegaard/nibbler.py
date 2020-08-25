from os import environ

# Bot settings
TRIGGER = "!"
DEBUG = True

# Extensions
EXTENSION_PATH = "extensions"
EXTENSIONS = [
    "brain",
    "channel_events",
    "dadjoke",
    "guess",
    "hva",
    "lastfm",
    "reddit",
    "reply",
    "rng",
    "timer",
    "tvtid",
    "urbandictionary",
    "utils",
    "wttr",
    "yourmom",
]

# Tokens
DISCORD_TOKEN = environ.get("DISCORD_TOKEN")

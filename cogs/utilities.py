from discord.ext import commands

class Utilities(commands.Cog, name="utilities"):
    """A collection of useful constants. No actual functions here :("""
    def __init__(self) -> None:
        # Common colours.
        self.error_colour = 0xFF3300
        self.success_colour = 0x00C92C
        self.regular_colour = 0xF5CC00
        self.gaming_colour = 0x0095FF

        # Icon URLs.
        self.note_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Note_icon.svg/480px-Note_icon.svg.png"
        self.illuminati_icon = "https://upload.wikimedia.org/wikipedia/commons/a/a9/Illuminati_triangle_eye.png"
        self.tick_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/500px-Flat_tick_icon.svg.png"
        self.cross_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flat_cross_icon.svg/500px-Flat_cross_icon.svg.png"

        # A regex to check for URLs.
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

        # Admin Abuse-related IDs.
        self.aa_server_id = 554211911697432576
        self.aa_defrole_id = 702649631875792926

        # Wavelink node dictionary.
        self.wavelink_nodes = {
            "main": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "main",
                "region": "sydney"
            }
        }

        # Reaction dictionary (for choosing stuff, I suppose?)
        self.react_options = {
            "1️⃣": 1,
            "2️⃣": 2,
            "3️⃣": 3,
            "4️⃣": 4,
            "5️⃣": 5,
            "6️⃣": 6,
            "7️⃣": 7,
            "8️⃣": 8,
            "9️⃣": 9
        }

def setup(bot): bot.add_cog(Utilities())

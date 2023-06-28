"""DEFINE YOUR MODALS HERE"""
import os
import time
import discord
import random
import datetime
from discordwebhook import Discord
from discord import ui as UI
from discord.ui import Modal
from _utils.weather import get_weather as Weather
from _utils.bruhpy import BruhPy
from _utils.lifegen import LifeGen
from _utils.nolang import Nolang
from .embeds import weather as weather_embed
from .embeds import bruhby as bruhpy_embed
from .embeds import nolang as nolang_embed

class UserInputModal(Modal):
    def __init__(self, prompt, short_or_long, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if short_or_long == "short":
            self.add_item(UI.TextInput(label=prompt, style=discord.TextStyle.short))
        else:
            self.add_item(UI.TextInput(label=prompt, style=discord.TextStyle.long))


class WeatherModal(Modal):
    def __init__(self, typE, prompt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(UI.TextInput(label=prompt, style=discord.TextStyle.short))
        self._typE = typE

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        orignal_response = await interaction.original_response()
        try:
            weather = await Weather(self.children[0].value, self._typE)
            embed = weather_embed(weather, type=self._typE)
        except ValueError:
            embed = discord.Embed(
                title=f"Unable to get weather for {self.children[0].value}",
                description=(
                    "Hey man! Not sure what happened but I guess I couldn't get the"
                    " weather for that city. No worries though, I am sure you can"
                    " google it!!!"
                ),
                color=random.randint(0, 0xFFFFFF),
                timestamp=datetime.datetime.now(),
            )
            embed.set_image(url=self._emoji_to_image.get(None))
            embed.set_footer(text='verified.  ✅', icon_url='https://avatars.githubusercontent.com/u/132738989?s=400&u=36375e751dc38b698a858540b8fdd38f4d98396c&v=4')

        await orignal_response.edit(view=None, embed=embed)


class BruhPyModal(Modal):
    def __init__(self, show_code, prompt, view, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(UI.TextInput(label=prompt, style=discord.TextStyle.long))
        self._tags = {
            "ERROR": "ansi",
            "NORMAL": "",
            "PY": "py",
            "INFO": "ansi",
        }
        self._view = view
        self._show_code = show_code

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        original_response = await interaction.original_response()
        await original_response.edit(view=self._view)

        # split the program
        program = self.children[0].value.split(' ')
        # run the program with the bruhpy class
        run_result = BruhPy(debug=False).run(arg="-s" if self._show_code else program[0],
                                             argvs=program if self._show_code else program[1:], 
                                             user=str(interaction.user)
                                            )
        
        embed = None
        code = None

        for res in run_result:
            # if there is output / error create an embed with the output
            if res[0] == 'OUTPUT' or res[0] == 'ERROR':
                embed = bruhpy_embed(res, str(interaction.user))
            # if they enabled show code, then add the code as content
            elif res[0] == 'PY':
                code = f"```py\n{res[1]}```"
        
        if embed:
            await original_response.edit(content='' if not code else code, view=None, embed=embed)
        else:
            await original_response.edit(content='' if not code else code, view=None)


class NolangModal(Modal):
    def __init__(self, show_code, prompt, view, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(UI.TextInput(label=prompt, style=discord.TextStyle.long))
        self._tags = {
            "ERROR": "ansi",
            "NORMAL": "",
            "PY": "",
            "INFO": "ansi",
        }
        self._view = view
        self._show_code = show_code

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        original_response = await interaction.original_response()
        await original_response.edit(view=self._view)

        # split the program
        program = self.children[0].value.split(' ')
        # run the program with the nolang class
        run_result = Nolang(debug=False).run(arg="-s" if self._show_code else program[0],
                                            argvs=program if self._show_code else program[1:],
                                            user=str(interaction.user))
        
        embed = None
        code = None

        for res in run_result:
            # if there is output / error create an embed with the output
            if res[0] == "OUTPUT" or res[0] == "ERROR":
                embed = nolang_embed(res, str(interaction.user))
            # if they enabled show code, then add the code as content
            elif res[0] == 'NL':
                code = f"```py\n{res[1]}```"
        
        if embed:
            await original_response.edit(content='' if not code else code, view=None, embed=embed)
        else:
            await original_response.edit(content='' if not code else code, view=None)


class GameOfLifeModal(Modal):
    marcus_says = Discord(url=os.environ["MARCUS"])

    def __init__(self, show_config, view, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.marcus_says = Discord(url=os.environ["MARCUS"])
        self._view = view
        self._show_config = show_config
        self.add_item(
            UI.TextInput(label="Enter a Grid Size:", style=discord.TextStyle.short)
        )
        self.add_item(
            UI.TextInput(
                label="Enter a Refresh Speed(ms):", style=discord.TextStyle.short
            )
        )
        self.add_item(
            UI.TextInput(label="Enter a Color Map:", style=discord.TextStyle.short)
        )
        self.add_item(
            UI.TextInput(label="Enter an Interpolation:", style=discord.TextStyle.short)
        )
        self.add_item(
            UI.TextInput(
                label="Render decay (0-no, 1-yes): ", style=discord.TextStyle.short
            )
        )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        original_response = await interaction.original_response()
        await original_response.edit(view=self._view)
        values = [child.value for child in self.children]
        try:
            life = LifeGen(values[4] == "1")
            life.gen_life_gif(int(values[0]), int(values[1]), values[2], values[3])
            with open("./BOT/_utils/_gif/tmp.gif", "rb") as life_gif:
                gif = discord.File(life_gif)
                await original_response.add_files(gif)
                if self._show_config:
                    await original_response.edit(
                        content=f"""```\nSize          : {values[0]}\nSpeed         : {values[1]}\nColormap      : {values[2]}\nInterpolation : {values[3]}\n```""",
                        view=None,
                    )
                else:
                    await original_response.edit(view=None)
        except Exception as e:
            with open("./error.fnbbef", "a+") as f:
                f.write(f"{time.time()} -> {str(e)}\n")
            await original_response.edit(
                content=(
                    "erm . . . what you requested is too large for a wee little boy"
                    " like me [shaking, looks at ground nervously]. .  . uwu!"
                ),
                view=None,
            )
            self.marcus_says.post(content="bro is not packing! 😭 🤣 🤣")

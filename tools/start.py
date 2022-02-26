import discord
from discord.ext import commands
import urllib
import os
import pathlib
import time
from download import download
import subprocess
from subprocess import PIPE, Popen
import shlex

bot = commands.Bot(command_prefix='.')

@bot.command()
async def decompile(ctx, arg1=None):
    if arg1 != None:
        if "http://" in arg1 or "https://" in arg1:
            await ctx.send("Note: The bot might randomly go offline, this is a known behavior, but the bot should be working after that.")
            executable_name = os.path.basename(arg1)
            await ctx.send("Downloading " + str(executable_name) + "...")
            start_time = time.time()
            output_dir = os.getcwd() + "\DOWNLOAD\{0}".format(executable_name)
            if os.path.exists(output_dir):
                os.remove(output_dir)
            executable = download(arg1, output_dir, replace=True)
            end_time = time.time()
            time_lapsed = end_time - start_time
            sec = time_lapsed
            mins = sec // 60
            sec = sec % 60
            hours = mins // 60
            mins = mins % 60
            await ctx.send("Downloaded " + str(executable_name))
            await ctx.send("Time Lapsed: " + str(int(hours)) + "h" + str(int(mins)) + "m" + str(int(sec)) + "s")
            await ctx.send("Decompiling...")
            cmd=['python', 'condadev.py', str(output_dir)]
            p = subprocess.Popen(cmd,
                                 stdout=subprocess.PIPE, shell=True)
            for line in iter(p.stdout.readline, b''):
                 await ctx.send('{}'.format(line.rstrip()))
            await ctx.send("Decompilation successfully!")
            await ctx.send("Cleaning up the host...")
            os.remove(output_dir)
            await ctx.send("Uploading the MFA...")
            await ctx.send(file=discord.File(r'{0}'.format(os.getcwd() + '\OUTPUT\output.mfa')))
            await ctx.send("Done!")
        else:
            await ctx.send("Error: Invaild link detected!")
    else:
        await ctx.send('Error: You must specify the direct link to the executable you want to decompile!')

token_file = open("token.dev", "r+")
token = token_file.read()
print("Bot current token: " + token)
bot.run(token)

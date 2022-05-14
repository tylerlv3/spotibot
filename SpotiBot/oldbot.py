import discord
from discord.ext import commands
import random
import gspread
import requests

sa = gspread.service_account()
sh = sa.open('SpotifyLogs')

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    guild = message.guild
    wks2 = sh.worksheet("LogsTest")
    count = requests.get("https://upgrader.cc/API/?stock")
    user = message.author
    print(user)
    if message.content == ".rc":
        wks = sh.worksheet("upCount")
        wks.update('A1', 0)
    else:
        pass
    if guild != '917536582301532161' and message.content == ".upgrade":
        count = requests.get("https://upgrader.cc/API/?stock")
        if len(count.json()) > 4:
            air1 = wks2.find(str(user))
            print(air1)
            if str(air1) == "None":
                await cust_chan(message)
            else:
                if message.author.id != 974419378974109727 and message.channel.category.id == 974474230710296618:
                    cUser = str(message.author)
                    userID = str(wks2.find(cUser)).lstrip("<Cell R").split("C")[0]
                    repchan = wks2.acell('B' + str(userID)).value
                    bChan = discord.utils.get(client.get_all_channels(), name=repchan)
                    embed1 = discord.Embed(title="Invalid Key, try again", color=15158332)
                    embed2 = discord.Embed(title="Spotify Username",
                                           description=str(cUser) + "\n\nPlease enter your Spotify Username.",
                                           color=3066993)
                    embed3 = discord.Embed(title="Spotify Password",
                                           description=str(cUser) + "\n\nPlease enter your Spotify Password.",
                                           color=3066993)
                    if userID != "None" and len(message.content) == 19:
                        try:
                            count = requests.get("https://upgrader.cc/API/?stock")
                            resp = requests.get("https://upgrader.cc/API/?info=" + str(message.content))
                            uKey = "C" + str(userID)
                            wks2.update(uKey, message.content)
                            respP = str(resp.json())
                            if "none" in respP:
                                await bChan.send(embed=embed2)
                                list = [1, 4, 7, 10]
                                code = str(count.json()).split(",")[random.choice(list)].split(":")[1].strip("'").split(
                                        "'")[1]
                                uKey2 = "D" + str(userID)
                                wks2.update(uKey2, message.content)
                                await bChan.send(embed=embed3)
                                check2 = wks2.acell("E" + str(userID)).value
                                if check2 == "None":
                                    uKey2 = "E" + str(userID)
                                    wks2.update(uKey2, message.content)
                                    await bChan.send(embed=embed3)
                            else:
                                await bChan.send(
                                    "Key is already premium, contact vxnii if it is saying this but your premium is gone")
                        except:
                            await bChan.send(embed=embed1)

                    else:
                        await bChan.send(embed=embed1)
                else:
                    print("already has open upgrade channel")

        else:
            chan = message.channel
            await chan.send("Cannot Upgrade Right Now, Try Again Later")
    else:
        pass





async def cust_chan(message):
    member = message.author
    guild = message.guild
    wks = sh.worksheet("upCount")
    count = wks.acell('A1').value
    tail = int(count) + 1
    wks.update('A1', tail)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        member: discord.PermissionOverwrite(read_messages=True)}
    upChan = await guild.create_text_channel("Upgrade - " + str(tail), overwrites=overwrites,category=client.get_channel(974474230710296618))
    embed1 = discord.Embed(title="Spotify Upgrader", description=str(member) + ", This Channel is where you will access your spotify premium, To begin please send your key you purchased",color=3066993)
    await upChan.send(member.mention, embed=embed1)
    wks2 = sh.worksheet("LogsTest")
    rowC = wks2.acell('A1').value
    rLog = int(rowC) + 1
    wks2.update('A1', rLog)
    uRow = "A" + str(wks2.acell('A1').value)
    cRow = "B" + str(wks2.acell('A1').value)
    wks2.update(uRow, str(member))
    wks2.update(cRow, str(upChan))
    print(upChan)





client.run('OTc0NDE5Mzc4OTc0MTA5NzI3.GDAzQN.61RLQsTscQCGhOQoIU8Nl7kTW4yxa2WYpXmz4k')

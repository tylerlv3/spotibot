import time

import discord
from discord.ext import commands
import random
import gspread
import requests

sa = gspread.service_account()
sh = sa.open('SpotifyLogs')
wks = sh.worksheet("upCount")
wks2 = sh.worksheet("LogsTest")

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_reaction_add(reaction, user):
    if user.id != 974419378974109727:
        emoj = reaction.emoji
        if emoj == "✅":
            print("Sending through API")
            await reaction.message.remove_reaction("❌", reaction.message.author)
            embed5 = discord.Embed(title="Upgrading ⚙️", color=3066993)
            editable = await reaction.message.channel.send(embed=embed5)
            await upgrade(user, editable, reaction)
        else:
            print("Incorrect info")
            await reaction.message.remove_reaction("✅", reaction.message.author)
    else:
        pass


@client.event
async def on_message(message):
    guild = message.guild
    user = message.author
    if message.content == ".rdb":
        wks.update('A1', 0)
        wks2.update('A1', 1)
        wks2.batch_clear(["A2:A300", "B2:B300", "C2:C300", "D2:D300", "E2:E300", "F2:F300", "G2:G100"])
        category = client.get_channel(974474230710296618)
        for channel in category.text_channels:
            await channel.delete()
    else:
        pass
    if guild != '917536582301532161' and message.content == ".upgrade":
        count = requests.get("https://upgrader.cc/API/?stock")
        if len(count.json()) > 4:
            uCheck = wks2.find(str(user))
            if str(uCheck) == "None":
                print("Creating Upgrade Channel")
                await cust_chan(message)
            else:
                userID = str(wks2.find(str(user))).lstrip("<Cell R").split("C")[0]
                checkComp = str(wks2.acell('F' + str(userID)).value)
                if checkComp == "success":
                    print("ready to QuickUpgrade")
                    await re_upgrade(message)
                else:
                    embed4 = discord.Embed(title="Please use the channel already created for you", color=15158332)
                    await message.channel.send(embed=embed4)
        else:
            await message.channel.send("Unable to Upgrade Right Now, Please Wait For a Restock")
    else:
        pass
    if message.channel.category.id == 974474230710296618 and int(message.author.id) != 974419378974109727:
        print("Checking Progress...")
        await prog_check(message)
    else:
        pass


async def prog_check(message):
    cUser = str(message.author)
    userID = str(wks2.find(cUser)).lstrip("<Cell R").split("C")[0]
    embed1 = discord.Embed(title="Invalid Key, try again", color=15158332)
    if message.channel.category.id == 974474230710296618 and message.author.id != 974419378974109727:
        checkOne = str(wks2.acell('C' + str(userID)).value)
        checkTwo = str(wks2.acell('D' + str(userID)).value)
        checkThree = str(wks2.acell('E' + str(userID)).value)
        if str(checkOne) == "None":
            await collect_key(message, userID)
        else:
            if str(checkTwo) == "None":
                print('Waiting for Username')
                await collect_usern(message, userID)
            else:
                if str(checkThree) == "None":
                    print('Waiting for Password')
                    await collect_upass(message, userID)
                else:
                    await upgrade_conf(message, userID)
                    print("Waiting For Confirmation")


async def collect_key(message, userID):
    embed1 = discord.Embed(title="Invalid Key, try again", color=15158332)
    embed2 = discord.Embed(title="Spotify Username",
                           description=str(message.author) + "\n\nPlease enter your Spotify Username.", color=3066993)
    resp = requests.get("https://upgrader.cc/API/?info=" + str(message.content))
    respP = str(resp.json())
    if "none" in str(respP):
        wks2.update(str('C' + userID), str(message.content))
        print("Key Uploaded")
        await message.channel.send(embed=embed2)
        print('Waiting For Username')
    else:
        await message.channel.send(embed=embed1)


async def collect_usern(message, userID):
    embed3 = discord.Embed(title="Spotify Username",
                           description=str(message.author) + "\n\nPlease enter your Spotify Password.", color=3066993)
    embed4 = discord.Embed(title="Invalid Username, Try Again", color=15158332)
    if " " not in message.content:
        wks2.update(str('D' + userID), str(message.content))
        print("Username Uploaded")
        await message.channel.send(embed=embed3)
    else:
        await message.channel.send(embed=embed4)


async def collect_upass(message, userID):
    embed4 = discord.Embed(title="Invalid Password, Try Again", color=15158332)
    if str(wks2.acell("E" + str(userID)).value) == "None":
        if " " not in message.content:
            wks2.update(str('E' + userID), str(message.content))
            print("Password Uploaded")
            await upgrade_conf(message, userID)
        else:
            await message.channel.send(embed=embed4)
    else:
        await upgrade_conf(message, userID)


async def upgrade_conf(message, userID):
    key = str(wks2.acell("C" + str(userID)).value)
    usern = str(wks2.acell("D" + str(userID)).value)
    passw = str(wks2.acell("E" + str(userID)).value)
    embedq = discord.Embed(title="Upgrade Confirmation",
                           description="If everything is correct react with ✅ , if some is incorrect restart with ❌",
                           color=0x106e9e)
    embedq.add_field(name="Key:", value=key, inline=True)
    embedq.add_field(name="Username:", value=usern, inline=True)
    embedq.add_field(name="Password:", value=passw, inline=True)
    finalC = await message.channel.send(embed=embedq)
    emojis = ['✅', '❌']
    for emoji in emojis:
        await finalC.add_reaction(emoji)


async def upgrade(user, editable, reaction):
    count = requests.get("https://upgrader.cc/API/?stock")
    list = [1, 4, 7, 10]
    code = str(count.json()).split(",")[random.choice(list)].split(":")[1].strip("'").split("'")[1]
    userID = str(wks2.find(str(user))).lstrip("<Cell R").split("C")[0]
    key = str(wks2.acell('C' + str(userID)).value)
    usern = str(wks2.acell('D' + str(userID)).value)
    passw = str(wks2.acell('E' + str(userID)).value)
    upLink = "https://upgrader.cc/API/?upgrade=" + key + "&login=" + usern + "&pwd=" + passw + "&country=" + code
    print(upLink)
    resp = requests.get(upLink)
    if "success" in str(resp.json()):
        wks2.update("F" + userID, "complete")
        embed5 = discord.Embed(title="Upgraded Successfully ️✅",
                               description="If you ever need to reupgrade, simply do '.upgrade' again.", color=3066993)
        embed5.set_footer(text="This channel will automatically delete in 15 seconds.")
        await editable.edit(embed=embed5)
        time.sleep(15)
        ups = str(wks2.acell('G' + str(userID)).value)
        if ups != "None":
            uCount = int(wks2.acell("G" + userID).value) + 1
            wks2.update("G" + userID, uCount)
        else:
            wks2.update("G" + userID, 1)
        await reaction.message.channel.delete()
    print(resp.json())


async def re_upgrade(message):
    channels = message.guild.channels
    guild = message.guild
    user = message.author
    userID = str(wks2.find(str(user))).lstrip("<Cell R").split("C")[0]
    uChan = str(wks2.acell("B" + userID).value)
    if str(uChan) not in str(channels):
        print("Recreating Channel")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True)}
        upChan = await guild.create_text_channel(uChan, overwrites=overwrites,
                                                 category=client.get_channel(974474230710296618))
        key = str(wks2.acell("C" + str(userID)).value)
        usern = str(wks2.acell("D" + str(userID)).value)
        passw = str(wks2.acell("E" + str(userID)).value)
        embedq = discord.Embed(title="Re-Upgrade Upgrade Confirmation",
                               description="If everything is still correct react with ✅ , if some is incorrect restart with ❌",
                               color=0x106e9e)
        embedq.add_field(name="Key:", value=key, inline=True)
        embedq.add_field(name="Username:", value=usern, inline=True)
        embedq.add_field(name="Password:", value=passw, inline=True)
        finalC = await upChan.send(user.mention, embed=embedq)
        emojis = ['✅', '❌']
        for emoji in emojis:
            await finalC.add_reaction(emoji)
    else:
        print("Channel already exists")
        embed4 = discord.Embed(title="Please use the channel already created for you", color=15158332)
        await message.channel.send(embed=embed4)



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
    upChan = await guild.create_text_channel("Upgrade - " + str(tail), overwrites=overwrites,
                                             category=client.get_channel(974474230710296618))
    embed2 = discord.Embed(title="Spotify Upgrader", description=str(
        member) + ", This Channel is where you will access your spotify premium, To begin please send your key you purchased",
                           color=3066993)
    await upChan.send(member.mention, embed=embed2)
    wks2 = sh.worksheet("LogsTest")
    rowC = wks2.acell('A1').value
    rLog = int(rowC) + 1
    wks2.update('A1', rLog)
    uRow = "A" + str(wks2.acell('A1').value)
    cRow = "B" + str(wks2.acell('A1').value)
    wks2.update(uRow, str(member))
    wks2.update(cRow, str(upChan))


client.run('OTc0NDE5Mzc4OTc0MTA5NzI3.GpGcfO.kvJpr9bXD50b9I9QOcIlNzojurjwQU5KhICCLc')

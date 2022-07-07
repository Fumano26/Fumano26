import discord

def add(name):
    if not name in get_names():
        f = open("banlist.txt","a",encoding="utf-8")
        f.write(name+"\n")
        f.close()
        return name+" is now banned."
    else:
        return name+" is already banned."

def change(text):
    f = open("banlist.txt","w",encoding="utf-8")
    f.write(text)
    f.close()

def get_names():
    f = open("banlist.txt","r",encoding="utf-8")
    players = f.read().split("\n")[:-1]
    return players

def listed_str(players):
    text = ""
    texte = []
    for player in players:
        text += player+"\n"
        if len(text) > 1950:
           texte += [text]
           text = ""
    texte += [text]
    return texte

def search(name):
    banned = False
    for player in get_names():
        if name == player:
            banned = True
    return banned

def player(name):
    banned = False
    for player in get_names():
        if name == player:
            banned = True
    if banned:
        return name+" -banned"
    else:
        return name+" -not banned"

def check_lobby(text):
    output = ""
    names = text.replace("\r","").split("\n")
    lobby_join = [" a rejoint le salon"," joined the lobby"," se ha unido a la sala."]
    banned_names = []
    unbanned_names = []
    for name in names:
        for language in lobby_join:
            if language in name:
                name = name.replace(language,"")
                if  name not in banned_names and name not in unbanned_names:
                    is_banned = search(name)
                    if is_banned:
                        banned_names += [name]
                    else:
                        unbanned_names += [name]
                    #output += f"{search(name)}\n"
    output = "Not Banned: "
    for p in unbanned_names:
        output += f"\n{p}"
    output += "\n\nBanned: "
    for p in banned_names:
        output += f"\n{p}"
    if len(banned_names) == 0:
        output += "\n--no one--"
    return output
    #if output != "":
        #return output
    #else:
        #return "no players located in your message, your language might still not be registered or no names found."
def delete(name):
    i = 0
    is_there = False
    new_text = ""
    for player in get_names():
        if player != name:
            new_text += f"{player}\n"
        else:
            is_there = True
    change(new_text)

    if is_there:
        return name+" is now unbanned."
    else:
        return name+" was not in list."

    


class MyClient(discord.Client):
    async def on_ready(self):
        print("Bot active ...")
    
    async def on_message(self, message):
        if message.guild.id == 891449487074136154:
            banlist_channel = client.get_channel(891457543572967424)
            bannlist_bot = client.get_channel(891449566149349397)
            bannlist_configure = client.get_channel(891449487074136157)
            #chaotic server
        elif message.guild.id == 868934035257315398:
            banlist_channel = client.get_channel(891744863719141406)
            bannlist_bot = client.get_channel(891744255872213033)
            bannlist_configure = client.get_channel(891744135172735022)
        bot_commands = "commands:\n!player 'name'  - looks if the 'name' is at the list\n!lobby 'text'  - paste your lobby text in and see if someone is banned at the list"
        configure_commands = "commands:\n!add 'name'  - adds an player to the list\n!del 'name'  - deletes a player from the list\n!update  - just updates the visualisation of list"

        if message.author == client.user:
            return

        elif message.content.startswith("!player ") and message.channel == bannlist_bot:
            name = message.content.replace("!player ","")
            await message.channel.send(player(name))

        elif message.content.startswith("!lobby ") and message.channel == bannlist_bot:
            text = message.content.replace("!lobby ","")
            await message.channel.send(check_lobby(text))

        elif message.content.startswith("!add ") and message.channel == bannlist_configure:
            text = message.content.replace("!add ","")
            answer = add(text)
            await bannlist_configure.send(answer)
            if not "is already banned." in answer:
                await banlist_channel.purge(limit=30)
                texte = listed_str(get_names())
                for text in texte:
                    await banlist_channel.send(text)

        elif message.content.startswith("!del ") and message.channel == bannlist_configure:
            text = message.content.replace("!del ","")
            msg = delete(text)
            await bannlist_configure.send(msg)
            if not "was not in list." in msg:
                await banlist_channel.purge(limit=30)
                texte = listed_str(get_names())
                for text in texte:
                    await banlist_channel.send(text)

        elif message.content == "!update" and message.channel == bannlist_configure:
            await banlist_channel.purge(limit=30)
            texte = listed_str(get_names())
            for text in texte:
                await banlist_channel.send(text)

        elif message.content == "!help" and message.channel == bannlist_bot:
            await bannlist_bot.send(bot_commands)

        elif message.content == "!help" and message.channel == bannlist_configure:
            await bannlist_configure.send(configure_commands)
        else:
            if message.channel == bannlist_bot:
                await bannlist_bot.send(f"@{message.author} for commands type !help")
            if message.channel == bannlist_configure:
                await bannlist_configure.send(f"@{message.author} for commands type !help")

client = MyClient()
print("Starting Client")
client.run("ODkxNDQ4MDUxOTUxMTA0MDUx.YU-fsQ.Ac1r3namJvSRMx-sC-DUfq0K1NE")

#path = cd /media/disk/Marc/discord bot
#path = nohup ./banlist.py &
##hilfslink = https://forum-raspberrypi.de/forum/thread/1227-anwendung-ueber-ssh-in-den-hintergrund/
#kill = kill $(ps aux | grep python | grep banlist.py | awk '{print $2}')
#file = nohup ./LogServer.py &
#kill $(ps aux | grep python | grep LogServer.py | awk '{print $2}')

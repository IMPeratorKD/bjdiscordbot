import discord
import random

random.seed()

class manager:
    def __init__(self):
        self.cards = []
        self.croupier_cards = []
        for i in range(2):
            self.cards.append(random.randint(2, 11))
            self.croupier_cards.append(random.randint(2, 11))

    def player_card(self):
        self.cards.append(random.randint(2, 11))
        if sum(self.cards) > 21:
            for index in range(len(self.cards)):
                if self.cards[index] == 11:
                    self.cards[index] = 1
                    return True
            return False
        return True

    def croupier_card(self):
        while sum(self.croupier_cards) < 17 or sum(self.croupier_cards) < sum(self.cards):
            self.croupier_cards.append(random.randint(2, 11))
            if sum(self.croupier_cards) > 21:
                for index in range(len(self.croupier_cards)):
                    if self.croupier_cards[index] == 11:
                        self.croupier_cards[index] = 1
                        break
                if sum(self.croupier_cards) > 21:
                    return False
        return True

    def winner(self):
        if sum(self.cards) > sum(self.croupier_cards):
            return 1
        if sum(self.cards) < sum(self.croupier_cards):
            return 2
        if sum(self.cards) == sum(self.croupier_cards):
            return 3

class MyClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(activity=discord.Game(name="!infobj", type=3))
        print("bj aktiv")
        self.name = None
        self.aktiv = True
    async def on_message(self, message):
        if message.content == "!infobj":
            infoEmbed = discord.Embed(
                title = "crouPIer",
                color = discord.Color.green()
            )
            infoEmbed.add_field(name="Version", value="1.0", inline=True)
            infoEmbed.add_field(name="Regeln", value="!rulesbj", inline=True)
            infoEmbed.add_field(name="Start", value="!bj", inline=True)
            infoEmbed.add_field(name="!card", value="Gibt dir eine weitere Karte.", inline=True)
            infoEmbed.add_field(name="!pass", value="Du erhälst keine weiteren Karten, Croupier ist am Zug und danach wird der Sieger ermittelt.")
            await message.channel.send(embed = infoEmbed)
        if message.content == "!rulesbj":
            rulesEmbed = discord.Embed(
                title = "Regeln",
                color = discord.Color.green()
            )
            rulesEmbed.add_field(name="Link zur Regeln", value="https: // www.blackjackapprenticeship.com / how - to - play - blackjack /", inline=True) #keine Haftung
            rulesEmbed.add_field(name="Zusatz", value="Die aktuelle Version beinhaltet keine Wetten und lässt nur ein Spieler zu. Die Karten(bzw. Punkte) werden zufällig ausgegeben.", inline=True)
            rulesEmbed.add_field(name="-", value="Bei weiteren Fragen oder Unklarheiten kann man meinen Entwickler, IMPerator, anschreiben.", inline=True)
            await message.channel.send(embed=rulesEmbed)


        if message.content == "!bj":
            self.bj = manager()
            await message.channel.send("Black Jack wird von "+str(message.author)+" gespielt.")
            await message.channel.send("Deine Karten: "+str(self.bj.cards[0])+","+str(self.bj.cards[1]))
            await message.channel.send("Croupier Karte: "+str(self.bj.croupier_cards[0]))
            self.aktiv, self.name = True, str(message.author)
        if self.aktiv and str(message.author) == self.name:
            if message.content == "!card":
                if not self.bj.player_card():
                    await message.channel.send("Croupier gewinnt, mehr als 21 Punkte. Die Karte: "+str(self.bj.cards[-1]))
                    self.aktiv, self.name = False, None
                    return
                await message.channel.send("Neue Karte: "+str(self.bj.cards[-1]))
            if message.content == "!pass":
                if not self.bj.croupier_card():
                    await message.channel.send("Du gewinnst, Croupier hat über 21 Punkte.")
                    self.aktiv, self.name = False, True
                    return
                self.winner_bj = self.bj.winner()
                if self.winner_bj == 1:
                    await message.channel.send("Du gewinnst, "+str(sum(self.bj.cards))+" gegen "+str(sum(self.bj.croupier_cards)))
                elif self.winner_bj == 2:
                    await message.channel.send("Croupier gewinnt, "+str(sum(self.bj.croupier_cards))+" gegen "+str(sum(self.bj.cards)))
                elif self.winner_bj == 3:
                    await message.channel.send("Unentschieden, beide haben "+str(sum(self.bj.cards))+" Punkte.")
                self.aktiv, self.name = False, None
                return

client = MyClient()
client.run('')
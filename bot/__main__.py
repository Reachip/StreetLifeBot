"""The main file, directly interpretable by typing the name of the parent-folder"""

import os

import asyncio

import discord
from discord.ext import commands

import ujson

from utils import get_json_file

bot = commands.Bot(command_prefix="!", description="Bot du serveur Street-Life RP.")
bot.remove_command("help")


@bot.event
async def on_reaction_add(reaction, user):
    """ When a reaction is add ... """
    data = await get_json_file(bot)

    if reaction.emoji == "🏴":
        embed = discord.Embed(title="Un message a été signalé :", color=0xb22222)
        embed.add_field(name="Signaleur :", value=user.name)
        embed.add_field(name="Auteur du message :", value=reaction.message.author)
        embed.add_field(name="Contenu :", value=reaction.message.content, inline=False)

        server_id = reaction.message.channel.server.id
        channel_id = reaction.message.channel.id
        message_id = reaction.message.id

        embed.add_field(
            name="Lien direct vers le message :",
            value=f"https://discordapp.com/channels/{server_id}/{channel_id}/{message_id}",
        )

        await bot.send_message(
            discord.Object(id=data["complaint_channel"]), "@here", embed=embed
        )


@bot.command(pass_context=True)
async def news(ctx, channel, extern_link, *subject):
    """ Send a news """
    data = await get_json_file(bot)
    user_roles = [role.name for role in ctx.message.author.roles]

    if "Modérateurs" or "Leader staff" or "Développeurs" in user_roles:
        embed = discord.Embed(title="INFORMATIONS :", color=0x0375b4)
        embed.add_field(name=" ".join(subject), value=extern_link)
        embed.set_image(
            url="http://street-life-rp.tk/discord/img/assets/infos_image.jpeg"
        )

        if channel == "IG":
            channel_where_msg = data["ig_infos_channel"]

        elif channel == "OCC":
            channel_where_msg = data["ooc_infos_channel"]

        else:
            channel_where_msg = data["ooc_infos_channel"]

        await bot.send_message(
            discord.Object(id=channel_where_msg), "@here", embed=embed
        )

    else:
        await bot.say("Vous n'avez pas le rôle adéquate pour pouvoir poster une news.")


@bot.command(pass_context=True)
async def sondage(ctx, waiting_time, *subject):
    """ Create a poll with a given "subject" """

    data = await get_json_file(bot)
    user_roles = [role.name for role in ctx.message.author.roles]

    if "Modérateurs" or "Leader staff" or "Développeurs" in user_roles:
        embed = discord.Embed(
            title="SONDAGE :", description=" ".join(subject), color=0x5cdb95
        )

        embed.set_author(
            name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url
        )
        embed.set_image(
            url="http://street-life-rp.tk/discord/img/assets/poll_image.jpg"
        )
        poll_message = await bot.send_message(
            discord.Object(id=data["poll_channel"]), embed=embed
        )

        for emoji in ("👍", "👎"):
            await bot.add_reaction(poll_message, emoji)

        await bot.send_message(
            discord.Object(id=data["poll_channel"]),
            f"Les statistiques de ce sondage seront visibles dans {waiting_time} minutes. @here",
        )

        await asyncio.sleep(int(waiting_time) * 60)

        poll = await bot.get_message(
            discord.Object(id=data["poll_channel"]), poll_message.id
        )

        poll_reaction = [reaction.count for reaction in poll.reactions]

        positive_share = poll_reaction[0] / sum(poll_reaction) * 100  # Percentage
        negatif_share = poll_reaction[1] / sum(poll_reaction) * 100  # Percentage

        await bot.send_message(
            discord.Object(id=data["poll_channel"]),
            f"{int(positive_share)} % sont pour, {int(negatif_share)} % sont contre.",
        )

    else:
        await bot.say(
            "Vous n'avez pas le rôle adéquate pour pouvoir poster un sondage."
        )


@bot.command(pass_context=True)
async def cmd(ctx):
    """ Equivalent of the native command !help but with a embed. """

    embed = discord.Embed(
        title="Commandes de Street Life Bot :",
        description="Contacter l'équipe de développement pour la moindre suggestion.",
        color=0xedf5e1,
    )
    embed.add_field(
        name="!social",
        value="Donne les liens vers les plateformes externes liées à Street Life Rôle Play.",
    )

    embed.add_field(
        name="!sondage [temps d'attente (en minute)] [question]",
        value="Créer un sondage.",
    )

    embed.add_field(
        name="!news [OOC ou IG] [lien externe] [description]",
        value="Créer une news dans la partie associée à cette dernière.",
    )

    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def social(ctx):
    """ Return a embed with the social networks of the community. """

    embed = discord.Embed(
        title="Réseaux sociaux du serveur",
        description="L'inscription est obligatoire sur le forum.",
        color=0x907163,
    )

    embed.add_field(name="Lien vers le forum", value="http://www.street-life-rp.net")
    embed.add_field(
        name="Invitation vers le serveur Discord", value="https://discord.gg/ADFcXwz"
    )

    embed.add_field(
        name="Organisation github pour les projets de développement informatique",
        value="https://github.com/StreetLifeRP",
    )

    await bot.send_message(ctx.message.channel, embed=embed)


bot.run(os.environ.get("TOKEN"))

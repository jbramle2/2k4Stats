import pytz
import queries as q
import discord
from discord.ext import commands
from table2ascii import table2ascii, Alignment, PresetStyle
from itertools import groupby
from operator import itemgetter

######################################################
with open('discord_token.txt', 'r') as t:
    discordtoken = t.read()

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    test_guilds=[482012169911664640],
    sync_commands_debug=True,
    intents=intents
)


##########################
# Generate Embed for Last Commands
##########################
async def gen_embed(back):
    match_num = q.get_match_num(back)
    match_info = q.get_match_info(match_num)

    # Retrieves map and server
    map_name = match_info[0][3]
    server_name = match_info[0][1]

    # Retrieves Date
    # ! MAKE GOOD
    date = match_info[0][4]

    print(date)
    print(type(date))

    dt_utc = pytz.utc.localize(date)

    est = pytz.timezone('US/Eastern')

    eastern_time = dt_utc.astimezone(est)

    print(eastern_time)

    # Retrieves team scores
    red_score = match_info[0][8]
    blue_score = match_info[0][9]

    # Checks for game to report correctly
    if red_score + blue_score < 10:
        print("NO TEAM SCORE")
        await interaction.followup.send("NO REPORTED SCORE")

    #####
    ### Retrieve player info
    #####

    # Sorts players into red and blue teams
    match_info_sorted = sorted(match_info, key=itemgetter(7))
    grouped_data = {k: list(v) for k, v in groupby(match_info_sorted, key=itemgetter(7))}

    red_team = grouped_data.get(0, [])
    blue_team = grouped_data.get(1, [])

    # Sort the lists by PPR
    red_team = sorted(red_team, key=lambda x: x[21], reverse=True)
    blue_team = sorted(blue_team, key=lambda x: x[21], reverse=True)

    # Create a list of just player names
    red_players = [item[6] for item in red_team]
    blue_players = [item[6] for item in blue_team]

    # Truncate player names to 11 characters
    red_players = [item[:11] for item in red_players]
    blue_players = [item[:11] for item in blue_players]

    print(red_players)
    print(blue_players)

    red_output = table2ascii(
        header=["Player", "K", "D", "DMG", "PPR"],
        body=[[str(red_players[0]), str(red_team[0][14]), str(red_team[0][16]), str(red_team[0][13]),
               str(round(red_team[0][21], 2))],
              [str(red_players[1]), str(red_team[1][14]), str(red_team[1][16]), str(red_team[1][13]),
               str(round(red_team[1][21], 2))],
              [str(red_players[2]), str(red_team[2][14]), str(red_team[2][16]), str(red_team[2][13]),
               str(round(red_team[2][21], 2))],
              [str(red_players[3]), str(red_team[3][14]), str(red_team[3][16]), str(red_team[3][13]),
               str(round(red_team[3][21], 2))]],
        style=PresetStyle.double_compact,
        cell_padding=0,
        alignments=Alignment.LEFT,
    )

    blue_output = table2ascii(
        header=["Player", "K", "D", "DMG", "PPR"],
        body=[[str(blue_players[0]), str(blue_team[0][14]), str(blue_team[0][16]), str(blue_team[0][13]),
               str(round(blue_team[0][21], 2))],
              [str(blue_players[1]), str(blue_team[1][14]), str(blue_team[1][16]), str(blue_team[1][13]),
               str(round(blue_team[1][21], 2))],
              [str(blue_players[2]), str(blue_team[2][14]), str(blue_team[2][16]), str(blue_team[2][13]),
               str(round(blue_team[2][21], 2))],
              [str(blue_players[3]), str(blue_team[3][14]), str(blue_team[3][16]), str(blue_team[3][13]),
               str(round(blue_team[3][21], 2))]],
        style=PresetStyle.double_compact,
        cell_padding=0,
        alignments=Alignment.LEFT,
    )
    embed = discord.Embed(title="Latest Match: " + str(match_num),
                          url="https://metrics.alde.dev/d/cdom6f94bsk5cf/match-stats?orgId=2&var-MatchID="
                              + str(match_num),
                          description="Date: " + str(date) + "\n Map: " + str(map_name))

    embed.add_field(name=":red_square: Red Score: " + str(red_score),
                    value="```" + red_output + "```",
                    inline=True)

    embed.add_field(name=":blue_square: Blue Score: " + str(blue_score),
                    value="```" + blue_output + "```",
                    inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/482012169911664642/1252186601858269184/"
                        "transparent_long.png?"
                        "ex=66714d26&is=666ffba6&hm=45cb3eecc2062d702f276680835c7dd2b39e073146c026e170a18994386c4233&")
    embed.set_footer(text=str(server_name))

    return embed


##########################
# Last Slash Command
##########################
@bot.tree.command(name="last", description="last", guild=discord.Object(id=482012169911664640))
async def last(interaction: discord.Interaction):
    # Waits for slow query
    await interaction.response.defer()

    # How far back to go in the matches. Defaults to 0.
    embed = await gen_embed(0)

    view = MyView()

    await interaction.followup.send(embed=embed, view=view)


##########################
# Generate Button View
##########################
class MyView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    # Resets embed to default state (most previous match)
    @discord.ui.button(label="⏮", style=discord.ButtonStyle.primary)
    async def reset(self, interaction, button):

        button.label = "⏮"

        embed = await gen_embed(0)

        view = MyView()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="(1) ⏩", style=discord.ButtonStyle.primary)
    async def back(self, interaction, button):

        # Current page based on the number in the button label
        number = button.label
        number = number.replace("(", "")
        number = number.replace(")", "")
        number = number.replace(" ", "")
        number = number.replace("⏩", "")

        button.label = "(" + str(int(number) + 1) + ") ⏩"

        embed = await gen_embed(number)

        await interaction.response.edit_message(embed=embed, view=self)

##########################
# Get player stats
##########################

@bot.tree.command(name="power", description="power", guild=discord.Object(id=482012169911664640))
async def power(interaction: discord.Interaction, player: str):

    await interaction.response.defer()

    player_stats = q.get_player_stats(player)

    player_avg_10 = q.get_player_avg_10(player)

    avg_kpr_10 = player_avg_10[4] / player_avg_10[12]
    avg_kdr_10 = player_avg_10[4] / player_avg_10[6]

    embed = discord.Embed(
        title="Power for " + str(player_stats[0]),
        description="**Latest:**  [" + str(player_avg_10[10]) +
                    "](https://metrics.alde.dev/d/cdom6f94bsk5cf/match-stats?orgId=2&var-MatchID=" +
                    str(player_avg_10[11]) + ")" +
                    "\n**Total matches: **" + str(player_stats[4]) +
                    "\n**W/L Ratio: **" + str(round(player_avg_10[7],2)) + " (" + str(round(player_stats[3],2)) + ")",
        colour=0xF0C43F,
    )
    embed.add_field(name="PPR", value=str(round(player_avg_10[8],2)) +
                                      " (" + str(round(player_stats[2],2)) + ")", inline=True)
    embed.add_field(name="KPR", value=str(round(avg_kpr_10,2)) +
                                      " (" + str(round(player_stats[5],2)) + ")", inline=True)
    embed.add_field(name="KDR", value=str(round(avg_kdr_10,2)) +
                                      " (" + str(round(player_stats[6],2)) + ")", inline=True)
    embed.add_field(name="LG_Acc", value= str(round(player_avg_10[13],2)) +
                                      " (" + str(round(player_stats[7],2)) + ")", inline=True)

    embed.set_footer(text= "*Last 10 maps (all time)")
    await interaction.followup.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}!')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=482012169911664640))
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


bot.run(str(discordtoken))

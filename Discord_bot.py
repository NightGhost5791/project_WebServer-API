import discord 
from discord_components import DiscordComponents, ComponentsBot, Button
import discord.ext.commands as commands
from discord_components.interaction import Interaction

import random

client = commands.Bot(command_prefix="!")
DiscordComponents(client)

player1 = ""
player2 = ""
turn = ""
GameOver = True

board = []

WinningConditions = [[0, 1, 2],
                     [3, 4, 5],
                     [6, 7, 8],
                     [0, 3, 6],
                     [1, 4, 7],
                     [2, 5, 8],
                     [0, 4, 8],
                     [2, 4, 6]]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count, player1, player2, turn, GameOver

    if GameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:",":white_large_square:",":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        GameOver = False
        count = 0

        player1 = p1
        player2 = p2

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("<@" + str(player1.id) + "> Ходит первым")
        elif num == 2:
            turn = player2
            await ctx.send("<@" + str(player2.id) + "> Ходит первым")

        await ctx.send(components = [
            [Button(label="1"), Button(label="2"), Button(label="3")],
            [Button(label="4"), Button(label="5"), Button(label="6")],
            [Button(label="7"), Button(label="8"), Button(label="9")]]) 
    else:
        await ctx.send("Партия ещё не закончилась")

@client.event
async def on_button_click(interaction: Interaction):
    #print(interaction.component.label)
    await interaction.send(content=interaction.component.label, ephemeral=False)
    client.loop.create_task(place(interaction, int(interaction.component.label)))

@client.command()
async def place(ctx, pos: int):
    global turn, player1, player2, board, count, GameOver

    if not GameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(WinningConditions, mark)
                print(count)
                if GameOver == True:
                    await ctx.send(mark + " Побеждают!")
                elif count >= 9:
                    GameOver = True
                    await ctx.send("Ничья!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Выберите пустую клетку")
        else:
            await ctx.send("Это не ваш ход!")
    else:
        await ctx.send("Для начала новой игры введите: !tictactoe Игрок1 Игрок2")


def checkWinner(WinningConditions, mark):
    global GameOver
    for condition in WinningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            GameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Укажите два игрока для начала игры")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Укажите два игрока для начала игры")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Выберите клетку")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Введите целое число")

client.run("TOKEN")


import discord 

from discord_components import DiscordComponents, ComponentsBot, Button
import discord.ext.commands as commands
import random 
# Импортируемые библиотеки

client = commands.Bot(command_prefix="!") # Префикс для активации команд
DiscordComponents(client)

player1 = ""
player2 = ""
turn = ""
GameOver = True
board = []
# Переменные

WinningConditions = [[0, 1, 2],
                     [3, 4, 5],
                     [6, 7, 8],
                     [0, 3, 6],
                     [1, 4, 7],
                     [2, 5, 8],
                     [0, 4, 8],
                     [2, 4, 6]]
# Комбинации победы для игры "Крестики-Нолики"

@client.command() # Добавление команды с названием instruction
async def instruction(ctx):
    await ctx.send('1. !tictactoe Игрок1 Игрок2\n Начать играть в "Крестики-Нолики"')
    await ctx.send('2. !wordgame Игрок1 Игрок2\n Начать "Игру в слова"')
    # Вывод инструкции по боту в чат

@client.command() # Добавление команды с названием tictactoe для запуска игры "Крестики-Нолики"
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count, player1, player2, turn, GameOver
    # Глобальные переменные 
    
    if GameOver: # Условие окончания игры
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:",":white_large_square:",":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        # Игровое поле
        turn = ""
        GameOver = False
        count = 0
        player1 = p1
        player2 = p2
        line = ""
        # Переменные
        
        emb = discord.Embed() # Создание заставки
        emb.set_image(url = "http://sun9-31.userapi.com/impf/0_pvt3wzfxqDQueaORCb7tbC7xtke8oc3T4JvQ/u8upEVZwQUo.jpg?size=1590x530&quality=95&crop=230,0,1200,400&sign=e088936cf44b66d169316dab5a740c08&type=cover_group")
        await ctx.send(embed = emb) 

        for x in range(len(board)): # Создание игрового поля
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2) # Выбор игрока, который будет ходить первым
        if num == 1:
            turn = player1
            await ctx.send("<@" + str(player1.id) + "> Ходит первым")
        elif num == 2:
            turn = player2
            await ctx.send("<@" + str(player2.id) + "> Ходит первым")

        await ctx.send(components = [
            [Button(label=1), Button(label=2), Button(label=3)],
            [Button(label=4), Button(label=5), Button(label=6)],
            [Button(label=7), Button(label=8), Button(label=9)]]) # Создание кнопок для упрощённого ввода команд
    else:
        await ctx.send("Партия ещё не закончилась") # Ошибка при попытке создания новой партии

@client.event # Событие нажатия на кнопку
async def on_button_click(ctx):  
    await client.loop.create_task(place(ctx, int(ctx.component.label)))
    # Вызов функции при нажатии на кнопку 

@client.command() # Создание функции для замены пустой клетки поля на крестик или нолик
async def place(ctx, pos: int):
    global turn, player1, player2, board, count, GameOver 
    if not GameOver:
        mark = ""

        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"

            elif turn == player2:
                mark = ":o2:"
            # Установка крестика или нолика 

            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1
                
                line = ""
                for x in range(len(board)): # Вывод игрового поля
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(WinningConditions, mark) # Проверка победителя
                if GameOver:
                    await ctx.send(mark + " Побеждают!")
                elif count >= 9: # Условие ничьей
                    GameOver = True
                    await ctx.send("Ничья!")

                # Смена ходов
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


def checkWinner(WinningConditions, mark): # Функция для проверки победителя
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
# Создание функций для реакции на ошибки

@client.command() # Добавление функции wordgame для запуска "Слова из Слов"
async def wordgame(ctx, p1: discord.Member, p2: discord.Member):
    global count, player1, player2, turn, GameOver
    if GameOver:
        turn = ""
        GameOver = False
        count = 0
        player1 = p1
        player2 = p2
        num = random.randint(1, 2) # Выбор игрока, который будет ходить первым
        
        emb = discord.Embed() # Создание заставки
        emb.set_image(url = "http://i.otzovik.com/objects/b/920000/915028.png")
        await ctx.send(embed = emb) 

        if num == 1:
            turn = player1
            await ctx.send("<@" + str(player1.id) + "> Ходит первым")
        elif num == 2:
            turn = player2
            await ctx.send("<@" + str(player2.id) + "> Ходит первым")

    else:
        await ctx.send("Игра ещё не закончилась")

@client.command() # Создание функции для ввода слова
async def word(ctx, wrd):
    global turn, player1, player2, count, GameOver, old_word
    if not GameOver:
        if turn == ctx.author:
            if count >= 1:
                if old_word[-1].lower() != wrd[0].lower(): # Сравнение первой буквы первого слова с последней буквы старого слова
                    await ctx.send('Игра окончена\n---Счёт:' + str(count))
                    GameOver = True

            if not GameOver:
                if turn == player1:
                    await ctx.send(str(player2) + ' Пишет слово на букву ' + wrd[-1].upper())
                    count += 1
                elif turn == player2:
                    await ctx.send(str(player1) + ' Пишет слово на букву ' + wrd[-1].upper())
                    count += 1
                # Подсказка для следующего игрока
                old_word = wrd # Замена старого слова на новое после проверки
                
                # Смена ходов
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
        else:
            await ctx.send("Это не ваш ход!")
    else:
        await ctx.send("Для начала новой игры введите: !wordgame Игрок1 Игрок2")

client.run("OTQ5OTgyMjg4NjQzNDg5ODE0.YiSR8w.011_NreopoTk-_rIARSZhR_k7ro") # Запуск бота по текущему токену 


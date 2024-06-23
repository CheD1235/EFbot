import nextcord
import os
import sys
import asyncio
import time
import json
import requests
import subprocess
import mysql.connector

from mysql.connector import Error
from nextcord import Member
from nextcord import Interaction
from nextcord.ext.commands import has_permissions
from nextcord import FFmpegPCMAudio
from nextcord import utils
from nextcord.ext import commands
from nextcord.utils import get 

bot = commands.Bot(command_prefix="!", help_command=None, intents=nextcord.Intents.all(),)
TOKEN = ''#Токен бота
BADWORDS=["дурак","идиот"]
LINKS =[".ru",".net",".org",".shop",".ру",".рф"]
ServerID=988512774441283634
queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)


bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.idle, activity= nextcord.Game("Написание диплома"))
    print("----------------")
    print("|-Аккаунт бота-|")
    print("----------------")
    print("----------------")
    print(f"|Имя бота:{bot.user.name}|")
    print("----------------")
    print("------------------------------")
    print(f"|ID бота: {bot.user.id}|")
    print("------------------------------")
    print("--------------------------------------------------------------------------------------")
    print(f"|Токен бота: {TOKEN}|")
    print("--------------------------------------------------------------------------------------")
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as file:
            file.write('{}')
            file.close()

        for guild in bot.guilds:
            for member in guild.members:
                with open('users.json', 'r') as file:
                    data = json.load(file)
                    file.close
                with open('users.json','w') as file:
                    data[str(member.id)]={
                        "WARNS":0,
                        "CAPS":0
                    }

                    json.dump(data,file, indent=4)
                    file.close()


@bot.event # Заход на сервер
async def on_member_join(member):
    emb = nextcord.Embed(
            description=f"Приветствую тебя на сервере! Если хочешь узнать на что я способен введи /помощь."
        )
    await member.send(embed=emb)

    channel = get(member.guild.channels,id=)#id КАНАЛА 
    embed = nextcord.Embed(
            title="Пришедшие",
            description=f"{member.mention}, Добро пожаловать!",
            color=0x0000FF
        )
    embed.set_image(url="https://media1.tenor.com/m/XL6emacfP5oAAAAd/hello-russian.gif")
    await channel.send(embed=embed)

@bot.event #Добавление реакции
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    channel = reaction.message.channel
    await channel.send(user.mention + ' Добавлена реакция: ' + reaction.emoji)


@bot.event #Удаление реакции
async def on_reaction_remove(reaction, user):
    if user == bot.user:
        return
    channel = reaction.message.channel
    await channel.send(user.mention + ' Удалена реакция: ' + reaction.emoji)


@bot.slash_command(name="помощь", description="Список доступных команд",guild_ids = [ServerID])
async def help(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="Навигация по командам")
    embed.add_field(name = '/очистка',value='Очистка чата')
    embed.add_field(name = '/кик',value='Кикнуть пользователя')
    embed.add_field(name = '/бан',value='Забанить пользователя')
    embed.add_field(name = '/unwarn',value='Снять 1 предупреждение')
    embed.add_field(name = '/Привет',value='Приветствие с ботом')
    embed.add_field(name = '/Пока',value='Прощание с ботом')
    embed.add_field(name = '/Выбор',value='Знаешь в чем наше отличие? Ты тот кто делает выбор, а я тот кто его дает.')
    embed.add_field(name = '/Сохранение',value='Сохранить любимые сообщения в боте')
    embed.add_field(name = '/Загрузка',value='Выгрузить все сообщения из бота')
    embed.add_field(name = '!warn',value='Выдать предупреждение')
    embed.add_field(name = '!clear_warns',value='Убрать все предупреждения у пользователя')
    embed.add_field(name = '!join',value='Присоединение бота к голосовому чату')
    embed.add_field(name = '!leave',value='Заставить бота покинуть голосовой чат')
    embed.add_field(name = '!pause',value='Поставить музыку на паузу')
    embed.add_field(name = '!resume',value='Убрать музыку с паузы')
    embed.add_field(name = '!stop',value='Полностью выключает музыку')
    embed.add_field(name = '!play',value='Проиграть какую-то музыку')
    embed.add_field(name = '!queue',value='Поставить песню в очередь')
    embed.color = 0xF1C232
    await interaction.response.send_message(embed=embed)

    

@bot.event # Выход из сервера
async def on_member_remove(member):
    try:
        emb = nextcord.Embed(
                description=f"Прощай, надеюсь увидимся вновь!"
            )
        await member.send(embed=emb)
    except nextcord.Forbidden:
        pass 
    
    channel = get(member.guild.channels,id=)#id КАНАЛА 
    embed = nextcord.Embed(
            title="Ушедший",
            description=f"{member.mention}, покинул(а), наши ряды...(",
            color=0x0000FF
        )
    embed.set_image(url="https://media1.tenor.com/m/O4rBMHAruSwAAAAd/грустный-кот.gif")
    await channel.send(embed=embed)

@bot.event # Анализ на плохие слова или сыллки
async def on_message(message):

    if message.author == bot.user:
        return
    if('привет') in message.content.lower():
        emoji = '✋'
        await message.add_reaction(emoji)
    if('пока') in message.content.lower():
        emoji = '✊'
        await message.add_reaction(emoji)

    WARN = BADWORDS + LINKS

    for i in range(0, len(WARN)):
        if WARN[i] in message.content.lower():
            await message.delete()
            with open('users.json', 'r') as file:
                data = json.load(file)
                file.close()

            with open('users.json', 'w') as file:
                data[str(message.author.id)]['WARNS'] += 1
                json.dump(data, file, indent=4)

                file.close()

            emb = nextcord.Embed(
                title="Нарушение",
                description=f"*Раннее, у нарушителя уже было {data[str(message.author.id)]['WARNS'] - 1} нарушений после 5 - бан!!!*",
                timestamp=message.created_at,
                color=0xFF0000
            )

            emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
            emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="Ругательства/ссылки", inline=True)

            await get(message.guild.text_channels, id= ).send(embed = emb) #id КАНАЛА 

            if data[str(message.author.id)]['WARNS'] >= 5:
                await message.author.ban(reason = "Вы привыси кол-во нарушений")

    if message.content.isupper():
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()

        with open('users.json', 'w') as file:
            await message.delete()
            data[str(message.author.id)]["CAPS"] += 1
            json.dump(data, file, indent=4)

        if data[str(message.author.id)]["CAPS"] >= 3:

            with open('users.json', 'w') as file: 
                data[str(message.author.id)]["CAPS"] = 0
                data[str(message.author.id)]["WARNS"] += 1

                json.dump(data, file, indent=4)
                file.close()

            emb = nextcord.Embed(
                title="Нарушение",
                description=f"*Раннее, у нарушителя уже было {data[str(message.author.id)]['WARNS'] - 1} нарушений после 5 - бан!!!*",
                timestamp=message.created_at,
                color=0xFF0000
            )

            emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
            emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="КАПС", inline=True)
            await get(message.guild.text_channels, id=).send(embed=emb)#id КАНАЛА 

            if data[str(message.author.id)]['WARNS'] >= 5:
                await message.author.ban(reason = "Вы привысили кол-во нарушений")
    await bot.process_commands(message)

@bot.command() # Команда предупреждения
@commands.has_permissions(manage_channels=True, administrator=True)
async def warn(ctx, member: nextcord.Member, reason:str):
    if reason.lower() == "ругательства" or reason.lower() == "сыллки":
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()

        with open('users.json','w') as file:
            data[str(member.id)]['WARNS']+=1
            json.dump(data, file, indent=4)

            file.close

        emb = nextcord.Embed(
            title="Нарушения",
            description=f"*Раннее, у пользователя было уже {data[str(member.id)]['WARNS']-1} нарушений, когда их будет 7, пользователя забанят.",
            timestamp=ctx.message.created_at,
            color=0xFF0000
            )
            

        emb.add_field(name="Канал:", value='Не определен', inline=True)
        emb.add_field(name="Нарушитель:", value=member.mention, inline=True)
        emb.add_field(name="Тип нарушения:", value="Ругательства/ссылки", inline=True)

        await get(ctx.guild.text_channels,id=).send(embed=emb)#id КАНАЛА 
        if data[str(member.id)]['WARNS']>=7:
            await member.ban(reason="Первышано кол-во нарушений")

        await ctx.message.reply(embed=nextcord.Embed(
            title="Успешно",
            description="Предупреждение выдано",
            timestamp=ctx.message.created_at,
            color=0xFF0000
        ))

    elif reason.lower() == "caps":
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()


        with open('users.json','w') as file:
            data[str(member.id)]["CAPS"] = 0
            data[str(member.id)]["WARNS"]+=1

            json.dump(data, file, indent=4)
            file.close()

        emb = nextcord.Embed(
            title="Нарушения",
            description=f"*Раннее, у пользователя было уже {data[str(member.id)]['WARNS']-1} нарушений, когда их будет 7, пользователя забанят.",
            timestamp=ctx.message.created_at,
            color=0xFF0000
            )
            

        emb.add_field(name="Канал:", value='Не определен', inline=True)
        emb.add_field(name="Нарушитель:", value=member.mention, inline=True)
        emb.add_field(name="Тип нарушения:", value="КАПС", inline=True)

        await get(ctx.guild.text_channels,id=1246462313259597916).send(embed=emb)
        if data[str(member.id)]['WARNS']>=7:
            await member.ban(reason="Первышано кол-во нарушений")

        await ctx.message.reply(embed=nextcord.Embed(
            title="Успешно",
            description="Предупреждение выдано",
            timestamp=ctx.message.created_at,
            color=0xFF0000
        ))

    else:
        await ctx.message.reply(embed=nextcord.Embed(
        title="Ошибка",
        description="Неправильная причина",
        timestamp=ctx.message.created_at,
        color=0xFF0000 
        ))

@warn.error #Команда ошибки
async def error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=nextcord.Embed(
            title="Ошибка",
            description="*Использование: !warn (@Участник) (Причина)*",
            timestamp=ctx.message.created_at,
            color=0xFFFF00
        ))

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=nextcord.Embed(
            title="Ошибка",
            description=f"*У вас {ctx.author.mention} недостаточно прав!*",
            timestamp=ctx.message.created_at,
            color=0xFFFF00   
        ))

@bot.slash_command(name="unwarn", description="Снять 1 предупреждение", guild_ids=[ServerID])
@has_permissions(manage_channels=True, administrator=True)
async def unwarn(interaction: nextcord.Interaction, member: nextcord.Member):
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()

    with open('users.json', 'w') as file:
        data[str(member.id)]['WARNS']-=1
        json.dump(data, file, indent=4)
        file.close()
    
    await interaction.response.send_message(f"1 предупреждение снято с {member.mention}.", delete_after = 5)


@bot.command()#Команда снятия всех предупреждений
@commands.has_permissions(administrator=True)
async def clear_warns(ctx, member: nextcord.Member):
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()

    with open('users.json', 'w') as file:
        data[str(member.id)]['WARNS'] = 0
        json.dump(data, file, indent=4)

        file.close()
        await ctx.message.reply(embed=nextcord.Embed(
            title="Успешно",
            description="Все предупреждения сняты",
            timestamp=ctx.message.created_at,
            color=0xFF0000
        ))

@bot.slash_command(name='привет', description='Приветствие от бота',guild_ids=[ServerID]) #команда Привет
async def hello(interaction: Interaction):
    await interaction.response.send_message(f"Привет, меня зовут {bot.user.mention}, рад знакомству.")

@bot.slash_command(name='пока', description='Прощание от бота',guild_ids=[ServerID]) #команда Пока
async def bye(interaction: Interaction):
    await interaction.response.send_message(f"Ох, уже уходишь? Ну тогда приятного дня {interaction.user.mention}!")

@bot.command(pass_context = True)#Присоединение бота к голосовому каналу
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('')
        player = voice.play(source)

    else:
        await ctx.send("Для выполнения этой команды, вы должны быть в голосовом канале.")

@bot.command(pass_context=True)#Покидание бота голосового канала
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Я вышел из голосового канала")
    else:
        await ctx.send("Извините, но в данный момент я не подключен к голосовому каналу.")

@bot.command(pass_context=True)#Остонавливает музыку 
async def pause(ctx):
    voice = nextcord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send('Музыка на паузе')
    else:
        await ctx.send('Музыка уже на паузе')

@bot.command(pass_context=True)#Возобновляет музыку 
async def resume(ctx):
    voice = nextcord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Музыка вновь воспроизводится.")

    else:
        await ctx.send("В данный момент, нету остоновленых песен.")


@bot.command(pass_context=True)#Заканчивает музыку 
async def stop(ctx):
    voice = nextcord.utils.get(bot.voice_clients, guild=ctx.guild)
    await ctx.send("Музыка сброшена")
    voice.stop()

@bot.command(pass_context=True)#Включает другую музыку 
async def play(ctx, arg):  
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))

@bot.command(pass_context=True)#Включает становление песен в очередь 
async def queue(ctx, arg): 
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)

    else:
        queues[guild_id] = [source]

    await ctx.send('Добавлено в очередь')
        
@bot.slash_command(name="кик", description="Выгнать пользователя", guild_ids=[ServerID]) #Кикнуть пользователя с сервера
@has_permissions(kick_members=True, administrator=True)
async def kick(interaction: nextcord.Interaction, member: nextcord.Member, reason=None):
    if member is None:
        await interaction.response.send_message("Пожалуйста, укажите пользователя, которого хотите выгнать.", delete_after=5)
        return

    if member.bot:
        await interaction.response.send_message("Нельзя выгонять ботов.", delete_after=5)
        return

    if member == interaction.user:
        await interaction.response.send_message("Нельзя выгонять себя.", delete_after=5)
        return

    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"Пользователь {member} выгнан(а) с сервера.", delete_after=5)
    except nextcord.errors.Forbidden:
        await interaction.response.send_message("Не удалось выгнать пользователя.Возможно у вас недостаточно прав", delete_after=5)
    
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.reply(embed=nextcord.Embed(
            title="Ошибка",
            description=f"У вас {ctx.author.mention}, недостаточно прав для этой команды",
            color=0xFFFF00
        ))

@bot.slash_command(name="бан", description="Забанить пользователя", guild_ids=[ServerID]) #Забанить пользователя на сервере
@has_permissions(ban_members=True, administrator=True)
async def ban(interaction: nextcord.Interaction, member: nextcord.Member, reason=None):

    if member is None:
        await interaction.response.send_message("Пожалуйста, укажите пользователя, которого хотите забанить.", delete_after=5)
        return

    if member.bot:
        await interaction.response.send_message("Нельзя банить ботов.", delete_after=5)
        return

    if member == interaction.user:
        await interaction.response.send_message("Нельзя банить себя.", delete_after=5)
        return

    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"Пользователь {member} забанен(а) на сервере.", delete_after=5)
    except nextcord.errors.Forbidden:
        await interaction.response.send_message("Не удалось забанить пользователя. Возможно у вас недостаточно прав", delete_after=5)

@bot.slash_command(name="очистка", description="Очистка чата", guild_ids=[ServerID])#Очистить чат
@has_permissions(administrator=True)
async def clear(interaction: nextcord.Interaction, amount=100):
    try:
        amount = int(amount)
    except ValueError:
        await interaction.response.send_message("Неверное значение. Укажите количество сообщений для очистки (число).")
        return
    if amount > 1000:
        await interaction.response.send_message(f"Максимальное количество сообщений для очистки - 1000.")
        return
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"Было удалено {amount} сообщений.", delete_after= 5)


class Vibor(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout= None)
        self.value = None
    
    @nextcord.ui.button(label = "Да", style=nextcord.ButtonStyle.green)
    async def da(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("Понял", ephemeral=False)
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "Нет", style=nextcord.ButtonStyle.danger)
    async def net(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("Не понял", ephemeral=False)
        self.value = False
        self.stop()

@bot.slash_command(name = "выбор", description="Сложный выбор", guild_ids = [ServerID])#Что-то выбрать
async def vib(interaction: Interaction):
    view = Vibor()
    await interaction.response.send_message("Сделай мудрый выбор.", view=view)
    await view.wait()

    if view.value is None:
        return
    
    elif view.value:
        print("Мудро...")
    
    else:
        print("Сильно...")

@bot.slash_command(name="сохранение", description="Сохранение данных", guild_ids=[ServerID])#Сохранить сообщение в бд
async def store_info(interaction: Interaction, message:str):
    guild = interaction.guild.id
    
    try:
        connection = mysql.connector.connect(host='localhost', 
                                             database = 'EFBot', 
                                             user = 'root', 
                                             password = 'root')

        table = "DB_" + str(guild)
        
        mySql_Create_Table_Query = """CREATE TABLE IF NOT EXISTS """+ table + """ (
        id int(11) NOT NULL AUTO_INCREMENT,
        User varchar(250) NOT NULL,
        Message varchar(5000) NOT NULL,
        PRIMARY KEY(id)) """

        cursor = connection.cursor()
        cursor.execute(mySql_Create_Table_Query)
        print("Таблица ("+ table +") успешно создана")
    
    except mysql.connector.Error as error:
        print("Не удалось создать таблицу в MySql: {}".format(error))

    finally:
        if connection.is_connected:

            mySql_Insert_Row_Query = "INSERT INTO "+ table +" (User, Message) VALUES (%s,%s)"
            mySql_Insert_Row_values = (str(interaction.user), message)

            cursor.execute(mySql_Insert_Row_Query, mySql_Insert_Row_values)
            connection.commit()

            await interaction.response.send_message("Я его сохранил")

            cursor.close()
            connection.close()
            print("Соединение закрыто")

@bot.slash_command(name="загрузка", description="Загрузка сохраненых данных", guild_ids=[ServerID])#Выгрузить сообщение с БД
async def store_info(interaction: Interaction):
    guild = interaction.guild.id
    table = "DB_"+str(guild)

    try:
        connection = mysql.connector.connect(host='localhost', 
                                         database='EFBot', 
                                         user='root', 
                                         password='root')
        cursor = connection.cursor()

        sql_select_query = "SELECT * FROM " + table + " WHERE user LIKE '" + str(interaction.user) + "'"
        cursor.execute(sql_select_query)

        record = cursor.fetchall()

        Received_Data = []

        for row in record:
            Received_Data.append({"Id": str(row[0]), "Пользователь": str(row[1]), "Сообщение": str(row[2])})
        output = ""
        for i, row in enumerate(Received_Data):
            if i > 0:
                output += "\n"
            output += "" + "\n"
            for key, value in row.items():
                output += "  " + key + ": " + value + "\n"
            output += ""
        await interaction.response.send_message("Все сохраненные данные: \n \n" + output)
    except mysql.connector.Error as error:
        print("Не удалось загрузить данные из MySql: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Соединение закрыто")

bot.run(TOKEN)
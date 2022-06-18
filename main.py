import os
from datetime import datetime
import discord
from discord.ext import tasks
import csv
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

OWNERID=int(os.getenv('OWNERID'))
intents = discord.Intents.all()
bot = discord.Bot(intents=intents, owner_id = OWNERID)

try:
    connection = sqlite3.connect('discord.db')
    print("Connected to SQLite")
    cursor = connection.cursor()
except sqlite3.Error as error:
    print("Failed to connect with sqlite3 database", error)

TABLE_PARAMETER = "{TABLE_PARAMETER}"
DELETE_TABLE_SQL = f"DELETE FROM {TABLE_PARAMETER};"
GET_TABLES_SQL = "SELECT name FROM sqlite_schema WHERE type='table';"
GET_CHAT_SQL = f"SELECT msg FROM {TABLE_PARAMETER};"

def get_tables(con):
    cur = con.cursor()
    cur.execute(GET_TABLES_SQL)
    tables = cur.fetchall()
    cur.close()
    return tables

def clean_table(con):
    tables = get_tables(con)
    cur = con.cursor()
    for table, in tables:
        sql = DELETE_TABLE_SQL.replace(TABLE_PARAMETER, table)
        cur.execute(sql)
    cur.close()
    con.commit()

def table_to_csv(con):
    if os.path.exists("output.csv"):
        os.remove("output.csv")
    else:
        print("The file does not exist")
    tables = get_tables(con)
    cur = con.cursor()
    for table, in tables:
        sql = GET_CHAT_SQL.replace(TABLE_PARAMETER, table)
        data = cur.execute(sql)
        with open('output.csv', 'a',encoding='utf-8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow((table,""))
            writer.writerows(data)
    cur.close()

def PostPastebinAPI(args):
    errors_list = [
        "Bad API request, invalid api_option",
        "Bad API request, invalid api_dev_key",
        "Bad API request, maximum number of 25 unlisted pastes for your free account",
        "Bad API request, maximum number of 10 private pastes for your free account",
        "Bad API request, api_paste_code was empty",
        "Bad API request, maximum paste file size exceeded",
        "Bad API request, invalid api_paste_expire_date",
        "Bad API request, invalid api_paste_private",
        "Bad API request, invalid api_paste_format",
        "Bad API request, invalid api_user_key",
        "Bad API request, invalid or expired api_user_key",
        "Bad API request, you can't add paste to folder as guest"
    ]
    response = requests.post("https://pastebin.com/api/api_post.php", args)
    if response.text in errors_list:
        return "Pastebin API Error: \n" "{}".format(response.text)
    return response.text

@tasks.loop(hours=12)
async def packup():
    #print(packup.current_loop)
    if(packup.current_loop!=0):
        table_to_csv(connection)
        clean_table(connection)
        dt = datetime.now()
        current=str(dt.strftime("%X %d-%m-%Y"))
        PASTEBIN_DEVKEY=os.getenv('PASTEBIN_DEVKEY')
        PASTEBIN_USER_KEY=os.getenv('PASTEBIN_USER_KEY')
        with open("output.csv",encoding='utf8') as file:
            code=file.read()+"\n"
        Post = PostPastebinAPI({
            "api_dev_key": PASTEBIN_DEVKEY,
            "api_user_key": PASTEBIN_USER_KEY,
            "api_option": "paste",
            "api_paste_expire_date": "1D",
            "api_paste_code": code,
            "api_paste_name": current,
            "api_paste_private": "2"
        })
        #print(Post)

packup.start()

GUILDID=int(os.getenv('GUILDID'))
@bot.slash_command(guild_ids=[GUILDID])
async def create_table(ctx: discord.ApplicationContext):
    if(await bot.is_owner(ctx.user)):
        if (ctx.guild_id==GUILDID):
            guild = bot.get_guild(GUILDID)
            a = guild.text_channels
            for i in a:
                b=str(i).replace("-","_")
                print(b)
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE "+b+"(no INTEGER PRIMARY KEY, msg TEXT)")
            await ctx.respond(f"Hello {ctx.author}!")


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    msg = f'{message.created_at}  {message.author}: {message.content}'
    a="INSERT INTO "+str(message.channel).replace("-", "_")+"(msg) VALUES (\""+msg+"\")"
    cursor.execute(a)
    connection.commit()

token=os.getenv('TOKEN')
bot.run(token)
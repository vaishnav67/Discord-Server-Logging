# Discord Server Logging
 A simple discord server logger which uploads the contents to pastebin

# Requirements
* Python 3 (module requirements in requirements.txt)
* Discord API access
* Pastebin API access

# How does it work?
1. Edit values according to your server/guild in main.py
2. Run the bot and use the /create_table command in your server to create a SQLite db containing different text channels as tables with messages as rows
3. Constantly monitor all text chats and saves them in SQLite
4. Converts SQLite data to text and uploads them to Pastebin
5. Database gets cleared and back to step 3

# Environment Variables
TOKEN, PASTEBIN_DEVKEY, PASTEBIN_USER_KEY, GUILDID, OWNERID

# To-do
2. Code simplification (which means never)
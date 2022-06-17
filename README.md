# Discord Server Logging
 A simple discord server logger which uploads the contents to pastebin

# Requirements
1. Python 3 (module requirements in requirements.txt)
2. Discord API access
3. Pastebin API access

# How does it work?
1. Edit values according to your server/guild in main.py
2. Run the bot and use the /create_table command in your server to create a SQLite db containing different text channels as tables with messages as rows
3. Constantly monitor all text chats and saves them in SQLite
4. Converts SQLite data to text and uploads them to Pastebin
5. Database gets cleared and back to step 3

# To-do
1. Implement user api for pastebin (else it posts as guest)
2. Code simplification (which means never)
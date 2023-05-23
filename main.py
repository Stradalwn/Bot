from pyrogram import Client, idle, compose
from config import Config
from plugins.dl import user

app = Client(
        "bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        workers=50,
        plugins=dict(root="plugins")
    )

apps = [app, user]

for app in apps:
    app.start()
    s = app.get_me()
    print(s.username)
idle()
for app in apps:
    app.stop()


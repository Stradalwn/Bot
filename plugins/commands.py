import os
import time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
import requests

from db import Database
from Script import script
from config import Config
from utiles import check_user, progress

START_TXT = script.START_TXT
HELP_TXT = script.HELP_TXT
ABOUT_TXT = script.ABOUT_TXT

db = Database(Config.DB_URL,Config.DB_NAME)

@Client.on_message(filters.command("users") & filters.private & filters.user(Config.ADMINS))
async def users(bot, cmd):
    try:
        users = await db.get_all_user()
    except Exception as e:
        return await cmd.reply_text(f"Error In UserId {e}")
    if not users:
        return await cmd.reply_text("users not found yet")
    
    users_text = ''
    for user in users:
        users_text += f"{user['user_id']}  :  {user['user_name']} \n"

    if users_text:
        return await cmd.reply_text(f"Users List \n\n{users_text}")
    
    else:
        return await cmd.reply_text(f"Something went wrong")

@Client.on_message(filters.command("clear_cache") & filters.private & filters.user(Config.ADMINS))
async def clear_cache(bot, cmd):
    extensions_to_remove = ['.mkv', '.mp4', '.ogg', '.gif', '.webp', 'mp3', '.wave', '.zip']
    removed_files = []
    kt = await cmd.reply_text("Searching Cache Files In OS 🗃️...")
    for filename in os.listdir('./'):
    # check if the file extension is in the list of extensions to remove
        if any(filename.endswith(extension) for extension in extensions_to_remove):
            # if the file extension matches, remove the file and add its name to the removed_files list
            os.remove(os.path.join('./', filename))
            removed_files.append(filename)
    
    if len(removed_files) == 0:
        return await kt.edit_text("The Cache Is Empty")
    
    cache_list = ''
    for filename in removed_files:
        cache_list += f"{filename} \n"
    
    cache_list += f"\n {len(removed_files)} files | file removed"

    return await kt.edit_text(cache_list)


@Client.on_message(filters.command("add_user") & filters.private & filters.user(Config.ADMINS))
async def add_user(bot, cmd):
    
    if not " " in cmd.text:
        return await cmd.reply_text("Pls Use Correct Format \n\n/add_user USER_ID \n\neg:- /add_user 1288398723")
    
    command , user_id = cmd.text.split(' ')

    try:
        user = await bot.get_users(user_id)
    except Exception as e:
        return await cmd.reply_text(f"Error In UserId {e}")
    if not user:
        return await cmd.reply_text("user id invalid")
    
    dbUser, State = await db.add_user(user.id, user.first_name)

    if State:
        return await cmd.reply_text(f"User Added Succesfully at {dbUser}: \nuser id: {user.id} \nuser name: {user.first_name}")
    
    else:
        return await cmd.reply_text(f"User Already Exists at {dbUser['_id']}: \nuser id: {dbUser['user_id']} \nuser name: {dbUser['user_name']}")

@Client.on_message(filters.command("remove_user") & filters.private & filters.user(Config.ADMINS))
async def remove_user(bot, cmd):
    
    if not " " in cmd.text:
        return await cmd.reply_text("Pls Use Correct Format \n\n/remove_user USER_ID \n\neg:- /remove_user 1288398723")
    
    command , user_id = cmd.text.split(' ')
    
    try:
        user = await bot.get_users(user_id)
    except Exception as e:
        return await cmd.reply_text(f"Error In UserId {e}")
    if not user:
        return await cmd.reply_text("user id invalid")
    
    state = await db.delete_user(user.id)

    if state:
        return await cmd.reply_text(f"User Delete at: \nuser id: {user.id} \nuser name: {user.first_name}")
    
    else:
        return await cmd.reply_text(f"User Doesn't Exists at \nuser id: \nuser name: {user.first_name}")

@Client.on_message(filters.command("add_caption") & filters.private)
async def add_caption(bot, cmd):
    if not ' ' in cmd.text:
        return await cmd.reply_text(f"Use correct formate /add_caption IMG_URL")
    command, caption = cmd.text.split(' ')

    dbCaption = await db.add_caption(cmd.from_user.id, caption)

    if dbCaption:
        return await cmd.reply_text(f"Caption Added Succesfully at {dbCaption}: \ncaption: {caption}")
    
    else:
        return await cmd.reply_text(f"Faild to add Caption : {caption}")

@Client.on_message(filters.command("remove_caption") & filters.private)
async def remove_caption(bot, cmd):
    state = await db.delete_caption(cmd.from_user.id)
    if state:
        return await cmd.reply_text(f"Caption Deleted")
    
    else:
        return await cmd.reply_text(f"Caption Doesn't Exists Yet")

@Client.on_message(filters.photo & filters.private )
async def add_thumbnail_photo(bot, cmd):
    download_location = f"{Config.DOWNLOAD_LOCATION}/{cmd.from_user.id}.jpg"
    await cmd.download(file_name=download_location)
    await cmd.reply_text(
        text="your custom thumbnail is saved",
        quote=True
    )

@Client.on_message(filters.command("thumb") & filters.incoming & filters.private)
async def send_photo(bot, message):
    download_location = f"{Config.DOWNLOAD_LOCATION}/{message.from_user.id}.jpg"

    if os.path.isfile(download_location):
        await message.reply_photo(
            photo=download_location,
            caption="your custom thumbnail",
            quote=True
        )
    else:
        await message.reply_text(text="you don't have set thumbnail yet!. send .jpg img to save as thumbnail.", quote=True)

@Client.on_message(filters.command("delthumb") & filters.incoming & filters.private)
async def delete_photo(bot, message):
    download_location = f"{Config.DOWNLOAD_LOCATION}/{message.from_user.id}.jpg"
    if os.path.isfile(download_location):
        os.remove(download_location)
        await message.reply_text(text="your thumbnail removed successfully.", quote=True)
    else:
        await message.reply_text(text="you don't have set thumbnail yet!. send .jpg img to save as thumbnail.", quote=True)

# @Client.on_message(filters.command("add_thumbnail") & filters.private)
# async def add_thumbnail(bot, cmd):
#     stats = await check_user(cmd)
#     if not stats:
#         return await cmd.reply_text(f"This is privet bot, you don't have acces to use this bot")

#     stats = await check_user(cmd)
#     if not stats:
#         return await cmd.reply_text(f"This is privet bot, you don't have acces to use this bot")
#     if not ' ' in cmd.text:
#         return await cmd.reply_text(f"Use correct formate /add_thumbnail IMG_URL")
#     command, img = cmd.text.split(' ')

#     if not img.endswith('.jpeg'):
#         return await cmd.reply_text(f"Use correct img formate `jpeg`")
    
#     dbThumb = await db.add_thumbnail(cmd.from_user.id, img)

#     if dbThumb:
#         return await cmd.reply_photo(photo=img, caption=f"Thumbnail Added Succesfully at {dbThumb}: \nimg: {img} \n\nThe thumbnail should be in JPEG format and less than 200 KB in size. A thumbnail’s width and height should not exceed 320 pixels.")
    
#     else:
#         return await cmd.reply_text(f"Faild to add Thumbnail : {img}")

# @Client.on_message(filters.command("remove_thumbnail") & filters.private)
# async def remove_thumbnail(bot, cmd):
#     stats = await check_user(cmd)
#     if not stats:
#         return await cmd.reply_text(f"This is privet bot, you don't have acces to use this bot")

#     state = await db.delete_thumbnail(cmd.from_user.id)
#     if state:
#         return await cmd.reply_text(f"Thumbnail Deleted")
    
#     else:
#         return await cmd.reply_text(f"Thumbnail Doesn't Exists")


@Client.on_message(filters.command("stats") & filters.private)
async def stats(bot, cmd):
    user_id = cmd.from_user.id
    caption = await db.get_caption(user_id)
    thumbnail = await db.get_thumbnail(user_id)
    user = await db.get_user(user_id)

    caption = caption['caption'] if caption else None
    thumbnail = thumbnail['thumbnail'] if thumbnail else None
    user_sts = 'Pro' if user else None

    if thumbnail:
        return await cmd.reply_photo(photo=thumbnail, caption=f"User : {user_sts} \nThumbnail : {thumbnail} \nCaption : {caption}")
    else:
        return await cmd.reply_text(f"User : {user_sts} \nThumbnail : {thumbnail} \nCaption : {caption}")
       
@Client.on_message(filters.command("start") & filters.private)
async def start(bot, cmd):
    await cmd.reply_text(
        START_TXT.format(cmd.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔮Help", callback_data='help_cb'),
                    InlineKeyboardButton(
                        "⚔About", callback_data='about_cb')
                ],
                [
                    InlineKeyboardButton(
                        "👨🏼‍💻Developer", url='https://fiverr.com/kalanakt'),
                    InlineKeyboardButton(
                        "⚙️Update Channel", url="https://t.me/TMWAD")
                ]
            ]
        )
    )


@Client.on_message(filters.command("help") & filters.private)
async def help(bot, cmd):
    await cmd.reply_text(
        HELP_TXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚔About", callback_data='about_cb'),
                    InlineKeyboardButton("⚡Back", callback_data='start_cb')
                ],
                [
                    InlineKeyboardButton(
                        "👨🏼‍💻Developer", url='https://fiverr.com/kalanakt'),
                    InlineKeyboardButton(
                        "⚙️Update Channel", url="https://t.me/TMWAD")
                ]
            ]
        )
    )


@Client.on_message(filters.command("about") & filters.private)
async def about(bot, cmd):
    await cmd.reply_text(
        ABOUT_TXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔮Help", callback_data='help_cb'),
                    InlineKeyboardButton("⚡Back", callback_data='start_cb')
                ],
                [
                    InlineKeyboardButton(
                        "👨🏼‍💻Developer", url='https://fiverr.com/kalanakt'),
                    InlineKeyboardButton(
                        "⚙️Update Channel", url="https://t.me/TMWAD")
                ]
            ]
        )
    )

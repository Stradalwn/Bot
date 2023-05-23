import re
import time
from pyrogram import Client, filters
import os
import gdown
import requests
from urllib.parse import unquote
import urllib3
import wget
from PIL import Image

from config import Config
from db import Database
from utiles import Mdata01, Mdata03, check_user, progress

googledrive_file_regex = r'^https?://drive\.google\.com/file/d/([\w-]+)$'
googledrive_folder_regex = r'^https:\/\/drive\.google\.com\/drive\/folders\/([-\w]+)$'
link_regex = re.compile(r'http(s)?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}(/\S*)?')


db = Database(Config.DB_URL, Config.DB_NAME)
user = Client(
        "user",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=Config.USER_SESSION_STRING,
        in_memory=True
    )

@Client.on_message(filters.text & filters.private & ~ filters.bot)
async def dl(bot, cmd):
    link = cmd.text

    if link.startswith('/'):
        return

    match = re.match(googledrive_file_regex, link)
    match_folder = re.match(googledrive_folder_regex, link)
    match_link = link_regex.search(link)

    user_id = cmd.from_user.id
    caption = await db.get_caption(user_id)
    # thumbnail = await db.get_thumbnail(user_id)

    caption_text = caption['caption'] if caption else None
    # thumbnail = thumbnail['thumbnail'] if thumbnail else None

    # if thumbnail:
    #     response = requests.get(thumbnail)
    #     content = response.content
    #     thumbnail_path = f"{user_id}_thumb.jpeg"

    #     with open(thumbnail_path, "wb") as f:
    #         f.write(content)

    #     img = Image.open(thumbnail_path)
    #     new_width, new_height = 300, 300

    #     resized_img = img.resize((new_width, new_height))
    #     if os.path.exists(thumbnail_path):
    #         os.remove(thumbnail_path)
    #     resized_img.save(thumbnail_path)

    if match or match_folder:
        stats = await check_user(cmd)
        if not stats:
            await cmd.reply_text(f"This is privet bot, you don't have acces to use this bot")
            return
    
    resized_img = f"{Config.DOWNLOAD_LOCATION}/{user_id}.jpg"

    resized_img = resized_img if os.path.isfile(resized_img) else None

    if match:
        file_id = match.group(1)
        kt = await cmd.reply_text('file downloading...')
        try:
            file = gdown.download(id=file_id)
        except Exception as e:
            await kt.delete()
            return await cmd.reply_text(f'Error : {e}')
        if file is None:
            await kt.delete()
            return await cmd.reply_text('Error : File is may not public or banned.')

        await kt.edit_text(f'Download succesfully : uploading to telegram....')
        start_time = time.time()
        if file.endswith('.png') or file.endswith('.jpg'):
            await bot.send_photo(
                chat_id=cmd.chat.id,
                photo=file
            )
        elif file.endswith('.mkv') or file.endswith('.zip'):
            try:
                await user.send_document(
                    chat_id=Config.LOG_CHANNEL,
                    document=file,
                    thumb=resized_img,
                    caption=caption
                )
            except Exception as e:
                await kt.edit_text(f"Error : {e}. \nTring To Upload Again ...")
                await bot.send_document(
                    chat_id=cmd.chat.id,
                    document=file,
                    thumb=resized_img,
                    caption=caption_text,
                    progress=progress,
                    progress_args=(
                        "<i>{} </i>\n\n📤 Uploading Please Wait ",
                        cmd,
                        start_time
                    )
                )
        elif file.endswith('.mp3') or file.endswith('.wave'):
            duration = await Mdata03(file)
            await bot.send_audio(
                chat_id=cmd.chat.id,
                audio=file,
                thumb=resized_img,
                caption=caption_text,
                duration=duration,
                progress=progress,
                progress_args=(
                    "<i>{} </i>\n\n📤 Uploading Please Wait ",
                    cmd,
                    start_time
                )
            )
        elif file.endswith('.webp'):
            await bot.send_sticker(
                cmd.chat.id,
                file
            )
        elif file.endswith('.mp4'):
            width, height, duration = await Mdata01(file)
            try:
                await user.send_video(
                    chat_id=Config.LOG_CHANNEL,
                    video=file,
                    thumb=resized_img,
                    caption=caption,
                    duration=duration, 
                    width=width, 
                    height=height,
                )
            except Exception as e:
                await kt.edit_text(f"Error : {e}. \nTring To Upload Again ...")
                await bot.send_video(
                    chat_id=cmd.chat.id,
                    video=file,
                    thumb=resized_img,
                    caption=caption_text,
                    duration=duration, 
                    width=width, 
                    height=height, 
                    supports_streaming=True,
                    progress=progress,
                    progress_args=(
                        "<i>{} </i>\n\n📤 Uploading Please Wait ",
                        cmd,
                        start_time
                    )
                )
        elif file.endswith('.gif'):
            await bot.send_animation(
                cmd.chat.id,
                file
            )
        elif file.endswith('.ogg'):
            await bot.send_voice(
                cmd.chat.id,
                file
            )

        else:
            await bot.send_message(cmd.chat.id, f"Error : File Type Not Valid")

        if os.path.exists(file):
            os.remove(file)

        return await kt.delete()
    elif match_folder:
        folder_id = match_folder.group(1)
        kt = await cmd.reply_text('files downloading...')
        try:
            filenames = gdown.download_folder(
                id=folder_id, quiet=True, use_cookies=False)
        except Exception as e:
            await kt.delete()
            return await cmd.reply_text(f'Error : {e}')
        if filenames is None:
            await kt.delete()
            return await cmd.reply_text('Error : Folder is may not public or banned.')

        await kt.edit_text(f'Download succesfully : uploading to telegram...')

        for file in filenames:
            if file.endswith('.png') or file.endswith('.jpg'):
                await bot.send_photo(
                    chat_id=cmd.chat.id,
                    photo=file
                )
            elif file.endswith('.mkv') or file.endswith('.zip'):
                try:
                    await user.send_document(
                        chat_id=Config.LOG_CHANNEL,
                        document=file,
                        thumb=resized_img,
                        caption=caption
                    )
                except Exception as e:
                    await kt.edit_text(f"Error : {e}. \nTring To Upload Again ...")
                    await bot.send_document(
                        chat_id=cmd.chat.id,
                        document=file,
                        thumb=resized_img,
                        caption=caption_text,
                        progress=progress,
                        progress_args=(
                            "<i>{} </i>\n\n📤 Uploading Please Wait ",
                            cmd,
                            start_time
                        )

                    )
            elif file.endswith('.mp3') or file.endswith('.wave'):
                duration = await Mdata03(file)
                await bot.send_audio(
                    chat_id=cmd.chat.id,
                    audio=file,
                    thumb=resized_img,
                    caption=caption_text,
                    duration=duration,
                    progress=progress,
                    progress_args=(
                        "<i>{} </i>\n\n📤 Uploading Please Wait ",
                        cmd,
                        start_time
                    )

                )
            elif file.endswith('.webp'):
                await bot.send_sticker(
                    cmd.chat.id,
                    file
                )
            elif file.endswith('.mp4'):
                width, height, duration = await Mdata01(file)
                try:
                    await user.send_video(
                        chat_id=Config.LOG_CHANNEL,
                        video=file,
                        thumb=resized_img,
                        caption=caption,
                        duration=duration, 
                        width=width, 
                        height=height
                    )
                except Exception as e:
                    await kt.edit_text(f"Error : {e}. \nTring To Upload Again ...")
                    await bot.send_video(
                        chat_id=cmd.chat.id,
                        video=file,
                        thumb=resized_img,
                        caption=caption_text,
                        duration=duration, 
                        width=width, 
                        height=height, 
                        supports_streaming=True,
                        progress=progress,
                        progress_args=(
                            "<i>{} </i>\n\n📤 Uploading Please Wait ",
                            cmd,
                            start_time
                        )
                    )
            elif file.endswith('.gif'):
                await bot.send_animation(
                    cmd.chat.id,
                    file
                )
            elif file.endswith('.ogg'):
                await bot.send_voice(
                    cmd.chat.id,
                    file
                )

            else:
                await bot.send_message(cmd.chat.id, f"Error : File Type Not Valid")

            if os.path.exists(file):
                os.remove(file)
    elif match_link:
        kt = await cmd.reply_text('file downloading using w get 🚀...')
        try:
            filename = wget.download(link)
        except Exception as e:
            await kt.edit_text(f"Error {e}. Trying Again Pls wait ⌛...")
            response = requests.get(link, stream=True)
            if response.status_code == 200:
                # open the file in binary mode and write the contents of the response to it
                filename = unquote(link.split('/')[-1])
                filename = filename.replace(' ', '_')
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                return await kt.edit_text(f"Failed To Downlaod : {link}...")

        await kt.edit_text(f'Download succesfully : uploading to telegram..')

        start_time = time.time()
        if filename.endswith('.png') or filename.endswith('.jpg'):
            await bot.send_photo(
                chat_id=cmd.chat.id,
                photo=filename
            )
        elif filename.endswith('.mkv') or filename.endswith('.zip'):
            await bot.send_document(
                chat_id=cmd.chat.id,
                document=filename,
                thumb=resized_img,
                caption=caption_text,
                progress=progress,
                progress_args=(
                    "<i>{} </i>\n\n📤 Uploading Please Wait ",
                    cmd,
                    start_time
                )
            )
        elif filename.endswith('.mp3') or filename.endswith('.wave'):
            duration = await Mdata03(filename)
            await bot.send_audio(
                chat_id=cmd.chat.id,
                audio=filename,
                thumb=resized_img,
                caption=caption_text,
                duration=duration,
                progress=progress,
                progress_args=(
                    "<i>{} </i>\n\n📤 Uploading Please Wait ",
                    cmd,
                    start_time
                )
            )
        elif filename.endswith('.webp'):
            await bot.send_sticker(
                cmd.chat.id,
                filename
            )
        elif filename.endswith('.mp4'):
            width, height, duration = await Mdata01(filename)
            await bot.send_video(
                chat_id=cmd.chat.id,
                video=filename,
                thumb=resized_img,
                caption=caption_text,
                duration=duration, 
                width=width, 
                height=height, 
                supports_streaming=True,
                progress=progress,
                progress_args=(
                    "<i>{} </i>\n\n📤 Uploading Please Wait ",
                    cmd,
                    start_time
                )
            )
        elif filename.endswith('.gif'):
            await bot.send_animation(
                cmd.chat.id,
                filename
            )
        elif filename.endswith('.ogg'):
            await bot.send_voice(
                cmd.chat.id,
                filename
            )

        else:
            await bot.send_message(cmd.chat.id, f"Error : File Type Not Valid")

        if os.path.exists(filename):
            os.remove(filename)

        return await kt.delete()
    
    else:
        return cmd.reply_text("Not recornize text")

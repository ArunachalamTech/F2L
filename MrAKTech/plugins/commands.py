import asyncio
import time
import os
import requests

from telegraph import upload_file
import logging
from platform import python_version

from pyrogram import filters, enums, __version__
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums.parse_mode import ParseMode

from MrAKTech import StreamBot
from MrAKTech.config import Telegram
from MrAKTech.tools.txt import tamilxd, BUTTON
from MrAKTech.database.u_db import u_db
from MrAKTech.tools.utils_bot import temp, readable_time, verify_user, is_check_admin

logger = logging.getLogger(__name__)


@StreamBot.on_message(
    filters.command("stop") & filters.private & filters.user(list(Telegram.OWNER_ID))
)
async def alive(bot: StreamBot, message: Message):  # type: ignore
    print("Stopping...")
    ax = await message.reply("Stopping...")
    try:
        await StreamBot.stop()
    except:  # noqa: E722
        pass
    print("Bot Stopped")
    await ax.edit_text("Bot Stopped")


@StreamBot.on_message(filters.command("alive"))
async def alivex(bot: StreamBot, message: Message):  # type: ignore
    txt = (
        f"**{temp.B_NAME}** ```RUNNING```\n"
        f"-> Current Uptime: `{readable_time((time.time() - temp.START_TIME))}`\n"
        f"-> Python: `{python_version()}`\n"
        f"-> Pyrogram: `{__version__}`"
    )
    await message.reply_text(txt, quote=True)


@StreamBot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if not await verify_user(client, message):
        return
    chat_id = message.text.split("_")[-1]
    if chat_id == "/start":
        await message.reply_photo(
            photo="https://graph.org/file/8cd764fbdf3ccd34abe22.jpg",
            caption=tamilxd.START_TXT.format(
                message.from_user.first_name, message.from_user.id
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=BUTTON.START_BUTTONS,
            quote=True,
        )
    else:
        if "channel" in message.text:
            tamil = await message.reply_text(
                "Geting your channel data, Please Wait...", quote=True
            )
            chat = await client.get_chat(chat_id)
            if chat.type != enums.ChatType.CHANNEL:
                await tamil.edit_text("This is Invalid command.")
            if not await is_check_admin(client, chat_id, message.from_user.id):
                await tamil.edit_text("You are not an admin in this channel.")
            else:
                username = chat.username
                username = "@" + username if username else "private"
                chatx = await u_db.add_channel(
                    int(message.from_user.id), int(chat_id), chat.title, username
                )
                await tamil.edit_text(
                    (
                        "<b>Channel added successfully.</b>"
                        if chatx
                        else "<b>This channel already added!...</b>"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("≺≺ Back", callback_data="channels")]]
                    ),
                )
        else:
            await message.reply_text("**Invalid Command**", quote=True)


@StreamBot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    await update.reply_text(
        text=tamilxd.ABOUT_TXT,
        disable_web_page_preview=True,
        reply_markup=BUTTON.ABOUT_BUTTONS,
        quote=True,
    )


@StreamBot.on_message(filters.command("help") & filters.private)
async def help_handler(bot, message):
    await message.reply_text(
        text=tamilxd.HELP_TXT,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=BUTTON.HELP_BUTTONS,
        quote=True,
    )


# thiss is for shortner
@StreamBot.on_message(filters.command(["shortner", "shortener"]) & filters.private)
async def shortner(bot, message):
    if not await verify_user(bot, message):
        return
    user_id = message.from_user.id
    userxdb = await u_db.get_user_details(user_id)
    buttons = []
    if userxdb["shortener_url"] and userxdb["shortener_api"] is not None:
        buttons.append(
            [InlineKeyboardButton("Show shortner", callback_data="show_shortner")]
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    "Default shortner", callback_data="delete_shortner"
                ),
                InlineKeyboardButton("Change shortner", callback_data="add_shortner"),
            ]
        )
    else:
        buttons.append(
            [InlineKeyboardButton("Set shortner", callback_data="add_shortner")]
        )
    buttons.append([InlineKeyboardButton("Close", callback_data="close")])
    await message.reply_text(
        text=tamilxd.CUSTOM_SHORTNER_TXT,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# this is for caption
@StreamBot.on_message(filters.command("caption"))
async def caption(bot, message):
    if not await verify_user(bot, message):
        return
    user_id = message.from_user.id
    caption = await u_db.get_caption(user_id)
    buttons = []
    if caption is not None:
        buttons.append(
            [InlineKeyboardButton("Show caption", callback_data="show_caption")]
        )
        buttons.append(
            [
                InlineKeyboardButton("Default caption", callback_data="delete_caption"),
                InlineKeyboardButton("Change caption", callback_data="add_caption"),
            ]
        )
    else:
        buttons.append(
            [InlineKeyboardButton("Set caption", callback_data="add_caption")]
        )
    buttons.append([InlineKeyboardButton("Close", callback_data="close")])
    await message.reply_text(
        text=tamilxd.CUSTOM_CAPTION_TXT,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@StreamBot.on_message(filters.command("settings"))
async def settings(client, message):
    await message.reply_text(
        "<b>ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ꜱᴇᴛᴛɪɴɢꜱ ᴀꜱ ʏᴏᴜʀ ᴡɪꜱʜ </b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Personal settings", callback_data="settings"),
                ],
                [InlineKeyboardButton("Channels settings", callback_data="channels")],
                [InlineKeyboardButton("≺≺ Close", callback_data="close")],
            ]
        ),
    )


# this is for user settings
@StreamBot.on_message(filters.command(["usetting", "us", "usettings"]))
async def settings(client, message):  # noqa: F811
    userxdb = await u_db.get_user_details(message.from_user.id)
    button = [
        [
            InlineKeyboardButton(
                (
                    "✅ Custom caption"
                    if userxdb["caption"] is not None
                    else "📝 Custom caption"
                ),
                callback_data="custom_caption",
            )
        ],
        [
            InlineKeyboardButton(
                (
                    "✅ Custom shortner"
                    if userxdb["shortener_url"] and userxdb["shortener_api"] is not None
                    else "🖼️ Custom shortner"
                ),
                callback_data="custom_shortner",
            )
        ],
        [
            InlineKeyboardButton("📤 Upload mode", callback_data="toggle_mode"),
            InlineKeyboardButton(
                userxdb["method"] if userxdb["method"] else "Links",
                callback_data="toggle_mode",
            ),
        ],
        [InlineKeyboardButton("Close ✗", callback_data="close")],
    ]
    await message.reply_text(
        text=tamilxd.SETTINGS_TXT.format(
            CAPTION="✅ Exists" if userxdb["caption"] is not None else "❌ Not Exists",
            URLX=(
                userxdb["shortener_url"]
                if userxdb["shortener_url"] is not None
                else "❌ Not Exists"
            ),
            APIX=(
                userxdb["shortener_api"]
                if userxdb["shortener_api"] is not None
                else "❌ Not Exists"
            ),
            STORAGEX=userxdb["storage"],
            METHODX=userxdb["method"],
            AUTO_EXTRACT="✅ Enabled" if userxdb.get("auto_extract", True) else "❌ Disabled",
        ),
        reply_markup=InlineKeyboardMarkup(button),
        disable_web_page_preview=True,
        quote=True,
    )


# this is for channels settings
@StreamBot.on_message(filters.command(["channels", "csetting", "cs", "csettings"]))
async def settings(bot, msg):  # noqa: F811
    buttons = []
    channels = await u_db.get_user_channels(msg.from_user.id)
    for channel in channels:
        buttons.append(
            [
                InlineKeyboardButton(
                    f"{channel['title']}",
                    callback_data=f"editchannels_{channel['chat_id']}",
                )
            ]
        )
    buttons.append(
        [InlineKeyboardButton("✚ Add Channel ✚", callback_data="addchannel")]
    )
    buttons.append([InlineKeyboardButton("≺≺ Back", callback_data="main")])
    await msg.reply_text(
        "<b><u>My Channels</b></u>\n\n<b>you can manage your target chats in here</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
    )


# this is for features
@StreamBot.on_message(filters.command("features") & filters.private)
async def about_handler(bot, message):
    hs = await message.reply_photo(
        photo="https://graph.org/file/68a0935f0d19ffd647a09.jpg",
        caption=(tamilxd.COMMENTS_TXT.format(message.from_user.mention)),
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("↻ ᴄʟᴏsᴇ ↻", callback_data="close")]]
        ),
    )
    await asyncio.sleep(150)
    await hs.delete()
    await message.delete()


# this is for id get
@StreamBot.on_message(filters.command("id"))
async def get_id(bot: StreamBot, message: Message):  # type: ignore
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"**File ID**: `{rep.audio.file_id}`"
            file_id += "**File Type**: `audio`"

        elif rep.document:
            file_id = f"**File ID**: `{rep.document.file_id}`"
            file_id += f"**File Type**: `{rep.document.mime_type}`"

        elif rep.photo:
            file_id = f"**File ID**: `{rep.photo.file_id}`"
            file_id += "**File Type**: `photo`"

        elif rep.sticker:
            file_id = f"**Sicker ID**: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"**Sticker Set**: `{rep.sticker.set_name}`\n"
                file_id += f"**Sticker Emoji**: `{rep.sticker.emoji}`\n"
                if rep.sticker.is_animated:
                    file_id += f"**Animated Sticker**: `{rep.sticker.is_animated}`\n"
                else:
                    file_id += "**Animated Sticker**: `False`\n"
            else:
                file_id += "**Sticker Set**: __None__\n"
                file_id += "**Sticker Emoji**: __None__"

        elif rep.video:
            file_id = f"**File ID**: `{rep.video.file_id}`\n"
            file_id += "**File Type**: `video`"

        elif rep.animation:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `GIF`"

        elif rep.voice:
            file_id = f"**File ID**: `{rep.voice.file_id}`\n"
            file_id += "**File Type**: `Voice Note`"

        elif rep.video_note:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `Video Note`"

        elif rep.location:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.location.latitude}`"

        elif rep.venue:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.venue.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.venue.location.latitude}`\n\n"
            file_id += "**Address**:\n"
            file_id += f"**title**: `{rep.venue.title}`\n"
            file_id += f"**detailed**: `{rep.venue.address}`\n\n"

        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`"
        await message.reply(user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`\n\n"
        user_detail += file_id
        await message.reply(user_detail, quote=True)

    else:
        await message.reply(f"**Chat ID**: `{message.chat.id}`", quote=True)


# this is for telegraph
@StreamBot.on_message(filters.command("telegraph"))
async def telegraph_upload(bot, message):
    if not (reply_to_message := message.reply_to_message):
        return await message.reply("Reply to any photo or video.")
    file = reply_to_message.photo or reply_to_message.video or None
    if file is None:
        return await message.reply("Invalid media.")
    if file.file_size >= 5242880:
        await message.reply_text(text="Send less than 5MB")
        return
    text = await message.reply_text(text="Processing....", quote=True)
    media = await reply_to_message.download()
    try:
        response = upload_file(media)
    except Exception as e:
        await text.edit_text(text=f"Error - {e}")
        return
    try:
        os.remove(media)
    except:  # noqa: E722
        pass
    await text.edit_text(
        f"<b>❤️ Your Telegram Link Complete 👇</b>\n\n<code>https://telegra.ph/{response[0]}</code></b>"
    )


# this is for GPT codes
@StreamBot.on_message(filters.command(["askgpt", "gpt"]))
async def gpt(app, message: Message):
    text = "".join(message.text.split(" ")[1:])
    if len(text) == 0:
        return await message.reply_text(
            "Cannot reply to empty message.", parse_mode=ParseMode.MARKDOWN
        )
    m = await message.reply_text("Getting Request....", parse_mode=ParseMode.MARKDOWN)
    url = "https://api.safone.dev/chatgpt"
    payloads = {
        "message": text,
        # "version": 3,
        "chat_mode": "assistant",
        "dialog_messages": '[{"bot":"","user":""}]',
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payloads, headers=headers)
        results = response.json()
        res = results["message"]

        await m.edit_text(f"{res}")
    except Exception as e:
        await m.edit_text(f"Error :-\n{e}")


# this is for  donate
@StreamBot.on_message(filters.command(["donate"]))
async def donate(app, message: Message):
    await message.reply_text(
        text=tamilxd.DONATE_TXT,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=BUTTON.DONATE_BUTTONS,
        quote=True,
    )


# Auto extraction commands
@StreamBot.on_message(filters.command(["extract", "autoextract"]))
async def extract_toggle(bot, message):
    if not await verify_user(bot, message):
        return
    user_id = message.from_user.id
    auto_extract = await u_db.get_auto_extract(user_id)

    buttons = []
    buttons.append([
        InlineKeyboardButton(
            "✅ Enable Auto Extract" if not auto_extract else "❌ Disable Auto Extract",
            callback_data="toggle_extract"
        )
    ])
    buttons.append([InlineKeyboardButton("Close", callback_data="close")])

    status = "Enabled" if auto_extract else "Disabled"
    await message.reply_text(
        f"<b><u>🔍 AUTO EXTRACTION SETTINGS</u></b>\n\n"
        f"<b>Current Status:</b> {status}\n\n"
        f"<b>📝 What it does:</b>\n"
        f"• Automatically extracts quality (1080p, 720p, 4K, etc.)\n"
        f"• Finds season numbers (S01, S02, etc.)\n"
        f"• Detects episode numbers (E01, E02, etc.)\n"
        f"• Replaces placeholders in your custom caption\n\n"
        f"<b>🎯 Supported placeholders:</b>\n"
        f"<code>{{quality}}</code> - Video quality\n"
        f"<code>{{season}}</code> - Season number\n"
        f"<code>{{episode}}</code> - Episode number",
        disable_web_page_preview=True,
        quote=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# Example caption command
@StreamBot.on_message(filters.command(["examples", "example"]))
async def show_examples(bot, message):
    if not await verify_user(bot, message):
        return
    
    example_text = """<b><u>📝 CAPTION EXAMPLES WITH AUTO EXTRACTION</u></b>

<b>🎬 Example 1:</b>
<code>🎥 {file_name}

📺 Quality: {quality}
🎞️ Season: {season} | Episode: {episode}
📦 Size: {file_size}

📥 Download: {download_link}
🖥️ Stream: {stream_link}</code>

<b>🎬 Example 2:</b>
<code>📁 File: {file_name}
🔍 [{quality}] S{season}E{episode}
📊 Size: {file_size}

⬇️ {download_link}</code>

<b>🎬 Example 3:</b>
<code>🎦 **{file_name}**

🌟 Quality: **{quality}**
📺 Season {season} - Episode {episode}
💾 {file_size}

📱 Watch Online: {stream_link}
💿 Download: {download_link}</code>

<b>💡 Note:</b> These placeholders will be automatically replaced with extracted information from your file names!"""
    
    await message.reply_text(
        example_text,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔍 Configure Auto Extract", callback_data="toggle_extract"),
            InlineKeyboardButton("Close", callback_data="close")
        ]])
    )


# Test extraction command
@StreamBot.on_message(filters.command(["test", "testextract"]))
async def test_extraction(bot, message):
    if not await verify_user(bot, message):
        return
    
    if len(message.command) < 2:
        await message.reply_text(
            "<b>📋 Test Extraction</b>\n\n"
            "<b>Usage:</b> <code>/test filename</code>\n\n"
            "<b>Example:</b> <code>/test Game.of.Thrones.S08E06.1080p.WEB-DL.x264.mkv</code>\n\n"
            "This will show you what quality, season, and episode information can be extracted from the filename.",
            quote=True
        )
        return
    
    # Get filename from command
    filename = " ".join(message.command[1:])
    
    # Import extraction functions
    from MrAKTech.tools.extract_info import extract_quality, extract_season_number, extract_episode_number, extract_combined_info
    
    # Test individual extractions
    quality = extract_quality(filename)
    season = extract_season_number(filename)
    episode = extract_episode_number(filename)
    
    # Test combined extraction (filename only in this case)
    combined_info = extract_combined_info(filename)
    
    result_text = f"""<b><u>🔍 EXTRACTION TEST RESULT</u></b>

<b>📁 Filename:</b> <code>{filename}</code>

<b>📊 Extracted Information:</b>
🎞️ <b>Quality:</b> <code>{quality or 'Not detected'}</code>
📺 <b>Season:</b> <code>{season or 'Not detected'}</code>
🎬 <b>Episode:</b> <code>{episode or 'Not detected'}</code>

<b>🧠 Smart Extraction (Best Result):</b>
🎞️ <b>Final Quality:</b> <code>{combined_info['quality'] or 'Not detected'}</code>
📺 <b>Final Season:</b> <code>{combined_info['season'] or 'Not detected'}</code>
🎬 <b>Final Episode:</b> <code>{combined_info['episode'] or 'Not detected'}</code>

<b>💡 The bot now checks both filename AND original caption to get the most complete information!</b>"""
    
    await message.reply_text(
        result_text,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📝 See Examples", callback_data="show_examples"),
            InlineKeyboardButton("Close", callback_data="close")
        ]])
    )

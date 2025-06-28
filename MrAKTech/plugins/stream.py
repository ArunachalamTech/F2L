# (c) @MrAKTech

import asyncio
import random

from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from MrAKTech import StreamBot
from MrAKTech.config import Telegram, Domain
from MrAKTech.database.u_db import u_db
from MrAKTech.tools.utils_bot import short_link, verify_user
from MrAKTech.tools.human_readable import humanbytes
from MrAKTech.tools.file_properties import get_name, get_hash, get_media_file_size
from MrAKTech.tools.extract_info import smart_replace_placeholders_in_caption, create_safe_format_dict
from MrAKTech.tools.extract_info import extract_quality, extract_season_number, extract_episode_number, replace_placeholders_in_caption


@StreamBot.on_message(
    (filters.private) & (filters.document | filters.video | filters.audio), group=4
)
async def private_receive_handler(c: Client, m: Message):
    if not await verify_user(c, m):
        return
    #
    mediax = m.document or m.video or m.audio
    if m.document or m.video or m.audio:
        if m.caption:
            file_caption = f"{m.caption}"
        else:
            file_caption = ""
    file_captionx = file_caption.replace(".mkv", "")
    log_msg = await m.forward(chat_id=Telegram.FLOG_CHANNEL)
    user = await u_db.get_user(m.from_user.id)
    caption_position = user["method"]
    c_caption = user["caption"]
    
    # Extract quality, season, and episode information from both filename and original caption
    file_name = get_name(log_msg) or ""
    auto_extract = user.get("auto_extract", True)
    
    if auto_extract:
        # Use smart extraction that combines filename and original caption data
        c_caption = smart_replace_placeholders_in_caption(c_caption, file_name, file_captionx)
    
    storage = f"https://telegram.me/{Telegram.FILE_STORE_BOT_USERNAME}?start=download_{log_msg.id}"
    storagex = await short_link(storage, user)
    stream_linkx = f"{random.choice(Domain.CLOUDFLARE_URLS)}watch/{str(log_msg.id)}?hash={get_hash(log_msg)}"
    stream_link = await short_link(stream_linkx, user)
    online_link = await short_link(
        f"{random.choice(Domain.CLOUDFLARE_URLS)}dl/{str(log_msg.id)}?hash={get_hash(log_msg)}",
        user,
    )
    high_link = await short_link(
        f"{random.choice(Domain.MRAKFAST_URLS)}dl/{str(log_msg.id)}?hash={get_hash(log_msg)}",
        user,
    )
    try:
        # Create basic format dictionary
        basic_format_dict = {
            "file_name": "" if get_name(log_msg) is None else get_name(log_msg),
            "caption": "" if file_captionx is None else file_captionx,
            "file_size": (
                ""
                if humanbytes(get_media_file_size(m)) is None
                else humanbytes(get_media_file_size(m))
            ),
            "download_link": "" if online_link is None else online_link,
            "high_link": "" if online_link is None else online_link,
            "stream_link": "" if stream_link is None else stream_link,
            "storage_link": "" if storagex is None else storagex,
        }
        
        # Create safe format dictionary with all placeholders
        safe_format_dict = create_safe_format_dict(basic_format_dict, file_name, file_captionx)
        
        if caption_position == "links":
            await m.reply_text(
                text=c_caption.format(**safe_format_dict),
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥", url=stream_link)]]
                ),
            )
        elif caption_position == "files":
            await c.send_cached_media(
                chat_id=m.from_user.id,
                file_id=mediax.file_id,
                caption=c_caption.format(**safe_format_dict),
            )
        await log_msg.reply_text(
            text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n **Fɪʟᴇ Uɴɪǫᴜᴇ ID:** {mediax.file_unique_id}\n**Stream ʟɪɴᴋ :** {stream_linkx}\n**High ʟɪɴᴋ :** {high_link}\n**Storage ʟɪɴᴋ :** {storage}",
            disable_web_page_preview=True,
            quote=True,
        )

    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(
            chat_id=Telegram.ELOG_CHANNEL,
            text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`",
            disable_web_page_preview=True,
        )

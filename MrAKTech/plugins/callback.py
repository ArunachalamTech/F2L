import asyncio
import time
import datetime
import shutil
import psutil
from shortzy import Shortzy
from validators import domain

from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from MrAKTech import StreamBot, work_loads, multi_clients, cdn_count
from MrAKTech.config import Telegram
from MrAKTech.database.u_db import u_db
from MrAKTech.tools.txt import tamilxd, BUTTON
from MrAKTech.tools.utils_bot import readable_time, get_readable_file_size, temp, is_check_admin

@StreamBot.on_callback_query()
async def cb_handler(bot, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    userxdb = await u_db.get_user_details(user_id)
    # Callback started
    if data == "start":
        await query.message.edit_text(
            text=(tamilxd.START_TXT.format(query.from_user.mention)),
            disable_web_page_preview=True,
            reply_markup=BUTTON.START_BUTTONS
        )

    elif data == "help":
        await query.message.edit_text(
            text=tamilxd.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=BUTTON.HELP_BUTTONS
        )

    elif data == "owner":
        await query.message.edit_text(
            text=tamilxd.OWNER_INFO,
            disable_web_page_preview=True,
            reply_markup=BUTTON.OWNER_BUTTONS
        )
    elif data == "about":
        await query.message.edit_text(
            text=tamilxd.ABOUT_TXT,
            disable_web_page_preview=True,
            reply_markup=BUTTON.ABOUT_BUTTONS
        )

    elif data == "dev":
        m=await query.message.reply_sticker("CAACAgIAAxkBAAEJ8bxk0L2LAm0P4AABCIUXG6g7V03RTTQAAoAOAALUdQlKzIMOAcx1iKkwBA")
        await asyncio.sleep(3)
        await m.delete()
        caption = tamilxd.DEV_TXT
        tamil=await query.message.reply_photo(
            photo="https://telegra.ph/file/4e48e88fe9811add5fb22.jpg",
            caption=caption,
            reply_markup=InlineKeyboardMarkup([[
               #InlineKeyboardButton("♙ ʜᴏᴍᴇ", callback_data = "start"),
               InlineKeyboardButton("✗ Close", callback_data = "close")
               ]]
            )
        )
        await asyncio.sleep(1600)
        await tamil.delete()
        await query.message.delete()

    elif data == "source":
        m=await query.message.reply_sticker("CAACAgUAAxkBAAEBlVBkoEL0LKGBhqNxTtVM_Ti0QHnO_AAC5wQAAo6i-VUZIF0fRfvjmx4E")
        await asyncio.sleep(2)
        await m.delete()
        tamil=await query.message.reply_photo(
            photo="https://graph.org/file/306e4f62551e994ee6792.jpg",
            caption=tamilxd.SOURCE_TXT,
            reply_markup=BUTTON.SOURCE_BUTTONS
        )
        await asyncio.sleep(10)
        await tamil.delete()
        await query.message.delete()

    elif data == "don":
        m=await query.message.reply_sticker("CAACAgUAAxkBAAEBlVBkoEL0LKGBhqNxTtVM_Ti0QHnO_AAC5wQAAo6i-VUZIF0fRfvjmx4E")
        await asyncio.sleep(3)
        await m.delete()
        tamil=await query.message.reply_photo(
            photo="https://telegra.ph/file/d6e78fb5f4288e91be748.jpg",
            caption=(tamilxd.DONATE_TXT),
            reply_markup=BUTTON.DONATE_BUTTONS,
        )
        await asyncio.sleep(1800)
        await tamil.delete()
        await query.message.delete()

    ########## USERS MAIN BOT DETAILS START ########

    elif data in ['settings', 'toggle_mode', 'storage_mode']:
        mode = await u_db.get_uploadmode(user_id)
        # modex = await u_db.get_storagemode(user_id)
        if data == "toggle_mode":
            if not mode:
                mode = "links"
            elif mode == "links":
                mode = "files"
            else:
                # mode = None
                mode = "links"
            await u_db.change_uploadmode(user_id, mode)
        # if data == "storage_mode":
        #     if not modex:
        #         modex = "Off"
        #     elif modex == "Off":
        #         modex = "On"
        #     else:
        #      #mode = None
        #         modex = "Off"
        #     await u_db.change_storagemode(user_id, modex)

        # button = [[
        #     InlineKeyboardButton(
        #         "✅ Custom caption" if userxdb['caption'] is not None else "📝 Custom caption",
        #         callback_data="custom_caption"
        #     )
        #     ],[
        #     InlineKeyboardButton(
        #         "✅ Custom shortner" if userxdb['shortener_url'] and userxdb['shortener_api'] is not None else "🖼️ Custom shortner",
        #         callback_data="custom_shortner"
        #     )
        #     ],[
        #     InlineKeyboardButton('📤 Upload mode', callback_data="toggle_mode"),
        #     InlineKeyboardButton(mode if mode else "Links", callback_data="toggle_mode")
        #     ],[
        #     InlineKeyboardButton('🛠️ Reset settings', callback_data="reset_setting"),
        #     ], [
        #     InlineKeyboardButton('Close ✗', callback_data="close")
        #     ]]

        #
        buttons = []
        buttons.append([InlineKeyboardButton(
            "✅ Custom Caption" if userxdb['caption'] != tamilxd.STREAM_MSG_TXT else "📝 Custom Caption",
            callback_data="custom_caption"
        )])
        buttons.append([InlineKeyboardButton(
            "✅ Custom Shortner" if userxdb['shortener_url'] and userxdb[
                'shortener_api'] is not None else "🖼️ Custom Shortner",
            callback_data="custom_shortner"
        )])
        auto_extract = userxdb.get('auto_extract', True)
        buttons.append([InlineKeyboardButton(
            "✅ Auto Extract" if auto_extract else "❌ Auto Extract",
            callback_data="toggle_extract"
        )])
        buttons.append([InlineKeyboardButton('📤 Upload Mode', callback_data="toggle_mode"),
                        InlineKeyboardButton(mode if mode else "Links", callback_data="toggle_mode")])
        if await u_db.is_settings(user_id):
            buttons.append([InlineKeyboardButton('🛠️ Reset Settings', callback_data="reset_setting")])
        buttons.append([InlineKeyboardButton('Close', callback_data="close")])
        await query.message.edit_text(
            text=tamilxd.SETTINGS_TXT.format(CAPTION="✅ Exists" if userxdb["caption"] is not None else "❌ Not Exists",
                                             URLX=userxdb["shortener_url"] if userxdb["shortener_url"] is not None else "❌ Not Exists",
                                             APIX=userxdb["shortener_api"] if userxdb["shortener_api"] is not None else "❌ Not Exists",
                                             STORAGEX=userxdb["storage"],
                                             METHODX=userxdb["method"],
                                             AUTO_EXTRACT="✅ Enabled" if userxdb.get("auto_extract", True) else "❌ Disabled"),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True)

    elif data == "reset_setting":
        await query.message.edit_text(
            text=tamilxd.RESET_SETTINGS,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('Yes', callback_data="reset_settings"),
                InlineKeyboardButton('No', callback_data="settings"),
            ]]))

    elif data == "reset_settings":
        await u_db.reset_settings(user_id)
        await query.answer("Successfully settings resetted.", show_alert=True)
        buttons = []
        buttons.append([InlineKeyboardButton("📝 Custom caption", callback_data="custom_caption")])
        buttons.append([InlineKeyboardButton("🖼️ Custom shortner", callback_data="custom_shortner")])
        buttons.append([InlineKeyboardButton("✅ Auto Extract", callback_data="toggle_extract")])
        buttons.append([InlineKeyboardButton('📤 Upload mode', callback_data="toggle_mode"),
                        InlineKeyboardButton("Links", callback_data="toggle_mode")])
        buttons.append([InlineKeyboardButton('Close', callback_data="close")])
        await query.message.edit_text(
            text=tamilxd.SETTINGS_TXT.format(CAPTION="❌ Not Exists",
                                             URLX="❌ Not Exists",
                                             APIX="❌ Not Exists",
                                             METHODX="Links",
                                             AUTO_EXTRACT="✅ Enabled"),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True)

    elif data == "custom_caption":
        buttons = []
        if userxdb['caption'] is not None:
            buttons.append([InlineKeyboardButton('Show caption', callback_data="show_caption")])
            buttons.append([InlineKeyboardButton('Default caption', callback_data="delete_caption"),
                            InlineKeyboardButton('Change caption', callback_data="add_caption")])
        else:
            buttons.append([InlineKeyboardButton('Set caption', callback_data="add_caption")])
        buttons.append([InlineKeyboardButton('≺≺ Back', callback_data="settings"),
                        InlineKeyboardButton('Close', callback_data="close")])
        await query.message.edit_text(
            text=tamilxd.CUSTOM_CAPTION_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "custom_shortner":
        buttons = []
        if userxdb['shortener_url'] and userxdb['shortener_api'] is not None:
            buttons.append([InlineKeyboardButton('Show shortner', callback_data="show_shortner")])
            buttons.append([InlineKeyboardButton('Delete shortner', callback_data="delete_shortner"),
                            InlineKeyboardButton('Change shortner', callback_data="add_shortner")])
        else:
            buttons.append([InlineKeyboardButton('Set shortner', callback_data="add_shortner")])
        buttons.append([InlineKeyboardButton('≺≺ Back', callback_data="settings"),
                        InlineKeyboardButton('Close', callback_data="close")])
        await query.message.edit_text(
            text=tamilxd.CUSTOM_SHORTNER_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "add_caption":
        await query.message.delete()
        try:
            tamil = await bot.send_message(query.message.chat.id, "Send your custom caption\n/cancel - <code>Cancel this process</code>")
            caption = await bot.listen(chat_id=user_id, timeout=300)
            if caption.text == "/cancel":
                await caption.delete()
                return await tamil.edit_text("<b>Your process is canceled!</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_caption")]]))
            try:
                caption.text.format(file_name='', file_size='', caption='', download_link='', stream_link='', storage_link='', quality='', season='', episode='')
            except KeyError as e:
                await caption.delete()
                return await tamil.edit_text(f"<b><u>Wrong filling</u> \n\n<code>{e}</code> \n\n Used in your caption. change it.</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_caption")]]))
            await u_db.set_caption(user_id, caption.text)
            await caption.delete()
            await tamil.edit_text("<b>Successfully added your custon caption!...</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_caption")]]))
        except asyncio.exceptions.TimeoutError:
            await tamil.edit_text('Process has been automatically cancelled.', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_caption")]]))

    elif data == "add_shortner":
        await query.message.delete()
        try:
            tamil = await bot.send_message(query.message.chat.id, "<b>Please provide your custom shortener URL\nEg: <code>dalink.in</code>\n/cancel - <code>Cancel this process</code></b>")
            url_input = await bot.listen(chat_id=user_id, timeout=300)
            if url_input.text == "/cancel":
                await url_input.delete()
                return await tamil.edit_text("<b>Your process is canceled!</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_shortner")]]))
            elif not domain(url_input.text):
                await url_input.delete()
                return await tamil.edit_text("<b>Invalid domain format. please provide a valid domain.</b>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_shortner")]]))
            try:
                # await u_db.set_shortner_url(user_id, url_input.text)
                await url_input.delete()
                await tamil.delete()
                tamil1 = await bot.send_message(query.message.chat.id, f"<b> https://{url_input.text}/member/tools/quick \n\nPlease provide your custom shortener API \n Eg: <code>88f4e0fc522facab5fef40d69f4114c260facc9b</code></b>")
                api = await bot.listen(chat_id=user_id)
                try:
                    shortzy = Shortzy(api_key=api.text, base_site=url_input.text)
                    link = Telegram.MAIN
                    await shortzy.convert(link)
                except Exception as e:
                    return await tamil1.edit_text(f"Your shortener API or URL is invalid, please check again! {e}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_shortner")]]))
                await u_db.set_shortner_url(user_id, url_input.text)
                await u_db.set_shortner_api(user_id, api.text)
                await api.delete()
                await tamil1.edit_text("<b>Successfully added your custon shortener!...</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_shortner")]]))
            except Exception as e:
                print(f"Error fetching user: {e}")
            return
        except asyncio.exceptions.TimeoutError:
            await tamil.edit_text('Process has been automatically cancelled.', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_shortner")]]))

    elif data =="show_caption":
        if len(userxdb['caption']) > 170:
            await query.message.edit_text(
                text=userxdb['caption'],
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="custom_caption")]])
            )
        else:
            await query.answer(f"Your custom caption:\n\n{userxdb['caption']}", show_alert=True)

    elif data == "delete_caption":
        if not userxdb['caption']:
            return await query.answer("Nothing will found to delete.", show_alert=True)
        await u_db.set_caption(query.from_user.id, tamilxd.STREAM_TXT)
        return await query.answer("Caption removed suppessfully!", show_alert=True)

    elif data == "toggle_extract":
        user_id = query.from_user.id
        auto_extract = await u_db.get_auto_extract(user_id)
        new_status = not auto_extract
        await u_db.set_auto_extract(user_id, new_status)
        
        buttons = []
        buttons.append([
            InlineKeyboardButton(
                "✅ Enable Auto Extract" if not new_status else "❌ Disable Auto Extract",
                callback_data="toggle_extract"
            )
        ])
        buttons.append([InlineKeyboardButton("Close", callback_data="close")])
        
        status = "Enabled" if new_status else "Disabled"
        await query.message.edit_text(
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
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    elif data == "show_examples":
        example_text = """<b><u>📝 CAPTION EXAMPLES WITH SMART AUTO EXTRACTION</u></b>

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

<b>🧠 Smart Extraction Features:</b>
• Checks both filename AND original caption
• Uses best available information from both sources
• Falls back gracefully when data is missing
• Automatically combines results for maximum accuracy

<b>💡 Note:</b> These placeholders will be automatically replaced with the best extracted information from your files!"""
        
        await query.message.edit_text(
            example_text,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔍 Configure Auto Extract", callback_data="toggle_extract"),
                InlineKeyboardButton("Close", callback_data="close")
            ]])
        )

    elif data =="show_shortner":
        if not userxdb['shortener_url'] and userxdb['shortener_api']:
            return await query.answer("Your didn't added any custom shortner URL", show_alert=True)
        await query.answer(f"Your custom shortner: \n\nURL - {userxdb['shortener_url']} \nAPI - {userxdb['shortener_api']}", show_alert=True)

    elif data == "delete_shortner":
        buttons = []
        if not userxdb['shortener_url'] and userxdb['shortener_api']:
            return await query.answer("Nothing will found to delete.", show_alert=True)
        await u_db.set_shortner_url(query.from_user.id, None)
        await u_db.set_shortner_api(query.from_user.id, None)
        await query.answer("Shortener removed successfully!", show_alert=True)
        #
        buttons.append([InlineKeyboardButton('Set shortener', callback_data="add_shortner")])
        buttons.append([InlineKeyboardButton('≺≺ Back', callback_data="settings"),
                        InlineKeyboardButton('Close', callback_data="close")])
        return await query.message.edit_text(
            text=tamilxd.CUSTOM_SHORTNER_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "main":
        await query.message.edit_text(
            "<b>Change your settings as your wish.</b>",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('Personal settings', callback_data='settings'),
                ],[
                InlineKeyboardButton('Channels settings', callback_data='channels')
                ],[
                InlineKeyboardButton('≺≺ Close', callback_data='close')
                ]]))

    elif data == "channels":
        buttons = []
        channels = await u_db.get_user_channels(user_id)
        for channel in channels:
            buttons.append([InlineKeyboardButton(f"{channel['title']}",
                         callback_data=f"editchannels_{channel['chat_id']}")])
        buttons.append([InlineKeyboardButton('✚ Add channel ✚',
                      callback_data="addchannel")])
        buttons.append([InlineKeyboardButton('≺≺ Back',
                      callback_data="main")])
        await query.message.edit_text(
            "<b><u>My channels</b></u>\n\n<b>You can manage your target chats in here.</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "addchannel":
        await query.message.delete()
        try:
            tamil = await bot.send_message(chat_id=query.message.chat.id, text=tamilxd.CHL_CHANNEL_ADD_TXT)
            chat_ids = await bot.listen(chat_id=user_id, timeout=60)
            if chat_ids.text=="/cancel":
                await chat_ids.delete()
                return await tamil.edit_text("<b>Your process has been canceled.</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="channels")]]))
            if not chat_ids.forward_date:
                await chat_ids.delete()
                return await tamil.edit_text("<b>This is not a forward message.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="channels")]]))
            chat_id = chat_ids.forward_from_chat.id
            if (await bot.get_chat(chat_id)).type != enums.ChatType.CHANNEL:
                await chat_ids.delete()
                return await tamil.edit_text("This is not a channel message.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="channels")]]))
            title = chat_ids.forward_from_chat.title

            if not await is_check_admin(bot, chat_id, query.from_user.id):
                await chat_ids.delete()
                return await tamil.edit_text('You not admin in that channel.', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="channels")]]))
            else:
                username = chat_ids.forward_from_chat.username
                username = "@" + username if username else "private"
                chat = await u_db.add_channel(int(user_id), int(chat_id), title, username)
                await chat_ids.delete()
                await tamil.edit_text("<b>Successfully Updated.</b>" if chat else "<b>This channel already added!...</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="channels")]]))
        except asyncio.exceptions.TimeoutError:
            await tamil.edit_text('Process has been automatically cancelled.', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="channels")]]))

    elif data.startswith(("editchannels", "chlmode")):
        chat_id = data.split('_')[1]
        chat = await u_db.get_chl_settings(chat_id)
        chatx = await bot.get_chat(int(chat_id))
        mode = chat['method']
        if data.startswith("chlmode"):
            if not mode:
                mode = "Button"
            elif mode == "Button":
                mode = "Caption"
            else:
                mode = "Button"
            await u_db.update_chl_settings(chat_id, 'method', mode)
        buttons = []
        buttons.append([InlineKeyboardButton(
            "✅  Custon Caption" if chat['caption'] != tamilxd.STREAM_TXT else "📝 Custon Caption",
            callback_data=f"chlcustomcaption_{chat_id}")])
        buttons.append([InlineKeyboardButton(
            "✅  Custon  Shortener" if chat['url'] and chat['api'] is not None else "🖼️ Custon  Shortener",
            callback_data=f"chlcustomshortner_{chat_id}")])
        buttons.append([InlineKeyboardButton('📤 Uploed Mode', callback_data=f"chlmode_{chat_id}"),
                        InlineKeyboardButton(mode if mode else "Button", callback_data=f"chlmode_{chat_id}")])
        if await u_db.is_chl_settings(chat_id):
            buttons.append([InlineKeyboardButton('Delete', callback_data=f"removechannelx_{chat_id}"),
                            InlineKeyboardButton('Reset', callback_data=f"resetchatsetting_{chat_id}")])
        else:
            buttons.append([InlineKeyboardButton('Delete', callback_data=f"removechannelx_{chat_id}")])
        buttons.append([InlineKeyboardButton('≺≺ Back', callback_data="channels")])
        #
        await query.message.edit_text(text=tamilxd.CHL_CHANNEL_DETAILS_TXT.format(TITLEX=chatx.title,
                                                                                CHANNEL_DIX=chat_id,
                                                                                USERNAMEX="@" + chatx.username if chatx.username else "private",
                                                                                CAPTION="✅ Exists" if chat["caption"] is not None else "❌ Not Exists",
                                                                                APIX=chat["api"] if chat["api"] is not None else "❌ Not Exists",
                                                                                URLX=chat["url"] if chat["url"] is not None else "❌ Not Exists",
                                                                                METHODX=chat["method"]),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True)

    elif data.startswith("removechannelx"):
        chat_id = data.split('_')[1]
        chat = await u_db.get_channel_details(user_id, chat_id)
        await query.message.edit_text(
            f"<b>Do you confirm ??\n\n You delete your : {chat['title']} channel?</b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Confirm ✅', callback_data=f"xremovechannel_{chat_id}")],[InlineKeyboardButton('≺≺ Back', callback_data=f"editchannels_{chat_id}")]]))

    elif data.startswith("xremovechannel"):
        chat_id = data.split('_')[1]
        await u_db.remove_channel(user_id, chat_id)
        await query.answer("Successfully deleted your channel.", show_alert=True)
        buttons = []
        channels = await u_db.get_user_channels(user_id)
        for channel in channels:
            buttons.append([InlineKeyboardButton(f"{channel['title']}",
                         callback_data=f"editchannels_{channel['chat_id']}")])
        buttons.append([InlineKeyboardButton('✚ Add channel ✚',
                      callback_data="addchannel")])
        buttons.append([InlineKeyboardButton('≺≺ Back',
                      callback_data="main")])
        await query.message.edit_text(
            "<b><u>My channels</b></u>\n\n<b>You can manage your chats in here.</b>",
        reply_markup=InlineKeyboardMarkup(buttons))
        #

    elif data.startswith("resetchatsetting"):
        chat_id = data.split('_')[1]
        await query.message.edit_text(
            text=tamilxd.RESET_SETTINGS,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('Yes', callback_data=f"xresetchatsettings_{chat_id}"),
                    InlineKeyboardButton('No', callback_data=f"editchannels_{chat_id}")
                ]]
            )
        ) 

    elif data.startswith("xresetchatsettings"):
        chat_id = data.split('_')[1]
        await u_db.reset_chl_settings(chat_id)
        await query.answer("Successfully resetted your channel settings.", show_alert=True)
        #
        chat = await u_db.get_chl_settings(chat_id)
        chatx = await bot.get_chat(chat_id)
        #
        return await query.message.edit_text(
            text=tamilxd.CHL_CHANNEL_DETAILS_TXT.format(
                TITLEX=chatx.title,
                CHANNEL_DIX=chat_id,
                USERNAMEX="@" + chatx.username if chatx.username else "private",
                CAPTION="❌ Not Exists",
                APIX="❌ Not Exists",
                URLX="❌ Not Exists",
                METHODX=chat["method"],
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Custon caption", callback_data=f"chlcustomcaption_{chat_id}")
                ],[InlineKeyboardButton("Custon  Shortener", callback_data=f"chlcustomshortner_{chat_id}")
                ],[InlineKeyboardButton("📤 Uploed Mode", callback_data=f"chlmode_{chat_id}"),
                   InlineKeyboardButton("Button", callback_data=f"chlmode_{chat_id}")
                ],[InlineKeyboardButton("Delete", callback_data=f"removechannelx_{chat_id}")
                ],[InlineKeyboardButton("≺≺ Back", callback_data="channels")]]
            ),
            disable_web_page_preview=True,
        )
        #

    elif data.startswith("chlcustomcaption"):
        chat_id = data.split('_')[1]
        chat = await u_db.get_chl_settings(chat_id)
        await query.message.edit_text(
            text=tamilxd.CHL_CUSTOM_CAPTION_TXT.format(CAPTIONX=chat['caption']),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton("Show Caption", callback_data=f"chlshowcaption_{chat_id}")
                ],[
                InlineKeyboardButton('Default Caption', callback_data=f"chldelcaption_{chat_id}"),
                InlineKeyboardButton("Change Caption", callback_data=f"chladdcaption_{chat_id}")
                ],[
                InlineKeyboardButton('Close', callback_data="close"),
                InlineKeyboardButton('≺≺ Back', callback_data=f"editchannels_{chat_id}")
                ]]
            ))

    elif data.startswith("chlcustomshortner"):
        buttons = []
        chat_id = data.split('_')[1]
        chat = await u_db.get_chl_settings(chat_id)
        if chat['api'] and chat['url'] is not None:
            buttons.append([InlineKeyboardButton('Change shortener', callback_data=f"chladdshortner_{chat_id}"),
                            InlineKeyboardButton('Delete shortener', callback_data=f"chldelshortner_{chat_id}")])
        else:
            buttons.append([InlineKeyboardButton('Set shortener', callback_data=f"chladdshortner_{chat_id}")])
        buttons.append([InlineKeyboardButton('≺≺ Back', callback_data=f"editchannels_{chat_id}"),
                        InlineKeyboardButton('Close', callback_data="close")])
        await query.message.edit_text(
            text=tamilxd.CHL_SHORTNER_TXT.format(
                URLX=chat["url"] if chat["url"] is not None else "❌ Not Exists",
                APIX=chat["api"] if chat["api"] is not None else "❌ Not Exists",
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    elif data.startswith("chladdcaption"):
        chat_id = data.split('_')[1]
        await query.message.delete()
        try:
            tamil = await bot.send_message(query.message.chat.id, f"Send your custom caption\n/cancel - <code>Cancel this process</code> \n\n {chat_id}")
            caption = await bot.listen(chat_id=user_id, timeout=120)
            if caption.text == "/cancel":
                await caption.delete()
                return await tamil.edit_text("<b>Your process is canceled!</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data=f"chlcustomcaption_{chat_id}")]]))
            try:
                caption.text.format(file_name='', file_size='', caption='', download_link='', stream_link='', storage_link='', quality='', season='', episode='')
            except KeyError as e:
                await caption.delete()
                return await tamil.edit_text(
                    f"<b><u>Wrong filling:</u><code>{e}</code>\n\n Used in your caption. change ɪᴛ.</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data=f"chlcustomcaption_{chat_id}")]]))
            await u_db.update_chl_settings(chat_id, 'caption', caption.text)
            await caption.delete()
            await tamil.edit_text("<b>Successfully added your cutom caption!...</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data=f"chlcustomcaption_{chat_id}")]]))
        except asyncio.exceptions.TimeoutError:
            await tamil.edit_text('Process has been automatically cancelled.', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="channels")]]))

    elif data.startswith("chladdshortner"):
        await query.message.delete()
        chat_id = data.split('_')[1]
        chl = await bot.get_chat(int(chat_id))
        try:
            tamil1 = await bot.send_message(query.message.chat.id, "<b>Please provide your custom shortener URL\nEg: <code>dalink.in</code>\n/cancel - <code>Cancel this process</code></b>")
            url_input = await bot.listen(chat_id=user_id, timeout=300)
            if url_input.text == "/cancel":
                await url_input.delete()
                return await tamil1.edit_text("<b>Your process is canceled!</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data=f"chlcustomshortner_{chat_id}")]]))
            elif not domain(url_input.text):
                await url_input.delete()
                return await tamil1.edit_text("<b>Invalid domain format. please provide a valid domain.</b>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data=f"chlcustomshortner_{chat_id}")]]))
            try:
                await url_input.delete()
                await tamil1.delete()
                tamil2 = await bot.send_message(query.message.chat.id, f"<b> https://{url_input.text}/member/tools/quick \n\nPlease provide your custom shortner API\n Eg: <code>88f4e0fc522facab5fef40d69f4114c260facc9b</code></b>")
                api_input = await bot.listen(chat_id=user_id)
                try:
                    shortzy = Shortzy(api_key=api_input.text, base_site=url_input.text)
                    link = Telegram.MAIN
                    await shortzy.convert(link)
                except Exception as e:
                    return await tamil2.edit_text(f"Your shortener API or URL is invalid, please chack again! {e}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data=f"chlcustomshortner_{chat_id}")]]))
                await u_db.update_chl_settings(chat_id, 'url', url_input.text)
                await u_db.update_chl_settings(chat_id, 'api', api_input.text)
                await api_input.delete()
                await tamil2.edit_text(f"<b>Successfully changed shortener for {chl.title} - {chl.id} to\n\nURL - {url_input.text}\nAPI - {api_input.text}</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data=f"chlcustomshortner_{chat_id}")]]))
            except Exception as e:
                print(f"Error fetching user: {e}")
            return
        except asyncio.exceptions.TimeoutError:
            await tamil1.edit_text('Process has been automatically cancelled.', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data="channels")]]))

            #
    elif data.startswith("chlshowcaption"):
        chat_id = data.split('_')[1]
        settings = await u_db.get_chl_settings(chat_id)
        if len(settings['caption']) > 170:
            await query.message.edit_text(
                text=settings['caption'],
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('≺≺ Back', callback_data=f"chlcustomcaption_{chat_id}")]])
            )
        else:
            await query.answer(f"Your custom caption:\n\n{settings['caption']}", show_alert=True)

    elif data.startswith("chldelcaption"):
        chat_id = data.split('_')[1]
        settings = await u_db.get_chl_settings(chat_id)
        if not settings['caption']:
            return await query.answer("Nothing will found to delete.", show_alert=True)
        await u_db.update_chl_settings(chat_id, 'caption', tamilxd.STREAM_TXT)
        return await query.answer("caption removed successfully!'", show_alert=True)

    elif data.startswith("chlshowshortner"):
        chat_id = data.split('_')[1]
        settings = await u_db.get_chl_settings(chat_id)
        if not settings['api'] and settings['url']:
            return await query.answer("You didn't added any custom shortener URL or API.", show_alert=True)
        await query.answer(f"Your custom Shortner: \n\nURL - {settings['url']} \nAPI - {settings['api']}", show_alert=True)

    elif data.startswith("chldelshortner"):
        chat_id = data.split('_')[1]
        settings = await u_db.get_chl_settings(chat_id)
        if not settings['api'] and settings['url']:
            return await query.answer("Nothing will found to delete.", show_alert=True)
        await u_db.update_chl_settings(chat_id, 'api', None)
        await u_db.update_chl_settings(chat_id, 'url', None)
        await query.answer("Shortener removed successfully!", show_alert=True)
        return await query.message.edit_text(
            text=tamilxd.CHL_SHORTNER_TXT.format(URLX="❌ Not Exists",APIX="❌ Not Exists"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('Set shortener', callback_data=f"chladdshortner_{chat_id}")
                ],[
                InlineKeyboardButton('Close', callback_data="close"),
                InlineKeyboardButton('≺≺ Back', callback_data=f"editchannels_{chat_id}")
                ]]))

    ######################## DELETE CALLBACKS ##########################

    elif data.startswith("delete"):
        file_id = data.split('_')[1]
        try:
            await StreamBot.delete_messages(chat_id=int(Telegram.FLOG_CHANNEL), message_ids=int(file_id))
            await query.answer("File Deleted successfully!", show_alert=True)
            return await bot.edit_message_reply_markup(
                chat_id=query.message.chat.id,
                message_id=query.message.id,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Deleted ✅", callback_data = "is_deleted"),
                    InlineKeyboardButton("Close", callback_data = "close")]]
                ))
        except Exception as e:  # noqa: E722
            print(e)
            # await query.message.delete()

    elif data.startswith("verify"):
        try:
            await query.answer("Verified thiss files data!", show_alert=True)
            return await bot.edit_message_reply_markup(
                chat_id=query.message.chat.id,
                message_id=query.message.id,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Verified ✅", callback_data = "is_verified"),
                    InlineKeyboardButton("Close", callback_data = "close")]]
                ))
        except Exception as e:  # noqa: E722
            print(e)

    elif data == 'is_verified':
        await query.answer("Already this file verified ✅!", show_alert=True)

    elif data == 'is_deleted':
        await query.answer("Already this file deleted ✅!", show_alert=True)

    ######################## OTHAR CALLBACKS ##########################

    elif data== "stats":
        ax = await query.message.edit_text('Refreshing.....')
        STATUS_TXT = f"""**╭──────❪ 𝗦𝗧𝗔𝗧𝗨𝗦 ❫─────⍟
│
├👤 Active Users : {await u_db.total_users_count()}
│
├👤 InActive Users : {await u_db.itotal_users_count()}
│
├🤖 Total Bots : {await u_db.total_users_bots_count()} 
│
├🤖 Total Channel : {await u_db.total_channels_count()} 
│
├🚫 Banned Users : {await u_db.total_banned_users_count()}
│
╰───────────────────⍟**"""
        await ax.edit_text(text=STATUS_TXT,
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton("Refresh 🔃", callback_data = "stats"),
                            InlineKeyboardButton("Close ✗", callback_data = "close")]]),
                        parse_mode=enums.ParseMode.MARKDOWN)

    elif data == "status":
        ax = await query.message.edit_text('Refreshing.......')
        india_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        total, used, free = shutil.disk_usage('.')
        bot_workloads = sorted(work_loads.items(), key=lambda x: x[1], reverse=True)
        v2_workloads = sorted(cdn_count.items(), key=lambda x: x[1], reverse=True)
        bot_workload_dict = dict(("bot" + str(c + 1), workload)for c, (_, workload) in enumerate(bot_workloads))
        v2_workload_dict = dict(("v2" + str(c + 1), workload)for c, (_, workload) in enumerate(v2_workloads))
        await ax.edit_text(
                text=tamilxd.STATUS_TXT.format(
                    date=india_time.strftime("%d-%B-%Y"),
                    time=india_time.strftime("%I:%M:%S %p"),
                    day=india_time.strftime("%A"),
                    utc_offset=india_time.strftime("%:z"),
                    #
                    currentTime=readable_time((time.time() - temp.START_TIME)),
                    total=get_readable_file_size(total),
                    used=get_readable_file_size(used),
                    free=get_readable_file_size(free),
                    cpuUsage=psutil.cpu_percent(interval=0.5),
                    memory=psutil.virtual_memory().percent,
                    disk=psutil.disk_usage('/').percent,
                    sent=get_readable_file_size(psutil.net_io_counters().bytes_sent),
                    recv=get_readable_file_size(psutil.net_io_counters().bytes_recv),
                    v1_traffic_total=sum(workload for _, workload in bot_workloads), # for this total v1 workload
                    v2_traffic_total=sum(workload for _, workload in v2_workloads), # for this total v2 workload
                    multi_clients=len(multi_clients),
                    v1_traffic_me=bot_workload_dict.get("bot1", 0), # for this bot v1 workload
                    v2_traffic_me=v2_workload_dict.get("bot1", 0), # for this bot v1 workload
                ),
                reply_markup=InlineKeyboardMarkup(
                    [[
                    InlineKeyboardButton("Refresh 🔃", callback_data = "status"),
                    InlineKeyboardButton("Close ✗", callback_data = "close")
                   ]]
               ),
           )

    ####################### OTHAR CALLBACKS ##########################

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:  # noqa: E722
            await query.message.delete()

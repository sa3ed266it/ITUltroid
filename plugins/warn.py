# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available

•`{i}warn <reply to user> <reason>`
    Gives Warn.

•`{i}resetwarn <reply to user>`
    To reset All Warns.

•`{i}warns <reply to user>`
   To Get List of Warnings of a user.

•`{i}setwarn <warn count> | <ban/mute/kick>`
   Set Number in warn count for warnings
   After putting " | " mark put action like ban/mute/kick
   Its Default 3 mute
   Example : `.setwarn 5 | mute`

"""

from pyUltroid.dB.warn_db import add_warn, reset_warn, warns

from . import eor, get_string, inline_mention, udB, ultroid_cmd


@ultroid_cmd(
    pattern="warn( (.*)|$)",
    manager=True,
    groups_only=True,
    admins_only=True,
)
async def warn(e):
    ultroid_bot = e.client
    reply = await e.get_reply_message()
    if len(e.text) > 5 and " " not in e.text[5]:
        return
    if reply:
        user = reply.sender_id
        reason = e.text[5:] if e.pattern_match.group(1).strip() else ""
    else:
        try:
            user = e.text.split()[1]
            if user.startswith("@"):
                ok = await ultroid_bot.get_entity(user)
                user = ok.id
            else:
                user = int(user)
        except BaseException:
            return await e.eor("Reply To A User", time=5)
        try:
            reason = e.text.split(maxsplit=2)[-1]
        except BaseException:
            reason = ""
    count, r = warns(e.chat_id, user)
    r = f"{r}|$|{reason}" if r else reason
    try:
        x = udB.get_key("SETWARN")
        number, action = int(x.split()[0]), x.split()[1]
    except BaseException:
        number, action = 3, "كتمه"
    if ("حظره" or "طرده" or "كتمه") not in action:
        action = "كتمه"
    if count + 1 >= number:
        if "حظره" in action:
            try:
                await ultroid_bot.edit_permissions(e.chat_id, user, view_messages=False)
            except BaseException:
                return await e.eor("`Something Went Wrong.`", time=5)
        elif "طرده" in action:
            try:
                await ultroid_bot.kick_participant(e.chat_id, user)
            except BaseException:
                return await e.eor("`Something Went Wrong.`", time=5)
        elif "كتمه" in action:
            try:
                await ultroid_bot.edit_permissions(
                    e.chat_id, user, until_date=None, send_messages=False
                )
            except BaseException:
                return await e.eor("`Something Went Wrong.`", time=5)
        add_warn(e.chat_id, user, count + 1, r)
        c, r = warns(e.chat_id, user)
        ok = await ultroid_bot.get_entity(user)
        user = inline_mention(ok)
        r = r.split("|$|")
        text = f"المستخدم : {user}\n تم {action}\n بسبب حصوله على {count+1} تحذير.\n\n"
        for x in range(c):
            text += f"•**{x+1}.** {r[x]}\n"
        await e.eor(text)
        return reset_warn(e.chat_id, ok.id)
    add_warn(e.chat_id, user, count + 1, r)
    ok = await ultroid_bot.get_entity(user)
    user = inline_mention(ok)
    await eor(
        e,
        f"**عدد التحذيرات :** {count+1}/{number}\n**المستخدم :**{user}\n**خلى بالك بقا 🙂**\n\n**السبب** : {reason}",
    )


@ultroid_cmd(
    pattern="resetwarn( (.*)|$)",
    manager=True,
    groups_only=True,
    admins_only=True,
)
async def rwarn(e):
    reply = await e.get_reply_message()
    if reply:
        user = reply.sender_id
    else:
        try:
            user = e.text.split()[1]
            if user.startswith("@"):
                ok = await e.client.get_entity(user)
                user = ok.id
            else:
                user = int(user)
        except BaseException:
            return await e.eor("Reply To user")
    reset_warn(e.chat_id, user)
    ok = await e.client.get_entity(user)
    user = inline_mention(ok)
    await e.eor(f"Cleared All Warns of {user}.")


@ultroid_cmd(
    pattern="warns( (.*)|$)",
    manager=True,
    groups_only=True,
    admins_only=True,
)
async def twarns(e):
    reply = await e.get_reply_message()
    if reply:
        user = reply.from_id.user_id
    else:
        try:
            user = e.text.split()[1]
            if user.startswith("@"):
                ok = await e.client.get_entity(user)
                user = ok.id
            else:
                user = int(user)
        except BaseException:
            return await e.eor("Reply To A User", time=5)
    c, r = warns(e.chat_id, user)
    if c and r:
        ok = await e.client.get_entity(user)
        user = inline_mention(ok)
        r = r.split("|$|")
        text = f"User {user} Got {c} Warns.\n\n"
        for x in range(c):
            text += f"•**{x+1}.** {r[x]}\n"
        await e.eor(text)
    else:
        await e.eor("`No Warnings`")


@ultroid_cmd(pattern="setwarn( (.*)|$)", manager=True)
async def warnset(e):
    ok = e.pattern_match.group(1).strip()
    if not ok:
        return await e.eor("stuff")
    if "•" in ok:
        try:
            number, action = int(ok.split()[0]), ok.split()[1]
        except BaseException:
            return await e.eor(get_string("schdl_2"), time=5)
        if ("حظر" or "طرد" or "كتم") not in action:
            return await e.eor("`Only كتم / حظر / طرد option suported`", time=5)
        udB.set_key("SETWARN", f"{number} {action}")
        await e.eor(f"Done Your Warn Count is now {number} and Action is {action}")
    else:
        await e.eor(get_string("schdl_2"), time=5)

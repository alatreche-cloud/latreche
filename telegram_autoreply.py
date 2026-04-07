from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateStatusRequest
import asyncio
import time

api_id = 33023413
api_hash = "b1dea584f8b42c54aeb251a8ca657fda"

client = TelegramClient("session", api_id, api_hash)

last_active = 0

async def keep_offline():
    while True:
        try:
            await client(UpdateStatusRequest(offline=True))
        except Exception:
            pass
        await asyncio.sleep(1)

@client.on(events.NewMessage(outgoing=True))
async def track_activity(event):
    global last_active
    last_active = time.time()
    await client(UpdateStatusRequest(offline=True))

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if not event.is_private:
        return

    if time.time() - last_active > 300:
        await event.reply("هاشم غير متصل الآن، سيرد عليك لاحقًا")
        await client(UpdateStatusRequest(offline=True))

async def main():
    await client.start()
    client.loop.create_task(keep_offline())
    await client.run_until_disconnected()

while True:
    try:
        client.loop.run_until_complete(main())
    except Exception:
        time.sleep(5)

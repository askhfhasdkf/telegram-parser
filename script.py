import time
import asyncio
from pyrogram import Client, errors
from pyrogram.errors import FloodWait
from config import sc_db
import sys


user_id = sys.argv[1]
print(user_id)

api_id = int(sc_db.get_api_id(user_id))
print(api_id)

api_hash = f"{sc_db.get_hash(user_id)}"
print(api_hash)
phone_number = sc_db.get_phone_number(user_id)
print(phone_number)

app = Client(user_id,
             api_id=api_id,
             api_hash=api_hash,
             phone_number=phone_number,
             )


async def activate_bot():
    await app.connect()
    code = await app.send_code("+" + f"{phone_number}")
    time.sleep(15)
    await app.sign_in(phone_number=phone_number, phone_code_hash=code.phone_code_hash, phone_code=sc_db.get_code(user_id))


async def send_messages():
    await asyncio.sleep(30)
    print("start!!!")

    timer = 800
    start_time = time.time()

    while True:
        confirm_time = time.time() - start_time

        if confirm_time >= timer:
            break
        chats = sc_db.get_all_names(user_id)
        print(chats)
        for chat in chats:
            print(chat)
            try:
                await app.send_message(chat, f"{sc_db.get_text(user_id)}")
            except FloodWait as e:
                print(f"Waiting for {e.x} seconds due to FloodWait...")
                await asyncio.sleep(e.x)

        await asyncio.sleep(15)
        print("stopeddd")

    try:
        await app.stop()
        print(f"Скрипт остановлен пользователем {user_id}")
    except ConnectionError as e:
        print(f"{e} Скрипт остановлен пользователем {user_id}")
    except errors.exceptions.unauthorized_401.AuthKeyUnregistered:
        print("The key is not registered. Deleting the session file and prompting the user to log in again.")


async def main():
    activation_task = asyncio.create_task(activate_bot())
    messages_task = asyncio.create_task(send_messages())

    await asyncio.gather(activation_task, messages_task)


if __name__ == "__main__":
    asyncio.run(main())

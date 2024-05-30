import config as cfg
import markup as nav
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from db import Database
import asyncio


bot = Bot(token=cfg.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('defbysby.db')


class UserSpam(StatesGroup):
    api_id = State()
    api_hash = State()
    text = State()
    phone = State()
    cod = State()
    chat = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, f"привет, это тест бот от defbysby", reply_markup=nav.menu_start)


@dp.callback_query_handler(text='link')
async def cmd_link(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.send_message(user_id, f"в разработке!")


@dp.callback_query_handler(text='sendall')
async def cmd_sendall(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.send_message(user_id, f"вы попали в меню рассылки!", reply_markup=nav.spam_menu)


@dp.callback_query_handler(text='add_chat')
async def cmd_addchat(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.send_message(user_id, f"введите ваш чат для рассылки по примеру ниже\n"
                                    f"@defbysby = defbysby\n"
                                    f"без собаки")
    await UserSpam.chat.set()


@dp.message_handler(state=UserSpam.chat)
async def add_chat(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat'] = message.text
    db.add_chat(user_id=message.from_user.id, name=data['chat'])
    await bot.send_message(message.from_user.id, f"отлично\n"
                                                 f"готово")
    await state.finish()


@dp.callback_query_handler(text='spam')
async def cmd_spam(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.send_message(user_id, f"введите боту ваш api_id от аккаунта!")
    await UserSpam.api_id.set()


@dp.message_handler(state=UserSpam.api_id)
async def add_api_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_id'] = message.text
    await bot.send_message(message.from_user.id, f"отлично\n"
                                                 f"Введите ваш api_hash от вашего аккаунта")
    await UserSpam.api_hash.set()


@dp.message_handler(state=UserSpam.api_hash)
async def add_api_hash(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_hash'] = message.text
    await bot.send_message(message.from_user.id, f"отлично\n"
                                                 f"теперь ваш текст для спама")

    await UserSpam.text.set()


@dp.message_handler(state=UserSpam.text)
async def add_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await bot.send_message(message.from_user.id, f"введите ваш номер от аккаунта!")

    await UserSpam.phone.set()


@dp.message_handler(state=UserSpam.phone)
async def add_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    db.add_info_cfg(user_id=message.from_user.id, api_id=data['api_id'], api_hash=data['api_hash'], text=data['text'], phone=data['phone'])
    await bot.send_message(message.from_user.id, f"готово, ваш аккаунт успешно создан!")
    await state.finish()


@dp.callback_query_handler(text='start')
async def start_script(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id

        asyncio.create_task(run_script(user_id))

        await UserSpam.cod.set()
        await bot.send_message(callback.from_user.id, f"<b>Введите код который придет вам в телеграмм\n\nУ вас есть 20 секунуд!</b>", parse_mode='html')
    except Exception as e:
        print(e)
        await bot.send_message(callback.from_user.id, f'<b>Произошла ошибка!!</b>', parse_mode='html')


async def run_script(user_id):
    try:
        await asyncio.create_subprocess_exec('python', 'script.py', str(user_id))
    except Exception as e:
        print(e)


@dp.message_handler(state=UserSpam.cod)
async def load_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['cod'] = message.text
    await bot.send_message(message.from_user.id, f"<b>Если вы ввели верный код, ваша расслыка будет успешно запущена!</b>", parse_mode='html')
    db.add_code(user_id=message.from_user.id, code=data['cod'])
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

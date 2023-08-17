from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
import asyncio
import requests
import tokens
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tokens import bot_API
from aiogram.types import CallbackQuery
from sqlite import db_start, create_profile, edit_profile
from aiogram.types import ContentType


bot = Bot(token=bot_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



async def on_starup(_):
    await db_start()


@dp.message_handler(state="*", commands='Отменить')
async def cancle(message: types.message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await asyncio.sleep(0.6)
    await message.reply('Отменено', reply_markup=types.ReplyKeyboardRemove())


#Машина состояний
class Form(StatesGroup):
    name = State()
    last = State()


#Кнопки
b_in_gift = types.InlineKeyboardButton(text='Получить!', callback_data='Gift')
kb_gift = types.InlineKeyboardMarkup(resize_keyboard=True).add(b_in_gift)

b_yess = types.InlineKeyboardButton(text="Я посмотрел!", callback_data='pic')
kb_yess = types.InlineKeyboardMarkup(resize_keyboard=True).add(b_yess)

b_photo = KeyboardButton(text='Да, хочу!')
kb_photo = ReplyKeyboardMarkup(resize_keyboard=True).add(b_photo)

b_anket = types.InlineKeyboardButton(text='Жми, чтоб заполнить анкету!', url='https://forms.gle/H6ooBr4RgY8cizyt5')
kb_anket = types.InlineKeyboardMarkup(resize_keyboard=True).add(b_anket)


@dp.message_handler(state="*", commands=['start'])
async def start_function(message: types.message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='AgACAgIAAxkBAAICGWTb2WnjaxD3Af2NV1gM6qJJDWK7AAJL0TEbaObhSuujfmUo5xseAQADAgADeQADMAQ',
                         caption='Привет! Меня зовут Ефим. Я фитнес-тренер')
    await create_profile(user_id=message.from_user.id)
    await Form.name.set()
    await asyncio.sleep(0.5)
    await message.answer('Как я могу к Вам обращаться?')


@dp.message_handler(state=Form.name)
async def take_name(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await edit_profile(state, user_id=message.from_user.id)
    await message.answer(f"Рад знакомству, {data['name']}! Специально для тебя у меня есть подарок 🎁",
                         reply_markup=kb_gift)
    await state.finish()



@dp.callback_query_handler(state= '*', text='Gift')
async def give_gift(call: types.CallbackQuery):
    await call.message.answer(f"В этом видео я хочу поделиться своей тренировкой для рук!\n\n "
                              f"*ОБЯЗАТЕЛЬНО ПОСМОТРИ ЕГО* 👇🏻\n"
                              f"https://youtu.be/KucO4HabPcE", reply_markup=kb_yess, parse_mode="Markdown")
    #await call.message.answer(f"Хочешь также забрать тренировку в формате картинки?", reply_markup=kb_photo)
    await call.answer()


@dp.callback_query_handler(state="*", text='pic')
async def wanna_pic(call: CallbackQuery):
    await call.message.answer('Хочешь забрать тренировку в формате картинки?', reply_markup=kb_photo)
    await call.answer()


@dp.message_handler(state= "*", text='Да, хочу!')
async def photo(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='AgACAgIAAxkBAAIBemTb0bW3v_06ua6xGS3KB1puzq2_AAIs0TEbaObhSpL2WtEGjDDwAQADAgADeQADMAQ')
    await message.answer(text='Вот, держи!',
                         reply_markup=types.ReplyKeyboardRemove())
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='AgACAgIAAxkBAAIBmGTb0sCxoUnL6MT5vfWlQSUbGWovAAIq0TEbaObhSsTjCcFVAuvGAQADAgADeQADMAQ',
                         caption='Для тех, кто посмотрел видео я хочу сделать еще один бонус!')
    await asyncio.sleep(0.5)
    await message.answer(f"*БЕСПЛАТНЫЙ ФИТНЕС - РАЗБОР*\n\n"
                              f"где ты узнаешь 👇🏻\n\n"
                              f"1. Пошаговый план для реализации твоей цели. \n"
                              f"2. О секретах построения тренировочного процесса и плана питания.\n"
                              f"3. О том, как нам с клиентами удается приходить к результатам в кратчайшие сроки. ",
                              parse_mode="Markdown")
    await message.answer(f"Для записи заполняй анкету!", reply_markup=kb_anket)



if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_starup)

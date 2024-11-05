from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import initiate_db, get_all_products, add_user, is_included

api = '7926865795:AAE_IGSB-MGf44pUiCmbAwAqvCZ7zDeCH34'

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
inl = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ], resize_keyboard=True
)
but = KeyboardButton(text='Регистрация')
but1 = KeyboardButton(text='Рассчитать')
button = KeyboardButton(text='Информация')
button1 = KeyboardButton(text='Купить')

kb.row(but)
kb.insert(but1)
kb.add(button)
kb.insert(button1)

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    global title, description, price
    all_products = get_all_products()
    images = ['photo/D3.jpg', 'photo/fe.jpg', 'photo/kl.jpg', 'photo/zn.jpg']
    for index, product in zip(images, all_products):
        title = str(product[1])
        description = str(product[2])
        price = str(product[3])

        with open(index, 'rb') as img:
            await message.answer(f'Название: {title} |'
                                 f' Описание: {description} |'
                                 f' Цена: {price}')
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=inl)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()



@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=int(message.text))
    user_data = await state.get_data()
    username = user_data["username"]
    email = user_data["email"]
    age = int(message.text)
    add_user(username, email, age)
    await message.answer("Регистрация прошла успешно", reply_markup=kb)
    await state.finish()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()
@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес в килограммах:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=int(message.text))
    await message.answer('Укажите свой пол М или Ж')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    if data["gender"] == 'Ж':
        calories = (10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) - 161
    else:
        calories = (10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) + 5

    await message.answer(f"Ваша норма калорий в день составляет- {calories}")
    await message.answer('Спасибо, что воспользовались ботом')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

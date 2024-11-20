from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio, logging
from config import token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message:types.Message):
    await message.answer(f"Добро пожаловать в наш онлайн магазин {message.from_user.full_name}! \n Чтобы продолжить выберите категорию: /menu")

products = {
    'Автозапчасти': [
        {'name': 'Мотор BMW X5', 'price': 260000},
        {'name': 'Лобовое стекло', 'price': 48552},
        {'name': 'Шины', 'price': 65000}
    ],
    'Мобильные запчасти': [
        {'name': 'Аккумулятор', 'price': 2000},
        {'name': 'Стекло', 'price': 300},
        {'name': 'Зарядник', 'price': 1000}
    ]}




@dp.message(Command("menu"))
async def menu_command(message:types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Автозапчасти", callback_data='category:Автозапчасти')
    builder.button(text="Мобильные запчасти", callback_data='category:Мобильные запчасти')
    keyboard = builder.as_markup()

    await message.answer("Раздел наших продуктов: ", reply_markup=builder.as_markup())


@dp.callback_query(lambda c: c.data.startswith('category:'))
async def process_category(callback_query: types.CallbackQuery):
    category = callback_query.data.split(":")[1]
    
    builder = InlineKeyboardBuilder()
    for i, product in enumerate(products[category]):
        builder.button(text=f"{product['name']} - {product['price']} ₽", callback_data=f"product:{category}:{i}")
    
    keyboard = builder.as_markup()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f"Вы выбрали категорию {category}. Вот доступные товары:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('product:'))
async def process_product(callback_query: types.CallbackQuery):
    category, index = callback_query.data.split(":")[1:]
    index = int(index)
    product = products[category][index]
    
    builder = InlineKeyboardBuilder()
    builder.button(text="Да, хочу купить", callback_data=f"confirm:{category}:{index}")
    builder.button(text="Нет, вернуться к выбору товаров", callback_data=f"back:{category}")
    
    keyboard = builder.as_markup()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f"Вы выбрали {product['name']} - {product['price']} ₽. Подтвердите свой выбор:",
        reply_markup=keyboard
    )



@dp.callback_query(lambda c: c.data.startswith('confirm:'))
async def process_confirm(callback_query: types.CallbackQuery):
    _, category, index = callback_query.data.split(":")
    index = int(index)
    product = products[category][index]

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f"Ваш заказ:\n{product['name']} - {product['price']} ₽\n\nСпасибо за покупку!", )


@dp.callback_query(lambda c: c.data.startswith('back:'))
async def process_back(callback_query: types.CallbackQuery):
    category = callback_query.data.split(":")[1]
    await process_category(callback_query)



@dp.message(Command("info"))
async def info(message: types.Message):
    await message.answer("Информация о магазине!!!")

async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())



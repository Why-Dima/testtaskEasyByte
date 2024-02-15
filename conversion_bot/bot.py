import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from conf import TOKEN, money
from extensions import ConvertException, MoneyConverter


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    mess = '''Добро пожаловать в EasyByteBot!
Здесь вы сможете конвертировать валюту,
Общаться с ботом.
Для того, чтобы узнать команды пропишите /help'''
    await message.answer(mess)
    await log(message)

@dp.message(Command('help'))
async def help(message: types.Message):
    mess = '''Основные команды:
/start - запускает бота
/help - информация о командах бота
/conversion - конвертатор валют
'''
    await message.answer(mess)
    await log(message)

@dp.message(Command('conversion'))
async def convers(message: types.Message):
    text = '''
    \n Чтобы узнать курс введите в именительном падеже:
    \n - Имя валюты из которой нужно перевести
    \n - Имя валюты в которую нужно перевести
    \n - Количество переводимой валюты
    \n Доступные валюты:
    '''
    #итерируемся по словарю и выводим ключи, это наши доступные валюты
    for i in money.keys():
        text = '\n -'.join((text, i))
    await message.answer(text)
    await log(message)

@dp.message()
async def conversion(message: types.Message):
    if (message.text).lower() == 'привет':
        await message.answer('Привет!')
    elif (message.text).lower() == 'пока':
        await message.answer('До встречи!')
    elif (message.text).lower() == 'как погода?':
        await message.answer('Погода зависит от настроения')
    elif (message.text).lower() == 'как дела?':
        await message.answer('Все хорошо, как у вас?')
    else:
        await log(message)
        #Проверяем данные валют, которые ввел пользователь
        try:
            values = message.text.lower().split(' ')
            print(values)
            if len(values) != 3:
                raise ConvertException('Не верное количество параметров')
            quote, base, amount = values
            total_base = MoneyConverter.get_price(quote, base, amount)
        except ConvertException as e:
            await bot.send_message(message.chat.id, f'Ошибка пользователя\n{e}')
        except Exception as e:
            await bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')
        else:
            total_base = float(total_base) * float(amount)
            #считаем цену валюты перемножая курс и введенное нами значение
            text = f'Цена {amount} {quote} в {base} = {"%.2f" % total_base}'
            await bot.send_message(message.chat.id, text)
            await log(message)

async def log(message: types.Message):
    print(f'Пользователь {message.chat.username} ввел {message.text}')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hlink
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = '7670032583:AAHUxuf5tSiOowl-Xq-aNQgm0nQo2rxYYh0'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
data = None
reg_data = None

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_info = KeyboardButton(text='Info')
button_calories = KeyboardButton(text='Рассчитать...')
button_buy = KeyboardButton(text='Купить')
button_reg = KeyboardButton(text='Регистрация')
kb.add(button_calories)
kb.insert(button_info)
kb.add(button_buy)
kb.insert(button_reg)

kb_in = InlineKeyboardMarkup()
button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in.add(button_calories)
kb_in.add(button_formulas)

kb_vine = InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text='Киндзмараули', callback_data='product_buying')],
        [InlineKeyboardButton(text='¨Хванчкара', callback_data='product_buying')],
        [InlineKeyboardButton(text='Саперави', callback_data='product_buying')],
        [InlineKeyboardButton(text='Цинандали', callback_data='product_buying')]
])

# texts = []
# text = '''Красное полусладкое вино.
# Вино строго моносортовое: производится из сорта винограда саперави, возделываемого в районе села Киндзмараули в Кварельском районе Кахетии. Виноград для этого вина собирается при сахаристости не менее 22 %, благодаря чему оно всегда является природно-полусладким без добавления сахара.
# Кондиционное вино «Киндзмараули» имеет «цвет переспелой вишни или граната, нежный, полный, бархатистый вкус и типичный сортовой букет, аромат свежий с сортовыми тонами, оттенки — вишнёвая косточка, чёрная смородина». Вино «Киндзмараули» рекомендуется подавать к десертам, фруктам и острым соусам — оно сглаживает остроту пищи. Природно-полусладкие вина не предназначены для длительного хранения и должны потребляться молодыми.'''
# texts.append(text)
# text = '''Природно-полусладкое красное вино из винограда сортов Александроули и Муджуретули, выращенного в окрестностях села Хванчкара, которое расположено в Амбролаурском районе региона Рача—Лечхуми. Послужило прообразом остальных природно-полусладких вин Грузии. Рекомендуется подавать к десертам и фруктам.
# Цвет тёмно-рубиновый. Профессор Мехузла определяет его цвет как «сочный гранатовый с фиолетовыми тонами». Аромат: малина, горная фиалка, темно-красная бархатная роза. Букет сильно развитый, вкус гармоничный, с тонами малины, бархатистый, послевкусие долгое.'''
# texts.append(text)
# text = '''Саперави – главный автохтонный (местный) красный сорт Грузии. В зависимости от состава почв, микроклимата и экспозиции этот виноград может давать разные ароматические и вкусовые винные оттенки. Так, например, красное сухое вино из саперави, собранного с высокогорных виноградников, будет иметь больше пряных нюансов. Кроме того, на особенности букета влияют способ и длительность выдержки.'''
# texts.append(text)
# text = '''Сухое белое кахетинское вино. Изготавливается из винограда сортов ркацители и мцване (85 % к 15 % соответственно). Созревает и выявляет свои лучшие свойства после двух-трёхлетней выдержки.
# «Цинандали» — одно из самых старых грузинских вин, известных по имени: промышленно производится с 1886 года. Как следует из названия вина, поначалу оно вырабатывалось только в родовом имении князя Чавчавадзе. Цинандали собрало 10 золотых и 9 серебряных медалей на международных выставках.
# Может подаваться к закуске, к легким мясным и рыбным блюдам. Рекомендуется подавать охлажденным до 10−12°С.'''
# texts.append(text)
#
# price = [1745, 3015, 1380, 1050]
# vine_names = ['КИНДЗМАРАУЛИ', 'ХВАНЧКАРА', 'САПЕРАВИ', 'ЦИНАНДАЛИ']
# pics = ['kindzmarauli.jpg', 'kvanchkara.jpg', 'saperavi.jpg', 'tsinandali.jpg']
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState (StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    global reg_data
    if is_user(message.text):
        await message.answer('Пользователь существует, введите другое имя.')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        reg_data = await state.get_data()
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    global reg_data
    await state.update_data(email=message.text)
    reg_data = await state.get_data()
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    global reg_data
    if int(message.text) < 18:
        await message.answer('Вы еще слишком молоды для нашего магазина...')
        await state.finish()
    else:
        await state.update_data(age=message.text)
        reg_data = await state.get_data()
        await state.finish()
        res = add_user(reg_data['username'], reg_data['email'], reg_data['age'])
        if res:
            await message.answer('Поздравляю, регистрация прошла успешно!')
            await state.finish()
        else:
            await message.answer('Упс... Извините, что-то пошло не так...')
            await state.finish()


@dp.message_handler(commands=['start'])
async def beg_point(message):
    await message.answer('Привет! Я бот помогающий Вашему здоровью.', reply_markup = kb) # \nСкажите, сколько Вам лет?')

@dp.message_handler(text='Info')
async def about(message):
    await message.answer('Этот бот разработан в качестве учебного задания в' + hlink('UrbanUniversity.', 'https://urban-university.ru/'),parse_mode="HTML")

@dp.message_handler(text='Рассчитать...')
async def calculation(message):
    await message.answer('Расчет', reply_markup=kb_in)

@dp.callback_query_handler(text='calories')
async def how_old(call):
    await call.message.answer('Скажите, сколько Вам лет?')
    await call.answer()
    await UserState.age.set()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Норма суточного потребления калорий расчитывается по формуле Миффлина-Сан Жеора, разработанной группой американских врачей-диетологов под руководством докторов Миффлина и Сан Жеора.\nУпрощенный вариант формулы Миффлина-Сан Жеора выглядит следующим образом:\n\nдля мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161. ', reply_markup = kb)
    await call.answer()

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Поздравляю!\nВы сделали прекрасную покупку.\nОплата будет списана с Вашего счета.\nВаша покупка будет доставлена в ближайшее время.')
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    global data
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Каков Ваш рост?')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    global data
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('И последний вопрос - каков Ваш вес?')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    global data
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await state.finish()
    calories = comp_caloryes(data['age'], data['growth'], data['weight'])
    await message.answer(f'Ваша суточная норма калорий:\n{int(calories[0])}, если Вы мужчина, или\n{int(calories[1])}, если Вы женщина.', reply_markup = kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    vines = get_all_products()
    items = len(vines)
    print('items -',items)
    for i in vines:
        if i[0] != items:
            with open(i[4], 'rb') as img:
                await message.answer_photo(img,i[1] + '\n' + i[2] + f'\nЦена - {i[3]} руб.')
        else:
            with open(i[4], 'rb') as img:
                await message.answer_photo(img,i[1] + '\n' + i[2] + f'\nЦена - {i[3]} руб.', reply_markup=kb_vine)
def comp_caloryes(age, growth, weight):
    result = int(weight) * 10 + int(growth) * 6.25 - int(age) * 5
    return result+5, result-161

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    initiate_db()
    executor.start_polling(dp, skip_updates=True)

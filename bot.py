import discord
import random
import asyncio
import requests
import os  # Додав бібліотеку os для роботи з змінними середовища
from discord.ext import commands
from discord import ui
from datetime import datetime

# Отримуємо токен з середовища
TOKEN = os.environ.get('DISCORD_TOKEN')  # Використовуємо змінну середовища DISCORD_TOKEN

# Налаштування intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Список доступних валют з перекладом
CURRENCY_CODES = {
    "USD": "США",
    "EUR": "Євро",
    "UAH": "Українська гривня",
    "GBP": "Фунт стерлінгів",
    "JPY": "Японська єна",
    "CAD": "Канадський долар",
    "AUD": "Австралійський долар",
    "CHF": "Швейцарський франк"
}

# Функція для отримання курсу валют
def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['rates'].get(target_currency, None)
    return None

# Функція автозаповнення з локалізацією
async def currency_autocomplete(interaction: discord.Interaction, current: str):
    return [
        discord.app_commands.Choice(name=f"{code} ({name})", value=code)
        for code, name in CURRENCY_CODES.items()
        if code.startswith(current.upper())
    ]

# Список поганих слів
bad_words = ["дебил", "дибіл", "блять", "сука", "ебать", "пидор", "ахуеть", "нихуя", "хуй", "нахуй", "хуйня", "блядина", "пидрила", "еблан", "ебанат", "бл", "сук", "нах", "чорт", "чиртила", "чортила", "нахуя", "шлюха", "ебал", "дрочил", "порно", "даун", "уебище", "пидр",]  # Замініть на реальні погані слова


# Фільтрація за замовчуванням вимкнена
protection_enabled = False

# Команда /hello
user_greeted = {}

@bot.tree.command(name="hello", description="Познайомитися з ботом")
async def hello(interaction: discord.Interaction):
    username_mention = interaction.user.mention
    if user_greeted.get(interaction.user.id):
        message = (
            f"> :clap: Оу, вітаю знову {username_mention}! Здається, ми вже знайомилися! Сподіваюся, ви отримуєте корисну інформацію"
            f"кожен день! :)"
        )
    else:
        message = (
            f"> :smiling_face_with_3_hearts: Вітаю {username_mention}, я Smilot AI, моя головна задача - допомагати людям! "
            f"Я буду дуже старатися допомагати тим, що вкладе мій розробник!❤️"
        )
        user_greeted[interaction.user.id] = True

    await interaction.response.send_message(message)

# Команда /counting
@bot.tree.command(name="counting", description="Підрахувати кількість хвилин з днів у Minecraft")
async def counting(interaction: discord.Interaction, days: int):
    total_minutes = days * 20
    await interaction.response.send_message(f"> Кількість хвилин у реальному житті для {days} днів у Minecraft: {total_minutes} хвилин.")

# Команда /exchange
@bot.tree.command(name="exchange", description="Обміняти валюту")
async def exchange(interaction: discord.Interaction, amount: float, from_currency: str, to_currency: str):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    rate = get_exchange_rate(from_currency, to_currency)
    if rate is None:
        await interaction.response.send_message(f"> Не вдалося знайти курс для {from_currency} -> {to_currency}.")
        return
    exchanged_amount = amount * rate
    await interaction.response.send_message(f"> {amount} {from_currency} = {exchanged_amount:.2f} {to_currency} (курс: {rate})")

@exchange.autocomplete("from_currency")
async def from_currency_autocomplete(interaction: discord.Interaction, current: str):
    return await currency_autocomplete(interaction, current)

@exchange.autocomplete("to_currency")
async def to_currency_autocomplete(interaction: discord.Interaction, current: str):
    return await currency_autocomplete(interaction, current)

# Команда /format
@bot.tree.command(name="format", description="Детальний опис форматування тексту у Discord")
async def format(interaction: discord.Interaction):
    username_mention = interaction.user.mention
    description = (
        f"✏️ Вітаю {username_mention}! Ось детальний опис форматування тексту у Discord :\n\n"
        "**1. Жирний текст (Bold):**\n"
        "Використовуй подвійні зірочки ** навколо тексту.\n"
        "Приклад: **Жирний текст**\n"
        "Результат: **Жирний текст**\n\n"
        "**2. Курсив (Italic):**\n"
        "Використовуй одну зірочку * або один знак підкреслення _ навколо тексту.\n"
        "Приклад: *Курсив* або _Курсив_\n"
        "Результат: *Курсив*\n\n"
        "**3. Жирний курсив (Bold Italic):**\n"
        "Комбінуй три зірочки *** навколо тексту.\n"
        "Приклад: ***Жирний курсив***\n"
        "Результат: ***Жирний курсив***\n\n"
        "**4. Закреслений текст (Strikethrough):**\n"
        "Використовуй подвійний тилда ~~ навколо тексту.\n"
        "Приклад: ~~Закреслений текст~~\n"
        "Результат: ~~Закреслений текст~~\n\n"
        "**5. Моноширинний текст (Monospace):**\n"
        "Використовуй одинарні зворотні апострофи    (гравіс).\n"
        "Приклад:  Моноширинний текст \n"
        "Результат: Моноширинний текст\n\n"
        "**6. Блок коду (Code Block):**\n"
        "Використовуй три зворотні апострофи"
        "**7. Цитування (Blockquote):**\n"
        "Використовуй знак більше > на початку тексту.\n"
        "Приклад: > Цитата\n"
        "Результат:\n> Цитата\n"
    )
    await interaction.response.send_message(description)

# Команда /protection
@bot.tree.command(name="protection", description="Увімкнути або вимкнути фільтрацію поганих слів")
async def protection(interaction: discord.Interaction):
    global protection_enabled
    # Перевірка прав адміністратора
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("> ❌ Ви повинні бути адміністратором, щоб використовувати цю команду.")
        return
    
    # Зміна стану фільтрації
    protection_enabled = not protection_enabled
    status = "увімкнено" if protection_enabled else "вимкнено"
    await interaction.response.send_message(f"> {'✅' if protection_enabled else '❌'} Фільтрація поганих слів {status}.")

# Подія для фільтрації повідомлень
@bot.event
async def on_message(message: discord.Message):
    global protection_enabled
    # Перевірка, щоб не реагувати на повідомлення від бота
    if message.author == bot.user:
        return
    
    # Якщо фільтрація увімкнена, перевіряємо на наявність поганих слів
    if protection_enabled and message.guild:
        if any(bad_word in message.content.lower() for bad_word in bad_words):
            await message.delete()  # Видаляємо повідомлення
            await message.channel.send(f"> {message.author.mention}, ваше повідомлення було видалено через наявність ненормативної лексики.")
        else:
            await bot.process_commands(message)

# Запуск бота
bot.run(TOKEN)

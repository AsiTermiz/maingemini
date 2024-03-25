import telebot
from telebot import types
import google.generativeai as genai
import threading

TELEGRAM_API_TOKEN = '7180517266:AAH296y2JgLodOE9k9KO9hODjP8XMCgvTUo'
GEMINI_API_KEY = "AIzaSyAzxRf2ZPJDMgNtXKVhRT5zFyOGxgKrSX8"
genai.configure(api_key=GEMINI_API_KEY)

# Generation configuration and safety settings
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Telegram bot initialization
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
model = genai.GenerativeModel(
    model_name='gemini-1.0-pro-latest',
    generation_config=generation_config,
    safety_settings=safety_settings
)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Hisobim💠", callback_data="myaccuz"),
               types.InlineKeyboardButton("Sozlamalar⚙️", callback_data="settingsuz"))
    markup.row(types.InlineKeyboardButton("Web Sayt🪐", url="https://asicloud.uz"),
               types.InlineKeyboardButton("Telegram Stories🌄", url="https://t.me/storiescreation"))
    bot.reply_to(message, "Salom☺️ Gemini Google AI ga hush kelibsiz👋, Asicloud tomonidan qo'llab quvvatlanadi:✅", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "myaccuz":
        user_id = call.from_user.id
        user_name = call.from_user.first_name
        # Edit the message text
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"ID: {user_id}\nIsmingiz: {user_name}")
        # Edit the inline keyboard
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(types.InlineKeyboardButton("Orqaga🔙", callback_data="homeuz"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=reply_markup)
    elif call.data == "settingsuz":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Sozlamalar!")
        # Edit the inline keyboard
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(types.InlineKeyboardButton("Til🇺🇿", callback_data="languages"))
        reply_markup.add(types.InlineKeyboardButton("Yordam🆘", callback_data="helpuz"))
        reply_markup.add(types.InlineKeyboardButton("Orqaga🔙", callback_data="homeuz"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=reply_markup)

    elif call.data == "homeuz":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Salom☺️ Gemini Google AI ga hush kelibsiz👋, Asicloud tomonidan qo'llab quvvatlanadi!✅")
        # Edit the inline keyboard
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("Hisobim💠", callback_data="myaccuz"),
               types.InlineKeyboardButton("Sozlamalar⚙️", callback_data="settingsuz"))
        markup.row(types.InlineKeyboardButton("Web Sayt🪐", url="https://asicloud.uz"),
               types.InlineKeyboardButton("Telegram Stories🌄", url="https://t.me/storiescreation"))

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=markup)


    elif call.data == "languages":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Tilni tanlang / Choose Language!")
        # Edit the inline keyboard
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("O'zbek tili🇺🇿", callback_data="homeuz"),
               types.InlineKeyboardButton("English🇺🇸", callback_data="homelangen"))
        markup.row(types.InlineKeyboardButton("Russian🇷🇺", callback_data="homelangru"),
               types.InlineKeyboardButton("Korean🇰🇷", callback_data="homelangko"))
        markup.row(types.InlineKeyboardButton("Arabic🇦🇪", callback_data="homelangar"),
               types.InlineKeyboardButton("Turkish🇹🇷", callback_data="homelangtr"))

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=markup)

    elif call.data == "helpuz":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Yordam bo'limi tez orada qo'shiladi!")
        # Edit the inline keyboard
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(types.InlineKeyboardButton("Orqaga🔙", callback_data="homeuz"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=reply_markup)


@bot.message_handler(commands=['gemini'])
def gemini_command(message):
    # Check if there's additional text after the command
    query = message.text.split(' ', 1)
    if len(query) == 1:
        bot.reply_to(message, "/gemini buyrug'ini guruhda quyidagicha ishlating, Masalan: /gemini what is Asicloud?")
    else:
        # Send a "Generating..." message
        generating_message = bot.reply_to(message, "......")
        # Start a thread to generate the response asynchronously
        threading.Thread(target=generate_response, args=(message.chat.id, generating_message.message_id, query[1])).start()


def generate_response(chat_id, message_id, query):
    # Generate response to the user's query
    chat = model.start_chat(history=[])
    response = chat.send_message(query)
    if response.text:
        # Edit the original message with the generated response
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=response.text)
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Kechirasiz javob topa olmadim!.")


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    # Check if the message was sent in a group
    if message.chat.type in ['group', 'supergroup']:
        return  # Ignore the message in group chats
    else:
        # Send a "Generating..." message
        generating_message = bot.reply_to(message, ".......")
        # Start a thread to generate the response asynchronously
        threading.Thread(target=generate_response, args=(message.chat.id, generating_message.message_id, message.text)).start()


# Start polling
bot.infinity_polling(timeout=10, long_polling_timeout=5)

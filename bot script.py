import telebot
import config

from neuro import result
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
ind = {}


@bot.message_handler(commands=['start'])
def welcome(message):
	chat_id = message.chat.id
	global ind
	ind[chat_id]=0
	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>".format(message.from_user, bot.get_me()),
		parse_mode='html')
	bot.send_message(message.chat.id, "Если бот работает неправильно повторно напиши /start")
	bot.send_message(message.chat.id, "Отправь мне фотографию которую хочешь стилизовать")

@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == 'test':
			bot.send_message(message.chat.id, ind)

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
	try:
		chat_id = message.chat.id
		global ind

		file_info = bot.get_file(message.photo[0].file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		if ind[chat_id] == 0:
			file_name = "content"
			bot.reply_to(message, "Принято!")
			bot.send_message(message.chat.id, "Теперь отправь фотографию с которой взять стиль")
			ind[chat_id]+=1
		else:
			file_name = "style"
			bot.reply_to(message, "Принято!")
			bot.send_message(message.chat.id, "Ваши фотографии обрабатываются. Пожалуйста подождите")
			ind[chat_id] = 2
		src = "content/" + file_name + str(chat_id) + ".jpg"
		with open(src, 'wb') as new_file:
			new_file.write(downloaded_file)
		if ind[chat_id] == 2:
			ind[chat_id]=0
			transform(chat_id)


		
	except Exception as e:
		bot.reply_to(message, "Введите /start")

def transform(chat_id):
	result(chat_id)
	with open('content/output' + str(chat_id) + '.jpg', 'rb') as f1:
		bot.send_message(chat_id, "Ваш результат")
		bot.send_photo(chat_id, f1)
		bot.send_message(chat_id, "Если хочешь сделать еще, пришли фотографию которую хочешь стилизовать")


# RUN
bot.polling(none_stop=True)


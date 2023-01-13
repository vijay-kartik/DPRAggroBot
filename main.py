import os
import telebot

API_KEY = os.environ['API_KEY']

bot = telebot.TeleBot(API_KEY)
h1 = 'Monitored Wells:'
h2 = 'TPR:'
h3 = 'Remarks:'
h4 = 'Wellhead Pressure:'
end = 'Regards'
h1_text = ''
h2_text = ''
h3_text = ''
h4_text = ''


@bot.message_handler(commands=["greet"])
def greet(message):
  bot.reply_to(message, "Hi! Kartik" + message.text)


@bot.message_handler(commands=['reset'])
def reset_extracts(msg):
  global h1_text, h2_text, h3_text, h4_text
  h1_text = ''
  h2_text = ''
  h3_text = ''
  h4_text = ''


@bot.message_handler(regexp=h1)
def extract_append_text(message):
  global h1_text
  h1_text += (message.text.split(h1)[1].split(h2)[0] + '\n')

  global h2_text
  h2_text += (
    message.text.split(h2)[1].split(h3)[0].rstrip('\n*').lstrip('*\n') + '\n')

  global h3_text
  h3_text += (message.text.split(h3)[1].split(h4)[0].rstrip('\n*').lstrip('*\n') + '\n')
  
  global h4_text
  h4_text += (message.text.split(h4)[1].split(end)[0].rstrip('\n*').lstrip('*\n') + '\n')

  bot.send_message(message.chat.id, "done" + h1_text)


@bot.message_handler(commands=['eval'])
def evaluate(msg):
  global h1_text, h2_text, h3_text, h4_text
  bot.reply_to(
    msg, 
    str('*') + h1 + str('*') + '\n' + h1_text.rstrip('\n*').lstrip('*\n') + '\n' + '\n' +
    str('*') + h2 + str('*') + h2_text.rstrip('\n*').lstrip('*\n') + '\n' +
    str('*') + h3 + str('*') + '\n' + h3_text.rstrip('\n*').lstrip('*\n') + '\n' + '\n' +
    str('*') + h4 + str('*') + '\n' + h4_text.rstrip('\n*').lstrip('*\n')
  )
  reset_extracts(msg)


bot.polling()

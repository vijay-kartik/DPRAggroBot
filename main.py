import os
import telebot
from datetime import datetime

API_KEY = os.environ['API_KEY']

headings = ['Monitored Wells:', 'TPR:', 'Remarks:', 'Wellhead Pressure:']
ends = ['TPR:', 'Remarks:', 'Wellhead Pressure:', 'Regards']
areas = ['Area-1', 'Area-3', 'Area-4']
bot = telebot.TeleBot(API_KEY)

greet_msg = "Welcome to DPRAggroBot! I am here to help you with aggregating your DPRs from Area-1, Area-3 and Area-4.\n\nYou can interact with me by using the following commands:\n/start - Trigger the DPR input one by one\n/eval - Get the final report \n/reset - Reset DPR data \n/help - Display this message again \n\nSome of the commands may not run for now as the new version is still in dev phase. I request you to kindly use old strategy to get your work done for now."

h1 = 'Monitored Wells:'
h2 = 'TPR:'
h3 = 'Remarks:'
h4 = 'Wellhead Pressure:'
end = 'Regards'

# global variables
h1_text = ''
h2_text = ''
h3_text = ''
h4_text = ''
msg_input_count = 0

# helper functions
def make_bold(str):
  return '*' + str + '*'

def clean(str):
  return str.rstrip('\n*\n').lstrip('\n*\n')

def extractRemarks(remarkString):
  print(remarkString)

# bot APIs
@bot.message_handler(commands=['start'])
def start(message):
  if msg_input_count >= 3:
    bot.send_message(message.chat.id, "All messages have been entered. You are ready to evaluate now.")
  else:
    bot.send_message(message.chat.id, text="Please enter DPR {} message:".format(areas[msg_input_count]))
    bot.register_next_step_handler(message, collect_message)

@bot.message_handler(commands=["greet", "help"])
def greet(message):
  bot.send_message(message.chat.id, greet_msg)

@bot.message_handler(commands=['reset'])
def reset_extracts(msg):
  global h1_text, h2_text, h3_text, h4_text, msg_input_count
  h1_text = ''
  h2_text = ''
  h3_text = ''
  h4_text = ''
  msg_input_count = 0

def collect_message(message):
  global msg_input_count 
  extract_append_text(message)
  msg_input_count += 1
  start(message)
    
@bot.message_handler(regexp="Sir")
def extract_append_text(message):
  global h1_text
  h1_text += (message.text.split(h1)[1].split(h2)[0].rstrip('\n*').lstrip('*\n') + '\n')

  global h2_text
  h2_text += (
    message.text.split(h2)[1].split(h3)[0].rstrip('\n*').lstrip('*\n') + '\n')

  global h3_text
  h3_text += (message.text.split(h3)[1].split(h4)[0].rstrip('\n*').lstrip('*\n') + '\n')
  
  global h4_text
  h4_text += (message.text.split(h4)[1].split(end)[0].rstrip('\n*').lstrip('*\n') + '\n')

  bot.send_message(message.chat.id, "done")


@bot.message_handler(commands=['eval'])
def evaluate(msg):
  global h1_text, h2_text, h3_text, h4_text
  intro_msg = "Sir,\n*A/Lift DPR: " + datetime.today().strftime('%d/%m/%Y')
  salutation = "\nRegards\n*Gairik Das*"
  full_text = intro_msg + "*\n" + make_bold(h1) + '\n' + clean(h1_text) + '\n' + make_bold(h2) + ' ' + clean(h2_text) + '\n' + make_bold(h3) + '\n' + clean(h3_text) + '\n' + '\n' + make_bold(h4) + '\n' + clean(h4_text) + '\n' + salutation
  
  for i in range(0, len(full_text), 3000):
    bot.send_message(
  msg.chat.id, full_text[i:i+3000])  
  
  reset_extracts(msg)
          
bot.polling()

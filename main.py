import os
import re
import telebot
from datetime import datetime

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

# Set the list of commands for the bot
commands = [
    {"command": "/start", "description": "Trigger the DPR input one by one"},
    {"command": "/eval", "description": "Get the final report"},
    {"command": "/reset", "description": "Reset DPR data"},
    {"command": "/help", "description": "Display this message again"}
]
bot.set_my_commands(commands)



headings = ['Monitored Wells:', 'TPR:', 'Remarks:', 'Wellhead Pressure:']
locations = []
ends = ['TPR:', 'Remarks:', 'Wellhead Pressure:', 'Regards']
areas = ['Area-1', 'Area-3', 'Area-4']

greet_msg = "Welcome to DPRAggroBot! I am here to help you with aggregating your DPRs from Area-1, Area-3 and Area-4.\n\nYou can interact with me by using the following commands:\n/start - Trigger the DPR input one by one\n/eval - Get the final report \n/reset - Reset DPR data \n/help - Display this message again"

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
  return str.strip('\n*\n*')

def extractRemarks(remarkString):
  print(remarkString)

def isInValidFormat(inputStr):
  global locations
  match1 = re.search(r"\*(monitored well(s)?:\*", inputStr, re.IGNORECASE)
  match2 = re.search(r"\*(well head|wellhead) pressure(s)?:\*", inputStr, re.IGNORECASE)
  match3 = re.search(r"\*TPR(s)?:\*", inputStr, re.IGNORECASE)
  match4 = re.search(r"\*remark(s)?:\*")

  if match1 and match2 and match3 and match4:
    locations.append([match1.start(), match1.end()])
    locations.append([match2.start(), match2.end()])
    locations.append([match3.start(), match3.end()])
    locations.append([match4.start(), match4.end()])
    return True
  else:
    return False

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
  locations = []

def collect_message(message):
  global msg_input_count
  if isInValidFormat(message.text):
    extract_append_text(message)
    msg_input_count += 1
  else:
    bot.send_message(message.chat.id, "Your message has some formatting issues. Kindly correct the format and try again.")  
  start(message)
    
@bot.message_handler(regexp="Sir")
def extract_append_text(message):
  global h1_text, h2_text, h3_text, h4_text
  h1_text += (
    clean(message.text.split(h1)[1].split(h2)[0]) + '\n')

  h2_text += (
    clean(message.text.split(h2)[1].split(h3)[0]) + '\n')

  h3_text += (
    clean(message.text.split(h3)[1].split(h4)[0]) + '\n')
  
  h4_text += (
    clean(message.text.split(h4)[1].split(end)[0]) + '\n')
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

from flask import Flask, request
import requests
import telebot

app = Flask(__name__)

yourKey = "insert your key here"

bot = telebot.TeleBot(yourKey)


def get_what_to_do():
    params = {"query": "/api/activity/"}
    api_result = requests.get('http://www.boredapi.com/api/activity/', params)
    api_response = api_result.json()
    return f'{api_response["activity"]}' + '. It will be a ' + f'{api_response["type"]}' + ' activity.'


def get_kanye_quote():
    api_result = requests.get('https://api.kanye.rest/')
    api_response = api_result.json()
    return "\n\nHere's your Kanye West quote: " + f'{api_response["quote"]}'


def get_age_by_name(name):
    api_result = requests.get(f'https://api.agify.io/?name={name}')
    print(api_result)
    api_response = api_result.json()
    return f'I guess your age is {api_response["age"]}'


@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok"


@bot.message_handler(commands=['start'])
def send_todo_and_kanye(message):
    bot.reply_to(message, 'Hi!\n\n' + get_what_to_do() + get_kanye_quote())


@bot.message_handler(func=lambda m: True)
def send_predicted_age(message):
    bot.reply_to(message, get_age_by_name(message.text))

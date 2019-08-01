import telebot
import sum_parser
import flask
import os


token = os.environ["TOKEN"]
bot = telebot.TeleBot(token)
# Telegram has a maximum message length of 4096 characters
max_len = 4096
server = flask.Flask(__name__)

@bot.message_handler(content_types=['text'])
def answer(message):
    ans = sum_parser.parsing(message.text)
    try:
        if len(ans) > max_len:
            for i in range(0, len(ans), max_len):
                bot.send_message(message.chat.id, ans[i:i + max_len], parse_mode='html')
        else:
            bot.send_message(message.chat.id, ans, parse_mode='html')
    except Exception as e:
        print(e)

@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://afternoon-beyond-27757.herokuapp.com/' + token)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=False)

import os
from flask import Flask, request
from telebot import TeleBot, types, util

token = "7356363033:AAGOFfbEa23y9BaPUZzBpcgconHJN4tOQZE"
bot = TeleBot(token, threaded=False, parse_mode='html', disable_web_page_preview=True)
app = Flask(__name__)

@bot.message_handler(content_types=["text"], chat_types=['private'])
def rest(message: types.Message):
    try:
        command = util.extract_command(message.text)
        if command:
            command = command.lower()
            if command == "start":
                bot.send_message(message.chat.id, 'Hey! How are you?')
    except:
        pass

@app.route('/' + token, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    url = os.getenv('VERCEL_PROJECT_PRODUCTION_URL')
    bot.set_webhook(url= f"{url}/{token}", max_connections=50)
    return "!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
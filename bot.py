import os
import flask
import telebot
import requests

TELEGRAM_BOT_TOKEN = "9104150951:AAE4JjeM6FQvFyvRfyUnxCWAyNmtp9CDV7s".strip()
# يمكنك وضع مفتاح DeepSeek API الخاص بك هنا أو كمتغير بيئة
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "ضع_مفتاح_ديپسيك_هنا").strip()

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = flask.Flask(__name__)

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=['POST'])
def webhook():
    json_string = flask.request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "Bot is running successfully with DeepSeek!", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك يا إسماعيل! أنا مساعدك الذكي السريع المدعوم بـ DeepSeek. 🤖\n"
        "اطرح أي سؤال وسأقوم بالإجابة عليه فوراً."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_ai_response(message):
    user_query = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # الاتصال المباشر عبر API الخاص بـ DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": user_query}],
            "stream": False
        }
        
        response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=data, timeout=30)
        res_json = response.json()
        
        if "choices" in res_json and len(res_json["choices"]) > 0:
            reply_text = res_json["choices"][0]["message"]["content"]
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, f"عذراً، لم يتمكن الخادم من الرد: {res_json}")
            
    except Exception as e:
        print(f"API Error: {e}")
        bot.reply_to(message, f"عذراً، حدث خطأ في الاتصال: {str(e)}")

if __name__ == "__main__":
    RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{RENDER_URL}/{TELEGRAM_BOT_TOKEN}")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

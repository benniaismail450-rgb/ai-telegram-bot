import os
import time
import flask
import telebot
from google import genai

TELEGRAM_BOT_TOKEN = "9104150951:AAE4JjeM6FQvFyvRfyUnxCWAyNmtp9CDV7s".strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Lloi3u_sd1XlpoSqBiFmL9jMr-5wKf3fUYdlOrNB3ZeQ").strip()

client = genai.Client(api_key=GEMINI_API_KEY)
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
    return "Bot is running successfully!", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك يا إسماعيل! أنا مساعدك الذكي السريع المدعوم بالذكاء الاصطناعي. 🤖\n"
        "طرح أي سؤال وسأقوم بالإجابة عليه فوراً."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_ai_response(message):
    user_query = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # توليد الإجابة مباشرة
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_query,
        )
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "عذراً، لم أتمكن من توليد إجابة.")
    except Exception as e:
        error_msg = str(e)
        print(f"Gemini Error: {error_msg}")
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            bot.reply_to(message, "لقد وصلت إلى الحد المسموح من الطلبات المجانية مؤقتاً، يجدر بك إنشاء مفتاح API جديد من Google AI Studio.")
        else:
            bot.reply_to(message, f"عذراً، حدث ضغط مؤقت: {error_msg}")

if __name__ == "__main__":
    RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{RENDER_URL}/{TELEGRAM_BOT_TOKEN}")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

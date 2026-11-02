import os
import telebot
from google import genai

# التوكن الصحيح للبوت
TELEGRAM_BOT_TOKEN = "9104150951:AAE4JjeM6FQvFyvRfyUnxCWAyNmtp9CDV7s".strip()

# مفتاح جيميناي مع تنظيف دقيق جداً لأي مسافات أو رموز مخفية لإنهاء خطأ Illegal header value
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Lloi3u_sd1XlpoSqBiFmL9jMr-5wKf3fUYdlOrNB3ZeQ").strip()

client = genai.Client(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك يا إسماعيل! أنا مساعدك الذكي المدعوم بالذكاء الاصطناعي. 🤖\n"
        "يمكنك طرح أي سؤال يخطر بالك وسأقوم بالإجابة عليه فوراً."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_ai_response(message):
    user_query = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_query,
        )
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "عذراً، لم أتمكن من توليد إجابة.")
    except Exception as e:
        print(f"Gemini Error details: {e}")
        bot.reply_to(message, "عاضي، الخدمة تشهد ضغطاً مؤقتاً، جرب إرسال سؤالك مرة أخرى بعد ثوانٍ قليلة.")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Starting bot polling...")
    bot.polling(non_stop=True, interval=2, timeout=20)

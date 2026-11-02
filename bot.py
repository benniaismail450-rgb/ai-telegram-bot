import os
import telebot
from google import genai

TELEGRAM_BOT_TOKEN = "9020627346:AAGu_GBPEbsOqQ2bj01Toh7zw9NiXxOXzyQ"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Lloi3u_sd1XlpoSqBiFmL9jMr-5wKf3fUYdlOrNB3ZeQ")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك! أنا مساعدك الذكي المدعوم بالذكاء الاصطناعي. 🤖\n"
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
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "عذراً، لم أتمكن من توليد إجابة.")
    except Exception as e:
        print(f"Gemini Error details: {e}")
        bot.reply_to(message, f"عذراً، حدث خطأ في الرد: {str(e)}")

if __name__ == "__main__":
    # مسح أي ويب هوك قديم وإيقاف أي جلسة معلقة تماماً
    bot.remove_webhook()
    print("Starting bot polling...")
    # استخدام polling عادي مع السماح بتخطي التحديثات القديمة لمنع التداخل
    bot.polling(non_stop=True, interval=1, timeout=20)

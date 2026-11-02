import os
import telebot
from google import genai

# جلب المفاتيح من بيئة الاستضافة على Render بأمان
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# تهيئة عميل جوجل الذكي بالطريقة الحديثة
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
    
    # إرسال حالة "جاري الكتابة..."
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # توليد الإجابة باستخدام النموذج الحديث
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_query,
        )
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "عذراً، لم أتمكن من توليد إجابة.")
            
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقاً.")

if __name__ == "__main__":
    print("البوت يعمل الآن بالطريقة الحديثة بنجاح...")
    bot.infinity_polling()

import os
import telebot
import google.generativeai as genai

# التوكن الخاص ببوتك على تيليجرام
TELEGRAM_BOT_TOKEN = "9020627346:AAGu_GBPEbsOqQ2bj01Toh7zw9NiXxOXzyQ"

# مفتاح الـ API المؤقت للرفع العام (أو يمكنك وضعه لاحقاً عبر متغيرات البيئة)
GEMINI_API_KEY = "AIza_Placeholder_Key"

# إعداد الذكاء الاصطناعي
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 1000,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# رسالة الترحيب عند بدء البوت
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك! أنا مساعدك الذكي المدعوم بالذكاء الاصطناعي. 🤖\n"
        "يمكنك طرح أي سؤال يخطر بالك وسأقوم بالإجابة عليه فوراً."
    )
    bot.reply_to(message, welcome_text)

# الرد على رسائل المستخدمين والاستفسارات
@bot.message_handler(func=lambda message: True)
def handle_ai_response(message):
    user_query = message.text
    
    # إرسال حالة "جاري الكتابة..." ليكون البوت تفاعلياً
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # توليد الإجابة باستخدام الذكاء الاصطناعي
        response = model.generate_content(user_query)
        ai_reply = response.text
        bot.reply_to(message, ai_reply)
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقاً.")

if __name__ == "__main__":
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()

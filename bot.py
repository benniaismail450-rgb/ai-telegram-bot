import os
import telebot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# جلب المفاتيح من بيئة الاستضافة على Render بأمان تام
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# إعداد الذكاء الاصطناعي
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 1000,
}

# إضافة فلاتر الأمان لحماية البوت من المحتوى المخالف أو الخطير
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config=generation_config,
    safety_settings=safety_settings
)

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
        # توليد الإجابة باستخدام الذكاء الاصطناعي مع الأمان المدمج
        response = model.generate_content(user_query)
        
        # التأكد من وجود رد صالح
        if response.text:
            ai_reply = response.text
        else:
            ai_reply = "عذراً، تم حظر هذا المحتوى بواسطة إعدادات الأمان."
            
        bot.reply_to(message, ai_reply)
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقاً.")

if __name__ == "__main__":
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()

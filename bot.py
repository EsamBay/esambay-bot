import telebot
import json
import os
import subprocess
from datetime import datetime

# =============================================
#   إعدادات البوت
# =============================================

BOT_TOKEN = "8595374501:AAHssdSP0y8UFbI23CrEPbyPhoxC-r1HncY"
ADMIN_ID  = 1199941388
DB_FILE   = "database.json"

# =============================================
#   الرسائل
# =============================================

MSG_WELCOME = """
👋 أهلاً وسهلاً {name}!

🏪 مرحباً بك في *متجر تفعيلك*
كل اشتراكاتك الرقمية في مكان واحد 🚀

━━━━━━━━━━━━━━━
✅ تفعيل فوري وضمان كامل
💳 أسعار تنافسية
🚀 دعم سريع عبر واتساب
━━━━━━━━━━━━━━━

اكتب /help لعرض الأوامر المتاحة.
"""

MSG_HELP = """
📋 *الأوامر المتاحة:*

/start      — بدء البوت والتسجيل
/subscribe  — الاشتراك في قائمة العروض
/help       — عرض هذه القائمة

━━━━━━━━━━━━━━━
👤 *للأدمن فقط:*
/stats      — إحصائيات المشتركين
/broadcast  — إرسال رسالة جماعية
━━━━━━━━━━━━━━━
"""

MSG_SUBSCRIBED    = "✅ تم اشتراكك بنجاح! ستصلك أحدث العروض."
MSG_UNSUBSCRIBED  = "🔕 تم إلغاء اشتراكك. يمكنك إعادته بـ /subscribe"
MSG_ADMIN_ONLY    = "⛔ هذا الأمر للأدمن فقط."
MSG_BROADCAST_ASK = "📢 أرسل الرسالة التي تريد إذاعتها لجميع المشتركين:"
MSG_BROADCAST_DONE = "✅ تم إرسال الرسالة لـ {count} مشترك."
MSG_NO_SUBS       = "ℹ️ لا يوجد مشتركون حتى الآن."

# =============================================
#   قاعدة البيانات
# =============================================

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    auto_commit()

def auto_commit():
    try:
        subprocess.run(["git", "config", "user.email", "bot@esambay.com"], check=True)
        subprocess.run(["git", "config", "user.name",  "EsamBay Bot"],     check=True)
        subprocess.run(["git", "add", DB_FILE],                            check=True)
        result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if result.returncode != 0:
            subprocess.run(["git", "commit", "-m",
                f"bot: update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("✅ Database saved to GitHub")
    except Exception as e:
        print(f"⚠️ Git error: {e}")

def add_user(user):
    db  = load_db()
    uid = str(user.id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id":         user.id,
            "name":       f"{user.first_name or ''} {user.last_name or ''}".strip(),
            "username":   user.username or "",
            "subscribed": True,
            "joined_at":  datetime.now().isoformat(),
        }
        save_db(db)
        return True
    return False

def set_subscription(user_id, status):
    db  = load_db()
    uid = str(user_id)
    if uid in db["users"]:
        db["users"][uid]["subscribed"] = status
        save_db(db)

def get_subscribers():
    db = load_db()
    return [u for u in db["users"].values() if u.get("subscribed")]

def get_stats():
    db    = load_db()
    total = len(db["users"])
    subs  = sum(1 for u in db["users"].values() if u.get("subscribed"))
    return {"total": total, "subscribed": subs, "unsubscribed": total - subs}

# =============================================
#   البوت
# =============================================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
waiting_broadcast = set()

@bot.message_handler(commands=["start"])
def cmd_start(message):
    user   = message.from_user
    is_new = add_user(user)
    name   = user.first_name or "صديقي"
    bot.send_message(message.chat.id, MSG_WELCOME.format(name=name))
    if is_new:
        bot.send_message(
            ADMIN_ID,
            f"🔔 *مستخدم جديد!*\n"
            f"👤 {user.first_name} {user.last_name or ''}\n"
            f"🆔 `{user.id}`\n"
            f"📛 @{user.username or 'بدون'}\n"
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(message.chat.id, MSG_HELP)

@bot.message_handler(commands=["subscribe"])
def cmd_subscribe(message):
    db  = load_db()
    uid = str(message.from_user.id)
    if uid not in db["users"]:
        add_user(message.from_user)
        bot.send_message(message.chat.id, MSG_SUBSCRIBED)
        return
    if db["users"][uid].get("subscribed"):
        set_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, MSG_UNSUBSCRIBED)
    else:
        set_subscription(message.from_user.id, True)
        bot.send_message(message.chat.id, MSG_SUBSCRIBED)

@bot.message_handler(commands=["stats"])
def cmd_stats(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, MSG_ADMIN_ONLY)
        return
    s = get_stats()
    bot.send_message(message.chat.id,
        f"📊 *إحصائيات المتجر*\n\n"
        f"👥 إجمالي المستخدمين: `{s['total']}`\n"
        f"✅ المشتركون: `{s['subscribed']}`\n"
        f"🔕 غير المشتركين: `{s['unsubscribed']}`"
    )

@bot.message_handler(commands=["broadcast"])
def cmd_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, MSG_ADMIN_ONLY)
        return
    if not get_subscribers():
        bot.send_message(message.chat.id, MSG_NO_SUBS)
        return
    waiting_broadcast.add(message.from_user.id)
    bot.send_message(message.chat.id, MSG_BROADCAST_ASK)

@bot.message_handler(func=lambda m: m.from_user.id in waiting_broadcast)
def handle_broadcast(message):
    waiting_broadcast.discard(message.from_user.id)
    count = 0
    for user in get_subscribers():
        try:
            bot.send_message(user["id"],
                f"📢 *رسالة من متجر تفعيلك:*\n\n{message.text}")
            count += 1
        except Exception as e:
            print(f"Failed {user['id']}: {e}")
    bot.send_message(message.chat.id, MSG_BROADCAST_DONE.format(count=count))

@bot.message_handler(func=lambda m: True)
def handle_other(message):
    bot.send_message(message.chat.id,
        "❓ لم أفهم طلبك. اكتب /help لعرض الأوامر.")

# =============================================
#   تشغيل
# =============================================

if __name__ == "__main__":
    print("🤖 EsamBay Bot is running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)

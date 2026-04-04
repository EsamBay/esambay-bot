import telebot
import json
import os
import subprocess
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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
👋 أهلاً وسهلاً *{name}*!

🏪 مرحباً بك في *متجر تفعيلك*
كل اشتراكاتك الرقمية في مكان واحد 🚀

━━━━━━━━━━━━━━━
✅ تفعيل فوري وضمان كامل
💳 أسعار تنافسية
🚀 دعم سريع عبر واتساب
━━━━━━━━━━━━━━━

اختر من القائمة أدناه 👇
"""

MSG_STORE = """
🛒 *متجر تفعيلك*

اختر التصنيف الذي تريده 👇

💡 جميع منتجاتنا أصلية ومضمونة 100%
"""

MSG_SUBSCRIPTIONS = """
📱 *الاشتراكات المتاحة:*

━━━━━━━━━━━━━━━
🎨 *أدوبي كريتف كلاود*
• شهر واحد: 89,000 ج.س
• 3 شهور: 189,000 ج.س

✏️ *كانفا برو*
• شهر واحد: 25,000 ج.س
• 3 شهور: 65,000 ج.س
• سنة: 180,000 ج.س

🎬 *كاب كت برو*
• شهر واحد: 29,000 ج.س
• 6 شهور: 160,000 ج.س

🖼️ *فريبيك بريميوم*
• شهر واحد: 42,000 ج.س
• 3 شهور: 110,000 ج.س
• سنة: 295,000 ج.س

🎥 *نتفليكس*
• شهر - بروفايل: 18,000 ج.س
• 3 شهور - بروفايل: 48,000 ج.س

🎓 *كورسيرا بلاس*
• 6 شهور: 99,000 ج.س
• سنة: 165,000 ج.س
━━━━━━━━━━━━━━━

للطلب اضغط 👇 *اطلب الآن*
"""

MSG_GAMES = """
🎮 *شحن الألعاب:*

━━━━━━━━━━━━━━━
🔫 *PUBG Mobile*
• 60 UC: 5,000 ج.س
• 325 UC: 20,000 ج.س
• 660 UC: 38,000 ج.س
• 1800 UC: 95,000 ج.س

💻 *ويندوز 10/11 برو*
• ويندوز 10 برو: 25,000 ج.س
• ويندوز 11 برو: 36,000 ج.س
━━━━━━━━━━━━━━━

للطلب اضغط 👇 *اطلب الآن*
"""

MSG_ORDER = """
✅ *تم استلام طلبك!*

سيتواصل معك فريقنا خلال دقائق لإتمام الطلب.

📞 *يمكنك أيضاً التواصل مباشرة:*
واتساب: 0123311896
"""

MSG_CONTACT = """
📞 *تواصل معنا*

━━━━━━━━━━━━━━━
📱 *واتساب:* 0123311896
🕐 *أوقات العمل:*
يومياً من 9 صباحاً حتى 11 مساءً
━━━━━━━━━━━━━━━

⚡ نرد على استفساراتكم في أسرع وقت!
"""

MSG_ABOUT = """
ℹ️ *عن متجر تفعيلك*

متجر تفعيلك هو منصتك الرقمية المتخصصة في تفعيل الاشتراكات والمنتجات الرقمية.

━━━━━━━━━━━━━━━
✅ *لماذا تختارنا؟*
• تفعيل فوري خلال دقائق
• اشتراكات أصلية ومضمونة 100%
• دعم سريع عبر واتساب
• أسعار تنافسية
━━━━━━━━━━━━━━━

💡 _تفعيلك… لأنك تستحق خدمة تليق بيك!_
"""

MSG_ADMIN_ONLY    = "⛔ هذا الأمر للأدمن فقط."
MSG_BROADCAST_ASK = "📢 أرسل الرسالة التي تريد إذاعتها لجميع المشتركين:"
MSG_BROADCAST_DONE = "✅ تم إرسال الرسالة لـ {count} مشترك."
MSG_NO_SUBS       = "ℹ️ لا يوجد مشتركون حتى الآن."

# =============================================
#   لوحة المفاتيح الرئيسية (أزرار كبيرة)
# =============================================

def main_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🛒 المتجر"),
        KeyboardButton("🎮 شحن الألعاب"),
        KeyboardButton("📦 طلب الآن"),
        KeyboardButton("📞 تواصل معنا"),
        KeyboardButton("ℹ️ عن المتجر"),
        KeyboardButton("⭐ اشتراكاتي"),
    )
    return kb

def admin_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🛒 المتجر"),
        KeyboardButton("🎮 شحن الألعاب"),
        KeyboardButton("📦 طلب الآن"),
        KeyboardButton("📞 تواصل معنا"),
        KeyboardButton("📊 الإحصائيات"),
        KeyboardButton("📢 رسالة جماعية"),
    )
    return kb

def order_inline():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("📱 اشتراكات", callback_data="order_sub"),
        InlineKeyboardButton("🎮 ألعاب", callback_data="order_games"),
    )
    kb.add(InlineKeyboardButton("💬 تواصل واتساب", url="https://wa.me/0123311896"))
    return kb

def contact_inline():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💬 واتساب", url="https://wa.me/0123311896"))
    return kb

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

# ── /start ────────────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(message):
    user   = message.from_user
    is_new = add_user(user)
    name   = user.first_name or "صديقي"
    kb     = admin_keyboard() if user.id == ADMIN_ID else main_keyboard()
    bot.send_message(message.chat.id, MSG_WELCOME.format(name=name), reply_markup=kb)
    if is_new:
        bot.send_message(
            ADMIN_ID,
            f"🔔 *مستخدم جديد!*\n"
            f"👤 {user.first_name} {user.last_name or ''}\n"
            f"🆔 `{user.id}`\n"
            f"📛 @{user.username or 'بدون'}\n"
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

# ── زر المتجر 🛒 ──────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def btn_store(message):
    bot.send_message(message.chat.id, MSG_STORE)
    bot.send_message(message.chat.id, MSG_SUBSCRIPTIONS, reply_markup=order_inline())

# ── زر الألعاب 🎮 ─────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🎮 شحن الألعاب")
def btn_games(message):
    bot.send_message(message.chat.id, MSG_GAMES, reply_markup=order_inline())

# ── زر طلب الآن 📦 ────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📦 طلب الآن")
def btn_order(message):
    bot.send_message(message.chat.id, MSG_ORDER, reply_markup=contact_inline())
    # إشعار الأدمن
    user = message.from_user
    bot.send_message(
        ADMIN_ID,
        f"🛒 *طلب جديد!*\n"
        f"👤 {user.first_name} {user.last_name or ''}\n"
        f"🆔 `{user.id}`\n"
        f"📛 @{user.username or 'بدون'}\n"
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

# ── زر تواصل 📞 ───────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📞 تواصل معنا")
def btn_contact(message):
    bot.send_message(message.chat.id, MSG_CONTACT, reply_markup=contact_inline())

# ── زر عن المتجر ℹ️ ───────────────────────────
@bot.message_handler(func=lambda m: m.text == "ℹ️ عن المتجر")
def btn_about(message):
    bot.send_message(message.chat.id, MSG_ABOUT)

# ── زر اشتراكاتي ⭐ ───────────────────────────
@bot.message_handler(func=lambda m: m.text == "⭐ اشتراكاتي")
def btn_mysubs(message):
    bot.send_message(
        message.chat.id,
        "📦 *اشتراكاتي*\n\nللاستفسار عن اشتراكاتك تواصل معنا عبر واتساب 👇",
        reply_markup=contact_inline()
    )

# ── زر الإحصائيات 📊 (أدمن) ──────────────────
@bot.message_handler(func=lambda m: m.text == "📊 الإحصائيات")
def btn_stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    s = get_stats()
    bot.send_message(
        message.chat.id,
        f"📊 *إحصائيات المتجر*\n\n"
        f"👥 إجمالي المستخدمين: `{s['total']}`\n"
        f"✅ المشتركون: `{s['subscribed']}`\n"
        f"🔕 غير المشتركين: `{s['unsubscribed']}`\n"
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

# ── زر رسالة جماعية 📢 (أدمن) ────────────────
@bot.message_handler(func=lambda m: m.text == "📢 رسالة جماعية")
def btn_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    if not get_subscribers():
        bot.send_message(message.chat.id, MSG_NO_SUBS)
        return
    waiting_broadcast.add(message.from_user.id)
    bot.send_message(message.chat.id, MSG_BROADCAST_ASK)

# ── Callback Inline ───────────────────────────
@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call):
    if call.data == "order_sub":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
            "📱 *لطلب اشتراك:*\n\nتواصل معنا عبر واتساب وأخبرنا بالاشتراك الذي تريده 👇",
            reply_markup=contact_inline())
    elif call.data == "order_games":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
            "🎮 *لشحن الألعاب:*\n\nتواصل معنا عبر واتساب وأخبرنا باللعبة والكمية 👇",
            reply_markup=contact_inline())

# ── استقبال رسالة الـ broadcast ───────────────
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

# ── أي رسالة أخرى ─────────────────────────────
@bot.message_handler(func=lambda m: True)
def handle_other(message):
    kb = admin_keyboard() if message.from_user.id == ADMIN_ID else main_keyboard()
    bot.send_message(message.chat.id,
        "❓ اختر من القائمة أدناه 👇",
        reply_markup=kb)

# =============================================
#   تشغيل
# =============================================

if __name__ == "__main__":
    print("🤖 EsamBay Bot is running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)

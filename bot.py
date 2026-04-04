import telebot
import json
import os
import subprocess
from datetime import datetime
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ForceReply
)

# =============================================
#   إعدادات البوت
# =============================================

BOT_TOKEN    = "8595374501:AAHssdSP0y8UFbI23CrEPbyPhoxC-r1HncY"
ADMIN_ID     = 1199941388
DB_FILE      = "database.json"
WHATSAPP_NUM = "249129978663"   # ← رقمك الجديد بدون +

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

MSG_CONTACT = """
📞 *تواصل معنا*

━━━━━━━━━━━━━━━
📱 *واتساب:* +{wa}
🕐 *أوقات العمل:*
يومياً من 9 صباحاً حتى 11 مساءً
━━━━━━━━━━━━━━━

⚡ نرد على استفساراتكم في أسرع وقت!
""".format(wa=WHATSAPP_NUM)

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

MSG_ADMIN_ONLY     = "⛔ هذا الأمر للأدمن فقط."
MSG_BROADCAST_ASK  = "📢 أرسل الرسالة التي تريد إذاعتها لجميع المشتركين:"
MSG_BROADCAST_DONE = "✅ تم إرسال الرسالة لـ {count} مشترك."
MSG_NO_SUBS        = "ℹ️ لا يوجد مشتركون حتى الآن."

# =============================================
#   لوحات المفاتيح
# =============================================

def wa_url(text="💬 تواصل واتساب"):
    """زر واتساب موحّد"""
    return InlineKeyboardButton(text, url=f"https://wa.me/{WHATSAPP_NUM}")

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
        InlineKeyboardButton("🎮 ألعاب",    callback_data="order_games"),
    )
    kb.add(wa_url())
    return kb

def contact_inline():
    kb = InlineKeyboardMarkup()
    kb.add(wa_url())
    return kb

def subs_inline():
    """أزرار اختيار نوع الاشتراك"""
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎨 أدوبي",      callback_data="sub_adobe"),
        InlineKeyboardButton("✏️ كانفا برو",  callback_data="sub_canva"),
        InlineKeyboardButton("🎬 كاب كت",     callback_data="sub_capcut"),
        InlineKeyboardButton("🖼️ فريبيك",    callback_data="sub_freepik"),
        InlineKeyboardButton("🎥 نتفليكس",   callback_data="sub_netflix"),
        InlineKeyboardButton("🎓 كورسيرا",   callback_data="sub_coursera"),
    )
    kb.add(wa_url("💬 تواصل مباشر"))
    return kb

def games_inline():
    """أزرار اختيار اللعبة"""
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔫 PUBG Mobile",     callback_data="game_pubg"),
        InlineKeyboardButton("💻 ويندوز 10/11 برو", callback_data="game_windows"),
    )
    kb.add(wa_url("💬 تواصل مباشر"))
    return kb

def pubg_amounts_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("60 UC  - 5,000 ج.س",   callback_data="pubg_60"),
        InlineKeyboardButton("325 UC - 20,000 ج.س",  callback_data="pubg_325"),
        InlineKeyboardButton("660 UC - 38,000 ج.س",  callback_data="pubg_660"),
        InlineKeyboardButton("1800 UC - 95,000 ج.س", callback_data="pubg_1800"),
    )
    return kb

def windows_versions_inline():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("ويندوز 10 برو - 25,000 ج.س", callback_data="win_10"),
        InlineKeyboardButton("ويندوز 11 برو - 36,000 ج.س", callback_data="win_11"),
    )
    return kb

def adobe_periods_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("شهر - 89,000 ج.س",    callback_data="adobe_1m"),
        InlineKeyboardButton("3 شهور - 189,000 ج.س", callback_data="adobe_3m"),
    )
    return kb

def canva_periods_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("شهر - 25,000 ج.س",    callback_data="canva_1m"),
        InlineKeyboardButton("3 شهور - 65,000 ج.س",  callback_data="canva_3m"),
        InlineKeyboardButton("سنة - 180,000 ج.س",    callback_data="canva_1y"),
    )
    return kb

def capcut_periods_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("شهر - 29,000 ج.س",    callback_data="capcut_1m"),
        InlineKeyboardButton("6 شهور - 160,000 ج.س", callback_data="capcut_6m"),
    )
    return kb

def freepik_periods_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("شهر - 42,000 ج.س",     callback_data="freepik_1m"),
        InlineKeyboardButton("3 شهور - 110,000 ج.س", callback_data="freepik_3m"),
        InlineKeyboardButton("سنة - 295,000 ج.س",    callback_data="freepik_1y"),
    )
    return kb

def netflix_periods_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("شهر - 18,000 ج.س",    callback_data="netflix_1m"),
        InlineKeyboardButton("3 شهور - 48,000 ج.س", callback_data="netflix_3m"),
    )
    return kb

def coursera_periods_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("6 شهور - 99,000 ج.س", callback_data="coursera_6m"),
        InlineKeyboardButton("سنة - 165,000 ج.س",   callback_data="coursera_1y"),
    )
    return kb

def confirm_order_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ تأكيد الطلب",  callback_data="confirm_order"),
        InlineKeyboardButton("❌ إلغاء",         callback_data="cancel_order"),
    )
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
        subprocess.run(["git", "config", "user.email", "bot@taf3elk.com"], check=True)
        subprocess.run(["git", "config", "user.name",  "Taf3elk Bot"],     check=True)
        subprocess.run(["git", "add", DB_FILE],                            check=True)
        result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if result.returncode != 0:
            subprocess.run(["git", "commit", "-m",
                f"bot: update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("[OK] Database saved to GitHub")
    except Exception as e:
        print(f"[WARN] Git error: {e}")

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
#   حالة المستخدمين (للطلبات التفصيلية)
# =============================================

# user_id -> {"step": ..., "product": ..., "period": ..., "name": ...}
user_states: dict = {}

def set_state(uid, **kwargs):
    user_states[uid] = user_states.get(uid, {})
    user_states[uid].update(kwargs)

def get_state(uid):
    return user_states.get(uid, {})

def clear_state(uid):
    user_states.pop(uid, None)

# =============================================
#   البوت
# =============================================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
waiting_broadcast = set()

# ─────────────────────────────────────────────
#  /start
# ─────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(message):
    user   = message.from_user
    is_new = add_user(user)
    name   = user.first_name or "صديقي"
    kb     = admin_keyboard() if user.id == ADMIN_ID else main_keyboard()
    clear_state(user.id)

    bot.send_message(message.chat.id, MSG_WELCOME.format(name=name), reply_markup=kb)

    if is_new:
        bot.send_message(
            ADMIN_ID,
            f"*مستخدم جديد!*\n"
            f"الاسم: {user.first_name} {user.last_name or ''}\n"
            f"ID: `{user.id}`\n"
            f"يوزر: @{user.username or 'بدون'}\n"
            f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

# ─────────────────────────────────────────────
#  المتجر
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def btn_store(message):
    bot.send_message(message.chat.id, MSG_STORE)
    bot.send_message(message.chat.id, MSG_SUBSCRIPTIONS, reply_markup=subs_inline())

# ─────────────────────────────────────────────
#  شحن الألعاب
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🎮 شحن الألعاب")
def btn_games(message):
    bot.send_message(message.chat.id, MSG_GAMES, reply_markup=games_inline())

# ─────────────────────────────────────────────
#  طلب الآن (عام)
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📦 طلب الآن")
def btn_order(message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("📱 اشتراكات", callback_data="order_sub"),
        InlineKeyboardButton("🎮 ألعاب",    callback_data="order_games"),
    )
    kb.add(wa_url())
    bot.send_message(
        message.chat.id,
        "📦 *ماذا تريد أن تطلب؟*\n\nاختر نوع الطلب 👇",
        reply_markup=kb
    )

# ─────────────────────────────────────────────
#  تواصل معنا
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📞 تواصل معنا")
def btn_contact(message):
    bot.send_message(message.chat.id, MSG_CONTACT, reply_markup=contact_inline())

# ─────────────────────────────────────────────
#  عن المتجر
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "ℹ️ عن المتجر")
def btn_about(message):
    bot.send_message(message.chat.id, MSG_ABOUT)

# ─────────────────────────────────────────────
#  اشتراكاتي
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "⭐ اشتراكاتي")
def btn_mysubs(message):
    bot.send_message(
        message.chat.id,
        "📦 *اشتراكاتي*\n\nللاستفسار عن اشتراكاتك تواصل معنا عبر واتساب 👇",
        reply_markup=contact_inline()
    )

# ─────────────────────────────────────────────
#  إحصائيات (أدمن)
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📊 الإحصائيات")
def btn_stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    s = get_stats()
    bot.send_message(
        message.chat.id,
        f"📊 *إحصائيات المتجر*\n\n"
        f"إجمالي المستخدمين: `{s['total']}`\n"
        f"المشتركون: `{s['subscribed']}`\n"
        f"غير المشتركين: `{s['unsubscribed']}`\n"
        f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

# ─────────────────────────────────────────────
#  رسالة جماعية (أدمن)
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📢 رسالة جماعية")
def btn_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    if not get_subscribers():
        bot.send_message(message.chat.id, MSG_NO_SUBS)
        return
    waiting_broadcast.add(message.from_user.id)
    bot.send_message(message.chat.id, MSG_BROADCAST_ASK)

# ─────────────────────────────────────────────
#  Callback Handler الموحّد
# ─────────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call):
    uid  = call.from_user.id
    data = call.data

    bot.answer_callback_query(call.id)

    # ── اختيار نوع الطلب ──
    if data == "order_sub":
        bot.send_message(call.message.chat.id,
            "📱 *اختر الاشتراك الذي تريده:*", reply_markup=subs_inline())

    elif data == "order_games":
        bot.send_message(call.message.chat.id,
            "🎮 *اختر اللعبة:*", reply_markup=games_inline())

    # ── اختيار الاشتراك ──
    elif data == "sub_adobe":
        set_state(uid, product="أدوبي كريتف كلاود")
        bot.send_message(call.message.chat.id,
            "🎨 *أدوبي كريتف كلاود*\nاختر المدة:", reply_markup=adobe_periods_inline())

    elif data == "sub_canva":
        set_state(uid, product="كانفا برو")
        bot.send_message(call.message.chat.id,
            "✏️ *كانفا برو*\nاختر المدة:", reply_markup=canva_periods_inline())

    elif data == "sub_capcut":
        set_state(uid, product="كاب كت برو")
        bot.send_message(call.message.chat.id,
            "🎬 *كاب كت برو*\nاختر المدة:", reply_markup=capcut_periods_inline())

    elif data == "sub_freepik":
        set_state(uid, product="فريبيك بريميوم")
        bot.send_message(call.message.chat.id,
            "🖼️ *فريبيك بريميوم*\nاختر المدة:", reply_markup=freepik_periods_inline())

    elif data == "sub_netflix":
        set_state(uid, product="نتفليكس")
        bot.send_message(call.message.chat.id,
            "🎥 *نتفليكس*\nاختر المدة:", reply_markup=netflix_periods_inline())

    elif data == "sub_coursera":
        set_state(uid, product="كورسيرا بلاس")
        bot.send_message(call.message.chat.id,
            "🎓 *كورسيرا بلاس*\nاختر المدة:", reply_markup=coursera_periods_inline())

    # ── اختيار مدة الاشتراكات ──
    elif data in ("adobe_1m","adobe_3m","canva_1m","canva_3m","canva_1y",
                  "capcut_1m","capcut_6m","freepik_1m","freepik_3m","freepik_1y",
                  "netflix_1m","netflix_3m","coursera_6m","coursera_1y"):
        periods = {
            "adobe_1m":    "شهر واحد - 89,000 ج.س",
            "adobe_3m":    "3 شهور - 189,000 ج.س",
            "canva_1m":    "شهر واحد - 25,000 ج.س",
            "canva_3m":    "3 شهور - 65,000 ج.س",
            "canva_1y":    "سنة - 180,000 ج.س",
            "capcut_1m":   "شهر واحد - 29,000 ج.س",
            "capcut_6m":   "6 شهور - 160,000 ج.س",
            "freepik_1m":  "شهر واحد - 42,000 ج.س",
            "freepik_3m":  "3 شهور - 110,000 ج.س",
            "freepik_1y":  "سنة - 295,000 ج.س",
            "netflix_1m":  "شهر واحد - 18,000 ج.س",
            "netflix_3m":  "3 شهور - 48,000 ج.س",
            "coursera_6m": "6 شهور - 99,000 ج.س",
            "coursera_1y": "سنة - 165,000 ج.س",
        }
        set_state(uid, period=periods[data], step="waiting_name")
        bot.send_message(
            call.message.chat.id,
            "✍️ *الخطوة الأخيرة!*\n\nأرسل *اسمك الكامل* لإتمام الطلب:",
            reply_markup=ForceReply(selective=True)
        )

    # ── اختيار اللعبة ──
    elif data == "game_pubg":
        set_state(uid, product="PUBG Mobile")
        bot.send_message(call.message.chat.id,
            "🔫 *PUBG Mobile*\nاختر الكمية:", reply_markup=pubg_amounts_inline())

    elif data == "game_windows":
        set_state(uid, product="ويندوز")
        bot.send_message(call.message.chat.id,
            "💻 *ويندوز*\nاختر الإصدار:", reply_markup=windows_versions_inline())

    elif data in ("pubg_60","pubg_325","pubg_660","pubg_1800"):
        amounts = {
            "pubg_60":   "60 UC - 5,000 ج.س",
            "pubg_325":  "325 UC - 20,000 ج.س",
            "pubg_660":  "660 UC - 38,000 ج.س",
            "pubg_1800": "1800 UC - 95,000 ج.س",
        }
        set_state(uid, period=amounts[data], step="waiting_name")
        bot.send_message(
            call.message.chat.id,
            "✍️ *الخطوة الأخيرة!*\n\nأرسل *اسمك الكامل* أو *ID اللعبة* لإتمام الطلب:",
            reply_markup=ForceReply(selective=True)
        )

    elif data in ("win_10","win_11"):
        versions = {
            "win_10": "ويندوز 10 برو - 25,000 ج.س",
            "win_11": "ويندوز 11 برو - 36,000 ج.س",
        }
        set_state(uid, period=versions[data], step="waiting_name")
        bot.send_message(
            call.message.chat.id,
            "✍️ *الخطوة الأخيرة!*\n\nأرسل *اسمك الكامل* لإتمام الطلب:",
            reply_markup=ForceReply(selective=True)
        )

    # ── تأكيد / إلغاء ──
    elif data == "confirm_order":
        state = get_state(uid)
        user  = call.from_user
        _send_order_to_admin(user, state)
        clear_state(uid)
        kb2 = InlineKeyboardMarkup()
        kb2.add(wa_url("💬 تواصل واتساب للمتابعة"))
        bot.send_message(
            call.message.chat.id,
            "✅ *تم استلام طلبك بنجاح!*\n\n"
            "سيتواصل معك فريقنا خلال دقائق.\n"
            "يمكنك أيضاً التواصل مباشرة 👇",
            reply_markup=kb2
        )

    elif data == "cancel_order":
        clear_state(uid)
        bot.send_message(call.message.chat.id, "❌ *تم إلغاء الطلب.*\n\nيمكنك البدء من جديد 👇",
            reply_markup=main_keyboard())

# ─────────────────────────────────────────────
#  استقبال الاسم بعد اختيار المنتج
# ─────────────────────────────────────────────
def _send_order_to_admin(tg_user, state):
    bot.send_message(
        ADMIN_ID,
        f"*طلب جديد!*\n"
        f"المنتج: {state.get('product','?')}\n"
        f"المدة/الكمية: {state.get('period','?')}\n"
        f"الاسم المُدخل: {state.get('customer_name','?')}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"مُرسِل: {tg_user.first_name} {tg_user.last_name or ''}\n"
        f"ID: `{tg_user.id}`\n"
        f"يوزر: @{tg_user.username or 'بدون'}\n"
        f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "waiting_name")
def handle_customer_name(message):
    uid = message.from_user.id
    set_state(uid, customer_name=message.text, step="confirm")
    state = get_state(uid)

    bot.send_message(
        message.chat.id,
        f"*تأكيد الطلب:*\n\n"
        f"المنتج: *{state.get('product','?')}*\n"
        f"المدة/الكمية: *{state.get('period','?')}*\n"
        f"الاسم: *{message.text}*\n\n"
        f"هل تريد تأكيد الطلب؟",
        reply_markup=confirm_order_inline()
    )

# ─────────────────────────────────────────────
#  Broadcast (أدمن)
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.from_user.id in waiting_broadcast)
def handle_broadcast(message):
    waiting_broadcast.discard(message.from_user.id)
    count = 0
    for user in get_subscribers():
        try:
            bot.send_message(user["id"],
                f"*رسالة من متجر تفعيلك:*\n\n{message.text}")
            count += 1
        except Exception as e:
            print(f"Failed {user['id']}: {e}")
    bot.send_message(message.chat.id, MSG_BROADCAST_DONE.format(count=count))

# ─────────────────────────────────────────────
#  أي رسالة أخرى
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: True)
def handle_other(message):
    kb = admin_keyboard() if message.from_user.id == ADMIN_ID else main_keyboard()
    bot.send_message(message.chat.id, "اختر من القائمة أدناه 👇", reply_markup=kb)

# =============================================
#   تشغيل
# =============================================
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)

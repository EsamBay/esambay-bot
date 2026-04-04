import telebot
import json
import os
import subprocess
import urllib.parse
from datetime import datetime
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# ══════════════════════════════════════════════
#   إعدادات البوت
# ══════════════════════════════════════════════
BOT_TOKEN = "8595374501:AAHssdSP0y8UFbI23CrEPbyPhoxC-r1HncY"
ADMIN_ID  = 1199941388
WHATSAPP  = "249129978663"
DB_FILE   = "database.json"

# ══════════════════════════════════════════════
#   منتجات المتجر
# ══════════════════════════════════════════════
STORE = {
    "🎮 شحن الألعاب": {
        "🔫 PUBG Mobile": {
            "desc": "شحن شدات PUBG Mobile مباشر\n✅ شحن فوري بدون تسجيل\n✅ فقط أرسل الـ ID",
            "variants": [
                ("60 UC",    "5,000 ج.س"),
                ("325 UC",   "20,000 ج.س"),
                ("660 UC",   "38,000 ج.س"),
                ("1800 UC",  "95,000 ج.س"),
                ("3850 UC",  "190,000 ج.س"),
                ("8100 UC",  "380,000 ج.س"),
            ]
        },
        "🔥 FreeFire": {
            "desc": "شحن جواهر FreeFire مباشر\n✅ شحن فوري بالـ ID\n✅ بدون تسجيل دخول",
            "variants": [
                ("100 جوهرة",  "3,000 ج.س"),
                ("310 جوهرة",  "8,000 ج.س"),
                ("520 جوهرة",  "13,000 ج.س"),
                ("1060 جوهرة", "25,000 ج.س"),
                ("2180 جوهرة", "50,000 ج.س"),
                ("5600 جوهرة", "120,000 ج.س"),
            ]
        },
        "⚽ FIFA Mobile": {
            "desc": "شحن FIFA Mobile\n✅ تسليم فوري\n✅ آمن ومضمون",
            "variants": [
                ("100 FC Points",  "5,000 ج.س"),
                ("500 FC Points",  "22,000 ج.س"),
                ("1050 FC Points", "43,000 ج.س"),
                ("2200 FC Points", "85,000 ج.س"),
            ]
        },
        "🏆 Clash of Clans": {
            "desc": "شحن Clash of Clans\n✅ تسليم فوري\n✅ جواهر أصلية",
            "variants": [
                ("80 جوهرة",   "3,000 ج.س"),
                ("500 جوهرة",  "15,000 ج.س"),
                ("1200 جوهرة", "33,000 ج.س"),
                ("2500 جوهرة", "65,000 ج.س"),
            ]
        },
        "🎯 Call of Duty": {
            "desc": "شحن Call of Duty Mobile\n✅ تسليم فوري\n✅ CP أصلية",
            "variants": [
                ("80 CP",   "5,000 ج.س"),
                ("400 CP",  "22,000 ج.س"),
                ("800 CP",  "42,000 ج.س"),
                ("2000 CP", "100,000 ج.س"),
            ]
        },
        "🌟 Brawl Stars": {
            "desc": "شحن Brawl Stars\n✅ تسليم فوري\n✅ جواهر أصلية",
            "variants": [
                ("30 جوهرة",  "5,000 ج.س"),
                ("80 جوهرة",  "12,000 ج.س"),
                ("170 جوهرة", "24,000 ج.س"),
                ("360 جوهرة", "48,000 ج.س"),
            ]
        },
        "🐉 Mobile Legends": {
            "desc": "شحن Mobile Legends\n✅ تسليم فوري\n✅ ألماس أصلي",
            "variants": [
                ("86 ألماس",   "5,000 ج.س"),
                ("172 ألماس",  "9,000 ج.س"),
                ("706 ألماس",  "34,000 ج.س"),
                ("2195 ألماس", "100,000 ج.س"),
            ]
        },
        "🌍 Genshin Impact": {
            "desc": "شحن Genshin Impact\n✅ تسليم فوري",
            "variants": [
                ("60 Crystals",   "3,000 ج.س"),
                ("300 Crystals",  "14,000 ج.س"),
                ("980 Crystals",  "42,000 ج.س"),
                ("1980 Crystals", "82,000 ج.س"),
            ]
        },
    },
    "🃏 بطاقات الألعاب": {
        "🎮 بطاقات FreeFire": {
            "desc": "بطاقات FreeFire رقمية\n✅ كود فوري بعد الطلب",
            "variants": [
                ("100 جوهرة",  "4,000 ج.س"),
                ("310 جوهرة",  "10,000 ج.س"),
                ("1060 جوهرة", "30,000 ج.س"),
            ]
        },
        "🔫 بطاقات PUBG Mobile": {
            "desc": "بطاقات PUBG Mobile\n✅ كود فوري بعد الطلب",
            "variants": [
                ("60 UC",   "6,000 ج.س"),
                ("325 UC",  "22,000 ج.س"),
                ("660 UC",  "42,000 ج.س"),
                ("1800 UC", "100,000 ج.س"),
            ]
        },
        "🍎 بطاقات iTunes": {
            "desc": "بطاقات iTunes / App Store\n✅ كود فوري بعد الطلب",
            "variants": [
                ("7$",   "21,000 ج.س"),
                ("15$",  "43,000 ج.س"),
                ("25$",  "70,000 ج.س"),
                ("50$",  "135,000 ج.س"),
                ("100$", "265,000 ج.س"),
            ]
        },
        "🎮 بطاقات PlayStation": {
            "desc": "بطاقات PlayStation Network\n✅ كود فوري بعد الطلب",
            "variants": [
                ("10$", "30,000 ج.س"),
                ("20$", "57,000 ج.س"),
                ("50$", "135,000 ج.س"),
                ("100$","265,000 ج.س"),
            ]
        },
        "💻 بطاقات Steam": {
            "desc": "بطاقات Steam\n✅ كود فوري بعد الطلب",
            "variants": [
                ("5$",  "15,000 ج.س"),
                ("10$", "28,000 ج.س"),
                ("20$", "54,000 ج.س"),
                ("50$", "130,000 ج.س"),
            ]
        },
        "🟥 بطاقات Roblox": {
            "desc": "بطاقات Roblox\n✅ كود فوري بعد الطلب",
            "variants": [
                ("400 Robux",  "12,000 ج.س"),
                ("800 Robux",  "22,000 ج.س"),
                ("1700 Robux", "43,000 ج.س"),
            ]
        },
        "🟢 بطاقات Xbox": {
            "desc": "بطاقات Xbox Gift Card\n✅ كود فوري بعد الطلب",
            "variants": [
                ("5$",  "15,000 ج.س"),
                ("10$", "28,000 ج.س"),
                ("20$", "54,000 ج.س"),
                ("50$", "130,000 ج.س"),
            ]
        },
    },
    "💳 الدفع الإلكتروني": {
        "🛰️ اشتراك Starlink": {
            "desc": "تجديد اشتراك Starlink\n✅ تجديد فوري بأرخص الأسعار",
            "variants": [
                ("شهر - Residential", "45,000 ج.س"),
                ("شهر - Roam",        "130,000 ج.س"),
                ("شهر - Business",    "200,000 ج.س"),
            ]
        },
        "🧾 تسديد فاتورة": {
            "desc": "تسديد أي فاتورة إلكترونية\n✅ Visa / Mastercard / PayPal",
            "variants": [
                ("حتى 10$",  "30,000 ج.س"),
                ("حتى 25$",  "70,000 ج.س"),
                ("حتى 50$",  "135,000 ج.س"),
                ("حتى 100$", "265,000 ج.س"),
            ]
        },
        "🎵 شحن عملات TikTok": {
            "desc": "شحن عملات TikTok Live\n✅ بأقل الأسعار",
            "variants": [
                ("70 عملة",   "5,000 ج.س"),
                ("350 عملة",  "22,000 ج.س"),
                ("700 عملة",  "42,000 ج.س"),
                ("1400 عملة", "82,000 ج.س"),
            ]
        },
    },
    "📲 سوشال ميديا": {
        "🎵 تزويد TikTok": {
            "desc": "زيادة TikTok\n✅ متابعين / لايكات / مشاهدات",
            "variants": [
                ("1000 متابع",   "8,000 ج.س"),
                ("5000 متابع",   "35,000 ج.س"),
                ("10000 متابع",  "65,000 ج.س"),
                ("1000 لايك",    "3,000 ج.س"),
                ("10000 مشاهدة", "2,000 ج.س"),
            ]
        },
        "📘 تزويد Facebook": {
            "desc": "زيادة Facebook\n✅ متابعين / لايكات صفحة",
            "variants": [
                ("1000 متابع",  "8,000 ج.س"),
                ("5000 متابع",  "35,000 ج.س"),
                ("10000 متابع", "65,000 ج.س"),
            ]
        },
        "📸 تزويد Instagram": {
            "desc": "زيادة Instagram\n✅ متابعين / لايكات",
            "variants": [
                ("1000 متابع",  "7,000 ج.س"),
                ("5000 متابع",  "30,000 ج.س"),
                ("10000 متابع", "55,000 ج.س"),
            ]
        },
        "▶️ تزويد YouTube": {
            "desc": "زيادة YouTube\n✅ مشتركين / مشاهدات",
            "variants": [
                ("1000 مشترك",   "20,000 ج.س"),
                ("5000 مشترك",   "90,000 ج.س"),
                ("10000 مشاهدة", "5,000 ج.س"),
            ]
        },
        "✈️ تزويد Telegram": {
            "desc": "زيادة Telegram\n✅ أعضاء قناة / مجموعة",
            "variants": [
                ("1000 عضو",  "12,000 ج.س"),
                ("5000 عضو",  "55,000 ج.س"),
                ("10000 عضو", "100,000 ج.س"),
            ]
        },
        "👻 تزويد Snapchat": {
            "desc": "زيادة Snapchat\n✅ متابعين / مشاهدات",
            "variants": [
                ("500 متابع",  "18,000 ج.س"),
                ("1000 متابع", "33,000 ج.س"),
                ("5000 متابع", "150,000 ج.س"),
            ]
        },
    },
    "📱 الاشتراكات": {
        "🎨 أدوبي كريتف كلاود": {
            "desc": "Adobe Creative Cloud\n✅ فوتوشوب، بريمير، إليستريتور\n✅ تفعيل فوري وضمان كامل",
            "variants": [
                ("شهر واحد", "99,000 ج.س"),
                ("3 شهور",   "199,000 ج.س"),
            ]
        },
        "✏️ كانفا برو": {
            "desc": "Canva Pro\n✅ آلاف القوالب الاحترافية",
            "variants": [
                ("شهر واحد", "25,000 ج.س"),
                ("3 شهور",   "65,000 ج.س"),
                ("سنة",      "180,000 ج.س"),
            ]
        },
        "🎬 كاب كت برو": {
            "desc": "CapCut Pro\n✅ مونتاج احترافي\n✅ حساب جاهز",
            "variants": [
                ("شهر واحد", "29,000 ج.س"),
                ("6 شهور",   "160,000 ج.س"),
            ]
        },
        "🎥 نتفليكس": {
            "desc": "Netflix\n✅ محتوى عربي وعالمي\n✅ جودة 4K",
            "variants": [
                ("شهر - بروفايل",    "18,000 ج.س"),
                ("3 شهور - بروفايل", "48,000 ج.س"),
            ]
        },
        "✈️ تيليجرام بريميوم": {
            "desc": "Telegram Premium\n✅ ستيكرات حصرية\n✅ رفع ملفات كبيرة",
            "variants": [
                ("3 شهور", "120,000 ج.س"),
                ("6 شهور", "200,000 ج.س"),
                ("سنة",    "275,000 ج.س"),
            ]
        },
        "🤖 ChatGPT Business": {
            "desc": "ChatGPT Business\n✅ GPT-4 بدون حدود",
            "variants": [
                ("شهر واحد", "35,000 ج.س"),
            ]
        },
        "🎓 كورسيرا بلاس": {
            "desc": "Coursera Plus\n✅ شهادات معترف بها دولياً",
            "variants": [
                ("6 شهور", "99,000 ج.س"),
                ("سنة",    "165,000 ج.س"),
            ]
        },
    },
}

# ══════════════════════════════════════════════
#   قاعدة البيانات
# ══════════════════════════════════════════════
def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "orders": []}
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
        subprocess.run(["git", "add", DB_FILE], check=True)
        r = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if r.returncode != 0:
            subprocess.run(["git", "commit", "-m",
                f"update {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push"], check=True)
    except Exception as e:
        print(f"Git: {e}")

def add_user(user):
    db  = load_db()
    uid = str(user.id)
    new = uid not in db["users"]
    if new:
        db["users"][uid] = {
            "id":       user.id,
            "name":     f"{user.first_name or ''} {user.last_name or ''}".strip(),
            "username": user.username or "",
            "joined":   datetime.now().isoformat(),
        }
        save_db(db)
    return new

def save_order(user, cat, product, variant, price):
    db = load_db()
    oid = len(db.get("orders", [])) + 1
    db.setdefault("orders", []).append({
        "id":       oid,
        "user_id":  user.id,
        "name":     f"{user.first_name or ''} {user.last_name or ''}".strip(),
        "username": user.username or "",
        "category": cat,
        "product":  product,
        "variant":  variant,
        "price":    price,
        "status":   "pending",
        "time":     datetime.now().isoformat(),
        "note":     "",
    })
    save_db(db)
    return oid

def get_order_by_id(oid):
    db = load_db()
    for i, o in enumerate(db.get("orders", [])):
        if o["id"] == int(oid):
            return i, o
    return None, None

def update_order_status(oid, status):
    db = load_db()
    for o in db["orders"]:
        if o["id"] == int(oid):
            o["status"]  = status
            o["updated"] = datetime.now().isoformat()
            break
    save_db(db)

def get_stats():
    db = load_db()
    orders = db.get("orders", [])
    return {
        "users":      len(db["users"]),
        "total":      len(orders),
        "pending":    sum(1 for o in orders if o.get("status") == "pending"),
        "processing": sum(1 for o in orders if o.get("status") == "processing"),
        "done":       sum(1 for o in orders if o.get("status") == "done"),
        "cancelled":  sum(1 for o in orders if o.get("status") == "cancelled"),
    }

# ══════════════════════════════════════════════
#   لوحات المفاتيح - العميل
# ══════════════════════════════════════════════
def kb_main(is_admin=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🛒 المتجر"),
        KeyboardButton("📦 طلباتي"),
        KeyboardButton("📞 تواصل معنا"),
        KeyboardButton("ℹ️ عن المتجر"),
    )
    if is_admin:
        kb.add(KeyboardButton("⚙️ لوحة التحكم"))
    return kb

def kb_categories():
    kb = InlineKeyboardMarkup(row_width=1)
    for cat in STORE:
        kb.add(InlineKeyboardButton(cat, callback_data=f"CAT|{cat}"))
    return kb

def kb_products(cat):
    kb = InlineKeyboardMarkup(row_width=1)
    for prod in STORE[cat]:
        kb.add(InlineKeyboardButton(prod, callback_data=f"PROD|{cat}|{prod}"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="BACK_CATS"))
    return kb

def kb_variants(cat, prod):
    kb = InlineKeyboardMarkup(row_width=1)
    for i, (vname, vprice) in enumerate(STORE[cat][prod]["variants"]):
        kb.add(InlineKeyboardButton(
            f"✅  {vname}  ←  {vprice}",
            callback_data=f"VAR|{cat}|{prod}|{i}"
        ))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data=f"CAT|{cat}"))
    return kb

def kb_confirm(cat, prod, vi):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ تأكيد", callback_data=f"CONFIRM|{cat}|{prod}|{vi}"),
        InlineKeyboardButton("❌ إلغاء", callback_data=f"PROD|{cat}|{prod}"),
    )
    return kb

def kb_after_order(cat, prod, vi):
    vname, vprice = STORE[cat][prod]["variants"][vi]
    msg = f"مرحباً، أريد إتمام طلبي:\n📦 {prod}\n📌 {vname}\n💰 {vprice}"
    kb  = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💬 تواصل واتساب لإتمام الدفع",
            url=f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"),
        InlineKeyboardButton("📦 طلباتي",      callback_data="MY_ORDERS"),
        InlineKeyboardButton("🛒 متابعة التسوق", callback_data="BACK_CATS"),
    )
    return kb

# ══════════════════════════════════════════════
#   لوحات المفاتيح - الأدمن
# ══════════════════════════════════════════════
STATUS_EMOJI = {
    "pending":    "🟡 معلق",
    "processing": "🔵 قيد التنفيذ",
    "done":       "✅ مكتمل",
    "cancelled":  "❌ ملغي",
}

def kb_admin_main():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🟡 الطلبات المعلقة",     callback_data="ADMIN_ORDERS|pending"),
        InlineKeyboardButton("🔵 قيد التنفيذ",         callback_data="ADMIN_ORDERS|processing"),
        InlineKeyboardButton("✅ الطلبات المكتملة",     callback_data="ADMIN_ORDERS|done"),
        InlineKeyboardButton("❌ الملغية",              callback_data="ADMIN_ORDERS|cancelled"),
        InlineKeyboardButton("📊 إحصائيات",            callback_data="ADMIN_STATS"),
        InlineKeyboardButton("👥 المستخدمون",           callback_data="ADMIN_USERS"),
        InlineKeyboardButton("📢 رسالة جماعية",         callback_data="ADMIN_BROADCAST"),
    )
    return kb

def kb_order_actions(oid, status, user_id):
    kb = InlineKeyboardMarkup(row_width=2)
    # أزرار تغيير الحالة
    if status != "processing":
        kb.add(InlineKeyboardButton("🔵 قيد التنفيذ",
               callback_data=f"SET_STATUS|{oid}|processing"))
    if status != "done":
        kb.add(InlineKeyboardButton("✅ تم التنفيذ",
               callback_data=f"SET_STATUS|{oid}|done"))
    if status != "cancelled":
        kb.add(InlineKeyboardButton("❌ إلغاء الطلب",
               callback_data=f"SET_STATUS|{oid}|cancelled"))
    if status != "pending":
        kb.add(InlineKeyboardButton("🟡 إعادة لمعلق",
               callback_data=f"SET_STATUS|{oid}|pending"))
    # مراسلة العميل وواتساب
    kb.add(
        InlineKeyboardButton("💬 مراسلة العميل",
               callback_data=f"MSG_USER|{user_id}|{oid}"),
        InlineKeyboardButton("📱 واتساب العميل",
               url=f"https://wa.me/{WHATSAPP}"),
    )
    kb.add(InlineKeyboardButton("🔙 رجوع للطلبات",
               callback_data=f"ADMIN_ORDERS|{status}"))
    return kb

def kb_orders_list(status):
    db     = load_db()
    orders = [o for o in db.get("orders", []) if o.get("status") == status]
    kb     = InlineKeyboardMarkup(row_width=1)
    if not orders:
        kb.add(InlineKeyboardButton("لا توجد طلبات", callback_data="NONE"))
    else:
        for o in reversed(orders[-10:]):
            label = f"#{o['id']} | {o['product'][:20]} | {o['name'][:10]}"
            kb.add(InlineKeyboardButton(label, callback_data=f"VIEW_ORDER|{o['id']}"))
    kb.add(InlineKeyboardButton("🔙 لوحة التحكم", callback_data="ADMIN_PANEL"))
    return kb

# ══════════════════════════════════════════════
#   البوت
# ══════════════════════════════════════════════
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
waiting_broadcast = set()
waiting_msg_user  = {}   # admin_id -> target_user_id

# ─────────────────────────────────────────────
#   /start
# ─────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(message):
    user   = message.from_user
    is_new = add_user(user)
    name   = user.first_name or "صديقي"
    is_adm = user.id == ADMIN_ID

    bot.send_message(
        message.chat.id,
        f"👋 أهلاً *{name}*!\n\n"
        f"🏪 مرحباً بك في *متجر EsamBay*\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎮 شحن الألعاب المباشر\n"
        f"🃏 بطاقات الألعاب\n"
        f"💳 الدفع الإلكتروني\n"
        f"📲 خدمات السوشال ميديا\n"
        f"📱 الاشتراكات الرقمية\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"✅ تسليم فوري وضمان كامل\n"
        f"اضغط *🛒 المتجر* للبدء 👇",
        reply_markup=kb_main(is_adm)
    )
    if is_new and not is_adm:
        try:
            bot.send_message(
                ADMIN_ID,
                f"🔔 *مستخدم جديد!*\n"
                f"👤 {user.first_name} {user.last_name or ''}\n"
                f"🆔 `{user.id}`\n"
                f"📛 @{user.username or 'بدون'}"
            )
        except: pass

# ─────────────────────────────────────────────
#   أزرار العميل
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def btn_store(message):
    bot.send_message(message.chat.id,
        "🛒 *اختر التصنيف* 👇", reply_markup=kb_categories())

@bot.message_handler(func=lambda m: m.text == "📦 طلباتي")
def btn_myorders(message):
    db  = load_db()
    uid = str(message.from_user.id)
    orders = [o for o in db.get("orders", []) if str(o.get("user_id")) == uid]
    if not orders:
        bot.send_message(message.chat.id,
            "📦 *طلباتي*\n\nلا توجد طلبات بعد.\nاضغط 🛒 المتجر للبدء!")
        return
    text = "📦 *آخر طلباتك:*\n\n"
    for o in reversed(orders[-5:]):
        st = STATUS_EMOJI.get(o.get("status"), "⚪")
        text += (
            f"━━━━━━━━━━\n"
            f"🔢 طلب #{o['id']}\n"
            f"📦 {o['product']}\n"
            f"📌 {o['variant']} — {o['price']}\n"
            f"📊 {st}\n"
        )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "📞 تواصل معنا")
def btn_contact(message):
    msg = "مرحباً، أحتاج مساعدة 👋"
    kb  = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💬 واتساب",
           url=f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"))
    bot.send_message(message.chat.id,
        f"📞 *تواصل معنا*\n\n"
        f"📱 واتساب: +{WHATSAPP}\n"
        f"🕐 يومياً 9ص — 11م\n\n"
        f"⚡ نرد في أسرع وقت!", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "ℹ️ عن المتجر")
def btn_about(message):
    bot.send_message(message.chat.id,
        "ℹ️ *متجر EsamBay*\n\n"
        "منصتك الرقمية لكل احتياجاتك\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🎮 شحن مباشر لجميع الألعاب\n"
        "🃏 بطاقات ألعاب رقمية\n"
        "💳 دفع إلكتروني لأي موقع\n"
        "📲 خدمات سوشال ميديا\n"
        "📱 اشتراكات رقمية أصلية\n"
        "━━━━━━━━━━━━━━━\n"
        "✅ تسليم فوري\n"
        "🔒 آمن ومضمون 100%")

# ─────────────────────────────────────────────
#   ⚙️ لوحة التحكم - الأدمن
# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "⚙️ لوحة التحكم")
def btn_admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    s = get_stats()
    bot.send_message(
        message.chat.id,
        f"⚙️ *لوحة تحكم المدير*\n\n"
        f"👥 المستخدمون: `{s['users']}`\n"
        f"🛒 إجمالي الطلبات: `{s['total']}`\n"
        f"🟡 معلقة: `{s['pending']}`\n"
        f"🔵 قيد التنفيذ: `{s['processing']}`\n"
        f"✅ مكتملة: `{s['done']}`\n"
        f"❌ ملغية: `{s['cancelled']}`\n\n"
        f"اختر ما تريد 👇",
        reply_markup=kb_admin_main()
    )

# رسالة جماعية
@bot.message_handler(func=lambda m: m.from_user.id in waiting_broadcast)
def do_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    waiting_broadcast.discard(message.from_user.id)
    db    = load_db()
    count = 0
    for u in db["users"].values():
        try:
            bot.send_message(u["id"],
                f"📢 *رسالة من متجر EsamBay:*\n\n{message.text}")
            count += 1
        except: pass
    bot.send_message(message.chat.id, f"✅ أُرسلت لـ {count} مستخدم.")

# مراسلة عميل محدد
@bot.message_handler(func=lambda m: m.from_user.id in waiting_msg_user)
def do_msg_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    target = waiting_msg_user.pop(message.from_user.id)
    try:
        bot.send_message(
            target,
            f"💬 *رسالة من متجر EsamBay:*\n\n{message.text}"
        )
        bot.send_message(message.chat.id, "✅ تم إرسال الرسالة للعميل!")
    except:
        bot.send_message(message.chat.id, "❌ فشل إرسال الرسالة.")

# ══════════════════════════════════════════════
#   Callback - كل المنطق
# ══════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: True)
def on_callback(call):
    cid  = call.message.chat.id
    mid  = call.message.message_id
    data = call.data
    bot.answer_callback_query(call.id)

    def edit(text, kb):
        try:
            bot.edit_message_text(text, cid, mid,
                parse_mode="Markdown", reply_markup=kb)
        except:
            bot.send_message(cid, text,
                parse_mode="Markdown", reply_markup=kb)

    # ══ تنقل المتجر ══════════════════════════

    if data == "BACK_CATS":
        edit("🛒 *اختر التصنيف* 👇", kb_categories())

    elif data == "MY_ORDERS":
        db  = load_db()
        uid = str(call.from_user.id)
        orders = [o for o in db.get("orders", []) if str(o.get("user_id")) == uid]
        if not orders:
            edit("📦 لا توجد طلبات بعد.\nاضغط 🛒 المتجر!", kb_categories())
            return
        text = "📦 *آخر طلباتك:*\n\n"
        for o in reversed(orders[-5:]):
            st = STATUS_EMOJI.get(o.get("status"), "⚪")
            text += f"🔢 #{o['id']} | {o['product']} | {o['variant']}\n{st}\n\n"
        edit(text, InlineKeyboardMarkup().add(
            InlineKeyboardButton("🛒 متابعة التسوق", callback_data="BACK_CATS")))

    elif data.startswith("CAT|"):
        cat = data[4:]
        edit(f"{cat}\n\nاختر المنتج 👇", kb_products(cat))

    elif data.startswith("PROD|"):
        _, cat, prod = data.split("|", 2)
        p = STORE[cat][prod]
        edit(
            f"{prod}\n\n📝 {p['desc']}\n\n💰 *اختر الباقة:*",
            kb_variants(cat, prod)
        )

    elif data.startswith("VAR|"):
        _, cat, prod, vi = data.split("|", 3)
        vi = int(vi)
        vname, vprice = STORE[cat][prod]["variants"][vi]
        edit(
            f"🛒 *تأكيد الطلب*\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📦 {prod}\n"
            f"📌 {vname}\n"
            f"💰 {vprice}\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"هل تريد تأكيد الطلب؟",
            kb_confirm(cat, prod, vi)
        )

    elif data.startswith("CONFIRM|"):
        _, cat, prod, vi = data.split("|", 3)
        vi   = int(vi)
        user = call.from_user
        vname, vprice = STORE[cat][prod]["variants"][vi]
        oid  = save_order(user, cat, prod, vname, vprice)

        edit(
            f"✅ *تم استلام طلبك!*\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔢 رقم الطلب: *#{oid}*\n"
            f"📦 {prod}\n"
            f"📌 {vname}\n"
            f"💰 {vprice}\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"اضغط الزر أدناه للتواصل\nوإتمام الدفع 👇",
            kb_after_order(cat, prod, vi)
        )

        # إشعار الأدمن بالطلب الجديد
        try:
            kb_notif = InlineKeyboardMarkup()
            kb_notif.add(InlineKeyboardButton(
                f"📋 عرض الطلب #{oid}",
                callback_data=f"VIEW_ORDER|{oid}"
            ))
            bot.send_message(
                ADMIN_ID,
                f"🛒 *طلب جديد #{oid}!*\n\n"
                f"👤 {user.first_name} {user.last_name or ''}\n"
                f"🆔 `{user.id}`\n"
                f"📛 @{user.username or 'بدون'}\n"
                f"━━━━━━━━━━\n"
                f"📁 {cat}\n"
                f"📦 {prod}\n"
                f"📌 {vname}\n"
                f"💰 {vprice}\n"
                f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                reply_markup=kb_notif
            )
        except: pass

    # ══ لوحة تحكم الأدمن ══════════════════════

    elif data == "ADMIN_PANEL":
        if call.from_user.id != ADMIN_ID:
            return
        s = get_stats()
        edit(
            f"⚙️ *لوحة تحكم المدير*\n\n"
            f"👥 المستخدمون: `{s['users']}`\n"
            f"🟡 معلقة: `{s['pending']}`\n"
            f"🔵 قيد التنفيذ: `{s['processing']}`\n"
            f"✅ مكتملة: `{s['done']}`\n"
            f"❌ ملغية: `{s['cancelled']}`\n\n"
            f"اختر ما تريد 👇",
            kb_admin_main()
        )

    elif data.startswith("ADMIN_ORDERS|"):
        if call.from_user.id != ADMIN_ID:
            return
        status = data.split("|")[1]
        db     = load_db()
        orders = [o for o in db.get("orders", []) if o.get("status") == status]
        count  = len(orders)
        st_txt = STATUS_EMOJI.get(status, status)
        edit(
            f"📋 *الطلبات - {st_txt}*\n\n"
            f"العدد: `{count}`\n\n"
            f"اضغط على أي طلب للتفاصيل 👇",
            kb_orders_list(status)
        )

    elif data.startswith("VIEW_ORDER|"):
        if call.from_user.id != ADMIN_ID:
            return
        oid      = data.split("|")[1]
        _, order = get_order_by_id(oid)
        if not order:
            bot.answer_callback_query(call.id, "الطلب غير موجود!", show_alert=True)
            return
        st  = STATUS_EMOJI.get(order.get("status"), "⚪")
        usr = order.get("username", "")
        edit(
            f"📋 *تفاصيل الطلب #{order['id']}*\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👤 العميل: {order['name']}\n"
            f"🆔 ID: `{order['user_id']}`\n"
            f"📛 @{usr if usr else 'بدون'}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📁 {order.get('category','')}\n"
            f"📦 {order['product']}\n"
            f"📌 {order['variant']}\n"
            f"💰 {order['price']}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 الحالة: {st}\n"
            f"📅 {order['time'][:16]}\n\n"
            f"اختر الإجراء 👇",
            kb_order_actions(order['id'], order['status'], order['user_id'])
        )

    elif data.startswith("SET_STATUS|"):
        if call.from_user.id != ADMIN_ID:
            return
        _, oid, new_status = data.split("|")
        _, order = get_order_by_id(oid)
        if not order:
            return
        update_order_status(oid, new_status)
        st_txt = STATUS_EMOJI.get(new_status, new_status)

        # إشعار العميل بتغيير حالة الطلب
        notif_msgs = {
            "processing": f"🔵 *تحديث طلبك #{oid}*\n\nطلبك قيد التنفيذ الآن!\nسيتم التواصل معك قريباً. ✨",
            "done":       f"✅ *تم تنفيذ طلبك #{oid}*\n\nشكراً لتسوقك معنا في متجر EsamBay! 🎉",
            "cancelled":  f"❌ *تم إلغاء طلبك #{oid}*\n\nللاستفسار تواصل معنا عبر واتساب.",
            "pending":    f"🟡 *طلبك #{oid} معلق*\n\nسيتم مراجعته قريباً.",
        }
        try:
            kb_u = InlineKeyboardMarkup()
            kb_u.add(InlineKeyboardButton("📦 طلباتي", callback_data="MY_ORDERS"))
            bot.send_message(order['user_id'],
                notif_msgs.get(new_status, f"تم تحديث طلبك #{oid}"),
                reply_markup=kb_u)
        except: pass

        bot.answer_callback_query(call.id, f"✅ تم تغيير الحالة إلى {st_txt}", show_alert=True)

        # إعادة تحميل الطلب بعد التحديث
        _, updated = get_order_by_id(oid)
        edit(
            f"📋 *تفاصيل الطلب #{updated['id']}*\n\n"
            f"📦 {updated['product']}\n"
            f"📌 {updated['variant']}\n"
            f"💰 {updated['price']}\n"
            f"📊 الحالة: {STATUS_EMOJI.get(updated['status'],'⚪')}\n"
            f"✅ تم التحديث بنجاح!",
            kb_order_actions(updated['id'], updated['status'], updated['user_id'])
        )

    elif data.startswith("MSG_USER|"):
        if call.from_user.id != ADMIN_ID:
            return
        _, user_id, oid = data.split("|")
        waiting_msg_user[ADMIN_ID] = int(user_id)
        edit(
            f"💬 *مراسلة العميل*\n\n"
            f"الطلب: #{oid}\n\n"
            f"أرسل الرسالة التي تريد إيصالها للعميل:",
            InlineKeyboardMarkup().add(
                InlineKeyboardButton("❌ إلغاء", callback_data=f"VIEW_ORDER|{oid}")
            )
        )

    elif data == "ADMIN_STATS":
        if call.from_user.id != ADMIN_ID:
            return
        s = get_stats()
        edit(
            f"📊 *إحصائيات المتجر*\n\n"
            f"👥 المستخدمون: `{s['users']}`\n"
            f"🛒 إجمالي الطلبات: `{s['total']}`\n"
            f"🟡 معلقة: `{s['pending']}`\n"
            f"🔵 قيد التنفيذ: `{s['processing']}`\n"
            f"✅ مكتملة: `{s['done']}`\n"
            f"❌ ملغية: `{s['cancelled']}`\n"
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            InlineKeyboardMarkup().add(
                InlineKeyboardButton("🔙 رجوع", callback_data="ADMIN_PANEL"))
        )

    elif data == "ADMIN_USERS":
        if call.from_user.id != ADMIN_ID:
            return
        db    = load_db()
        users = list(db["users"].values())[-10:]
        text  = f"👥 *آخر المستخدمين ({len(db['users'])} إجمالاً)*\n\n"
        for u in reversed(users):
            text += f"👤 {u['name']} | `{u['id']}` | @{u.get('username','بدون')}\n"
        edit(text, InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 رجوع", callback_data="ADMIN_PANEL")))

    elif data == "ADMIN_BROADCAST":
        if call.from_user.id != ADMIN_ID:
            return
        waiting_broadcast.add(ADMIN_ID)
        edit(
            "📢 *رسالة جماعية*\n\nأرسل الرسالة التي تريد إذاعتها لجميع المستخدمين:",
            InlineKeyboardMarkup().add(
                InlineKeyboardButton("❌ إلغاء", callback_data="ADMIN_PANEL"))
        )

    elif data == "NONE":
        bot.answer_callback_query(call.id, "لا توجد طلبات في هذه الحالة")

# ─────────────────────────────────────────────
@bot.message_handler(func=lambda m: True)
def other(message):
    bot.send_message(message.chat.id,
        "اضغط *🛒 المتجر* للبدء 👇",
        reply_markup=kb_main(message.from_user.id == ADMIN_ID))

# ══════════════════════════════════════════════
if __name__ == "__main__":
    print("🤖 EsamBay Bot running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)

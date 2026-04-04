import telebot
import json
import os
import subprocess
from datetime import datetime
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# =============================================
#   إعدادات البوت
# =============================================
BOT_TOKEN = "8595374501:AAHssdSP0y8UFbI23CrEPbyPhoxC-r1HncY"
ADMIN_ID  = 1199941388
WHATSAPP  = "+249129978663"
DB_FILE   = "database.json"

# =============================================
#   قاعدة بيانات المنتجات الكاملة
# =============================================
CATEGORIES = {
    "sub":      "📱 الاشتراكات",
    "ai":       "🤖 ذكاء اصطناعي",
    "creative": "🎨 باكجات الإبداع",
    "edu":      "🎓 برامج تعليمية",
    "social":   "📲 سوشال ميديا",
    "games":    "🎮 ألعاب",
    "computer": "💻 كمبيوتر",
    "mobile":   "📱 الهاتف",
    "crypto":   "💰 عملات رقمية",
}

PRODUCTS = {
    # ── الاشتراكات ──────────────────────────────
    "adobe": {
        "name": "🎨 أدوبي كريتف كلاود",
        "cat": "sub",
        "desc": "كل أدوات الإبداع في مكان واحد\n✅ فوتوشوب، إليستريتور، بريمير وأكثر\n✅ تفعيل فوري وضمان كامل",
        "variants": [
            ("شهر واحد", "99,000 ج.س"),
            ("3 شهور",   "199,000 ج.س"),
        ]
    },
    "canva": {
        "name": "✏️ كانفا برو",
        "cat": "sub",
        "desc": "فعّل Canva Pro وخلي إبداعك يلمع\n✅ آلاف القوالب الاحترافية\n✅ تصاميم بجودة عالية",
        "variants": [
            ("شهر واحد", "25,000 ج.س"),
            ("3 شهور",   "65,000 ج.س"),
            ("سنة",      "180,000 ج.س"),
        ]
    },
    "capcut": {
        "name": "🎬 كاب كت برو",
        "cat": "sub",
        "desc": "مونتاج أسرع.. فيديوهات أروع\n✅ حساب جاهز للاستخدام الفوري\n✅ أدوات مونتاج احترافية",
        "variants": [
            ("شهر واحد", "29,000 ج.س"),
            ("6 شهور",   "160,000 ج.س"),
        ]
    },
    "freepik": {
        "name": "🖼️ فريبيك بريميوم",
        "cat": "sub",
        "desc": "ملايين الصور والمتجهات\n✅ موارد مجانية عالية الجودة\n✅ استخدام تجاري",
        "variants": [
            ("شهر واحد", "42,000 ج.س"),
            ("3 شهور",   "110,000 ج.س"),
            ("6 شهور",   "195,000 ج.س"),
            ("سنة",      "295,000 ج.س"),
        ]
    },
    "netflix": {
        "name": "🎥 نتفليكس",
        "cat": "sub",
        "desc": "كل مسلسلاتك وأفلامك المفضلة\n✅ محتوى عربي وعالمي\n✅ جودة 4K",
        "variants": [
            ("شهر - بروفايل",   "18,000 ج.س"),
            ("3 شهور - بروفايل","48,000 ج.س"),
        ]
    },
    "telegram": {
        "name": "✈️ تيليجرام بريميوم",
        "cat": "sub",
        "desc": "اشتراك Telegram Premium\n✅ رفع ملفات كبيرة\n✅ ستيكرات وإيموجي حصرية\n✅ سرعة تحميل أعلى",
        "variants": [
            ("3 شهور", "120,000 ج.س"),
            ("6 شهور", "200,000 ج.س"),
            ("سنة",    "275,000 ج.س"),
        ]
    },
    "linkedin": {
        "name": "💼 LinkedIn Premium Career",
        "cat": "sub",
        "desc": "طوّر مسيرتك المهنية\n✅ عرض من شاهد ملفك\n✅ InMail messages\n🔥 خصم 67%",
        "variants": [
            ("3 شهور", "65,000 ج.س"),
        ]
    },
    "nordvpn": {
        "name": "🔒 NordVPN",
        "cat": "sub",
        "desc": "اشتراك NordVPN الأكثر أماناً\n✅ تصفح آمن ومشفر\n✅ سرعة عالية\n🔥 خصم 34%",
        "variants": [
            ("سنة - جهاز واحد", "99,000 ج.س"),
        ]
    },

    # ── ذكاء اصطناعي ────────────────────────────
    "chatgpt": {
        "name": "🤖 ChatGPT Business",
        "cat": "ai",
        "desc": "اشتراك ChatGPT Business\n✅ GPT-4 بدون حدود\n✅ استخدام تجاري",
        "variants": [
            ("شهر واحد", "35,000 ج.س"),
        ]
    },
    "perplexity": {
        "name": "🔍 Perplexity Pro",
        "cat": "ai",
        "desc": "اشتراك Perplexity Pro حساب جاهز\n✅ بحث ذكي متقدم\n✅ إجابات دقيقة مع مصادر",
        "variants": [
            ("سنة", "120,000 ج.س"),
        ]
    },

    # ── باكجات الإبداع ──────────────────────────
    "ai_lab": {
        "name": "🧪 باكج AI Creative Lab",
        "cat": "creative",
        "desc": "باكج متكامل للمبدعين\n✅ أدوبي + كانفا + كاب كت\n✅ أدوات ذكاء اصطناعي\n✅ وفر أكثر من 50%",
        "variants": [
            ("AI Creative Lab", "470,000 ج.س"),
        ]
    },
    "elite": {
        "name": "👑 باكج Elite Digital Creator",
        "cat": "creative",
        "desc": "باكج المبدع الرقمي المتقدم\n✅ كل أدوات الإبداع\n✅ ذكاء اصطناعي\n✅ سوشال ميديا",
        "variants": [
            ("Elite Digital Creator", "799,000 ج.س"),
        ]
    },
    "empire": {
        "name": "🏆 باكج Creative Empire Ultimate",
        "cat": "creative",
        "desc": "الباكج الأقوى على الإطلاق\n✅ كل شيء في باكج واحد\n✅ للشركات والمحترفين",
        "variants": [
            ("Creative Empire Ultimate", "1,200,000 ج.س"),
        ]
    },

    # ── برامج تعليمية ───────────────────────────
    "coursera": {
        "name": "🎓 كورسيرا بلاس",
        "cat": "edu",
        "desc": "طوّر مستقبلك مع Coursera Plus\n✅ شهادات معترف بها دولياً\n✅ آلاف الكورسات",
        "variants": [
            ("6 شهور", "99,000 ج.س"),
            ("سنة",    "165,000 ج.س"),
        ]
    },
    "duolingo": {
        "name": "🦜 سوبر دولينجو",
        "cat": "edu",
        "desc": "تعلم اللغات بطريقة ممتعة\n✅ بدون إعلانات\n✅ ميزات حصرية",
        "variants": [
            ("سنة - ترقية حسابك",     "149,000 ج.س"),
            ("سنة - إضافة لعائلة",    "249,000 ج.س"),
        ]
    },

    # ── ألعاب ────────────────────────────────────
    "pubg": {
        "name": "🔫 شحن PUBG Mobile",
        "cat": "games",
        "desc": "شحن فوري لـ PUBG Mobile\n✅ آمن، سريع، ومضمون 100%",
        "variants": [
            ("60 UC",   "5,000 ج.س"),
            ("325 UC",  "20,000 ج.س"),
            ("660 UC",  "38,000 ج.س"),
            ("1800 UC", "95,000 ج.س"),
        ]
    },
    "fifa": {
        "name": "⚽ فيفا 26 للسوني 5",
        "cat": "games",
        "desc": "EA Sports FC 26 - PS5\n✅ النسخة التامة\n✅ تفعيل فوري",
        "variants": [
            ("فيفا 26 للسوني 5 التمت", "189,000 ج.س"),
        ]
    },
    "cod": {
        "name": "🎯 كول أوف ديوتي بلاك أوبس 3",
        "cat": "games",
        "desc": "Call of Duty Black Ops 3 - PC\n✅ تفعيل فوري",
        "variants": [
            ("Black Ops 3 PC", "75,000 ج.س"),
        ]
    },

    # ── كمبيوتر ──────────────────────────────────
    "windows": {
        "name": "💻 ويندوز 10/11 برو",
        "cat": "computer",
        "desc": "مفتاح تفعيل Windows أصلي\n✅ تفعيل مدى الحياة\n✅ مضمون 100%",
        "variants": [
            ("ويندوز 10 برو", "25,000 ج.س"),
            ("ويندوز 11 برو", "36,000 ج.س"),
        ]
    },

    # ── سوشال ميديا ─────────────────────────────
    "tiktok": {
        "name": "🎵 تيك توك - متابعين",
        "cat": "social",
        "desc": "زيادة متابعين تيك توك\n✅ متابعين حقيقيين\n✅ تسليم سريع",
        "variants": [
            ("1000 متابع",  "15,000 ج.س"),
            ("5000 متابع",  "60,000 ج.س"),
            ("10000 متابع", "100,000 ج.س"),
        ]
    },
    "instagram": {
        "name": "📸 انستجرام - متابعين",
        "cat": "social",
        "desc": "زيادة متابعين انستجرام\n✅ متابعين حقيقيين\n✅ تسليم سريع",
        "variants": [
            ("1000 متابع",  "12,000 ج.س"),
            ("5000 متابع",  "50,000 ج.س"),
            ("10000 متابع", "90,000 ج.س"),
        ]
    },
}

# =============================================
#   قاعدة البيانات JSON
# =============================================
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
                f"bot: update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("✅ DB saved")
    except Exception as e:
        print(f"⚠️ Git: {e}")

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

def save_order(user, product_name, variant):
    db = load_db()
    db.setdefault("orders", []).append({
        "id":       len(db["orders"]) + 1,
        "user_id":  user.id,
        "name":     f"{user.first_name or ''} {user.last_name or ''}".strip(),
        "username": user.username or "",
        "product":  product_name,
        "variant":  variant,
        "time":     datetime.now().isoformat(),
        "status":   "pending",
    })
    save_db(db)

def get_stats():
    db = load_db()
    return {
        "users":  len(db["users"]),
        "orders": len(db.get("orders", [])),
        "pending": sum(1 for o in db.get("orders", []) if o.get("status") == "pending"),
    }

# =============================================
#   لوحات المفاتيح
# =============================================

# ─ القائمة الرئيسية (أزرار كبيرة) ─────────────
def kb_main(is_admin=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🛒 المتجر"),
        KeyboardButton("🔥 العروض"),
        KeyboardButton("📦 طلباتي"),
        KeyboardButton("📞 تواصل معنا"),
        KeyboardButton("ℹ️ عن المتجر"),
        KeyboardButton("⭐ اشتراكاتي"),
    )
    if is_admin:
        kb.add(
            KeyboardButton("📊 الإحصائيات"),
            KeyboardButton("📢 رسالة جماعية"),
        )
    return kb

# ─ تصنيفات المتجر (Inline) ─────────────────────
def kb_categories():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(CATEGORIES[k], callback_data=f"cat_{k}")
        for k in CATEGORIES
    ]
    kb.add(*buttons)
    return kb

# ─ منتجات تصنيف معين (Inline) ──────────────────
def kb_products(cat_key):
    kb = InlineKeyboardMarkup(row_width=1)
    for pid, p in PRODUCTS.items():
        if p["cat"] == cat_key:
            kb.add(InlineKeyboardButton(p["name"], callback_data=f"prod_{pid}"))
    kb.add(InlineKeyboardButton("🔙 رجوع للتصنيفات", callback_data="back_cats"))
    return kb

# ─ باقات منتج معين (Inline) ────────────────────
def kb_variants(pid):
    p  = PRODUCTS[pid]
    kb = InlineKeyboardMarkup(row_width=1)
    for i, (vname, vprice) in enumerate(p["variants"]):
        kb.add(InlineKeyboardButton(
            f"✅ {vname}  —  {vprice}",
            callback_data=f"order_{pid}_{i}"
        ))
    kb.add(InlineKeyboardButton(
        "🔙 رجوع للمنتجات",
        callback_data=f"cat_{p['cat']}"
    ))
    return kb

# ─ تأكيد الطلب (Inline) ────────────────────────
def kb_confirm(pid, vi):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("✅ تأكيد الطلب", callback_data=f"confirm_{pid}_{vi}"),
        InlineKeyboardButton("❌ إلغاء",        callback_data=f"prod_{pid}"),
    )
    return kb

# ─ واتساب (Inline) ─────────────────────────────
def kb_whatsapp(msg=""):
    kb = InlineKeyboardMarkup()
    url = f"https://wa.me/{WHATSAPP.replace('+','')}"
    if msg:
        url += f"?text={msg}"
    kb.add(InlineKeyboardButton("💬 تواصل واتساب", url=url))
    return kb

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
    is_adm = user.id == ADMIN_ID

    bot.send_message(
        message.chat.id,
        f"👋 أهلاً *{name}*!\n\n"
        f"🏪 مرحباً بك في *متجر EsamBay*\n"
        f"كل اشتراكاتك الرقمية في مكان واحد 🚀\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"✅ تفعيل فوري وضمان كامل\n"
        f"💳 أسعار تنافسية\n"
        f"🚀 دعم سريع عبر واتساب\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"اختر من القائمة أدناه 👇",
        reply_markup=kb_main(is_adm)
    )

    if is_new and is_adm is False:
        try:
            bot.send_message(
                ADMIN_ID,
                f"🔔 *مستخدم جديد!*\n"
                f"👤 {user.first_name} {user.last_name or ''}\n"
                f"🆔 `{user.id}`\n"
                f"📛 @{user.username or 'بدون'}\n"
                f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
        except:
            pass

# ── 🛒 المتجر ─────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def btn_store(message):
    bot.send_message(
        message.chat.id,
        "🛒 *متجر EsamBay*\n\nاختر التصنيف 👇",
        reply_markup=kb_categories()
    )

# ── 🔥 العروض ────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🔥 العروض")
def btn_offers(message):
    text = (
        "🔥 *العروض الحصرية*\n\n"
        "━━━━━━━━━━━━━━━\n"
        "💼 *LinkedIn Premium Career*\n"
        "~~199,000~~ ← *65,000 ج.س* 🔥 خصم 67%\n\n"
        "🔒 *NordVPN*\n"
        "~~150,000~~ ← *99,000 ج.س* 🔥 خصم 34%\n\n"
        "🎨 *أدوبي كريتف كلاود*\n"
        "شهر واحد: *99,000 ج.س*\n\n"
        "✈️ *تيليجرام بريميوم*\n"
        "3 شهور: *120,000 ج.س*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "للطلب اضغط على *المتجر* 👇"
    )
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🛒 اذهب للمتجر", callback_data="back_cats"))
    bot.send_message(message.chat.id, text, reply_markup=kb)

# ── 📦 طلباتي ─────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📦 طلباتي")
def btn_myorders(message):
    db  = load_db()
    uid = str(message.from_user.id)
    orders = [o for o in db.get("orders", []) if str(o.get("user_id")) == uid]
    if not orders:
        bot.send_message(message.chat.id,
            "📦 *طلباتي*\n\nليس لديك أي طلبات حتى الآن.\n\n🛒 تفضل بزيارة المتجر!")
        return
    text = "📦 *طلباتي:*\n\n"
    for o in reversed(orders[-5:]):
        status = {"pending": "🟡 معلق", "done": "✅ مكتمل"}.get(o.get("status"), "⚪")
        text += (
            f"━━━━━━━━━━━━\n"
            f"🔢 طلب #{o['id']}\n"
            f"📦 {o['product']}\n"
            f"📌 {o['variant']}\n"
            f"📊 {status}\n"
            f"📅 {o['time'][:16]}\n"
        )
    bot.send_message(message.chat.id, text)

# ── 📞 تواصل معنا ─────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📞 تواصل معنا")
def btn_contact(message):
    text = (
        "📞 *تواصل معنا*\n\n"
        "━━━━━━━━━━━━━━━\n"
        f"📱 *واتساب:* {WHATSAPP}\n\n"
        "🕐 *أوقات العمل:*\n"
        "يومياً من 9 صباحاً حتى 11 مساءً\n\n"
        "⚡ نرد على استفساراتكم في أسرع وقت!\n"
        "━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, text, reply_markup=kb_whatsapp())

# ── ℹ️ عن المتجر ──────────────────────────────
@bot.message_handler(func=lambda m: m.text == "ℹ️ عن المتجر")
def btn_about(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ *عن متجر EsamBay*\n\n"
        "منصتك الرقمية المتخصصة في تفعيل الاشتراكات والمنتجات الرقمية.\n\n"
        "━━━━━━━━━━━━━━━\n"
        "✅ *لماذا تختارنا؟*\n"
        "• تفعيل فوري خلال دقائق\n"
        "• اشتراكات أصلية ومضمونة 100%\n"
        "• دعم سريع عبر واتساب\n"
        "• أسعار تنافسية\n"
        "━━━━━━━━━━━━━━━\n\n"
        "💡 _EsamBay… لأنك تستحق خدمة تليق بيك!_"
    )

# ── ⭐ اشتراكاتي ──────────────────────────────
@bot.message_handler(func=lambda m: m.text == "⭐ اشتراكاتي")
def btn_mysubs(message):
    bot.send_message(
        message.chat.id,
        "⭐ *اشتراكاتي*\n\n"
        "للاستفسار عن اشتراكاتك الحالية\nتواصل معنا عبر واتساب 👇",
        reply_markup=kb_whatsapp(f"مرحباً، أريد الاستفسار عن اشتراكاتي. ID: {message.from_user.id}")
    )

# ── 📊 الإحصائيات (أدمن) ─────────────────────
@bot.message_handler(func=lambda m: m.text == "📊 الإحصائيات")
def btn_stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    s = get_stats()
    bot.send_message(
        message.chat.id,
        f"📊 *إحصائيات المتجر*\n\n"
        f"👥 المستخدمون: `{s['users']}`\n"
        f"🛒 إجمالي الطلبات: `{s['orders']}`\n"
        f"🟡 طلبات معلقة: `{s['pending']}`\n"
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

# ── 📢 رسالة جماعية (أدمن) ───────────────────
@bot.message_handler(func=lambda m: m.text == "📢 رسالة جماعية")
def btn_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    waiting_broadcast.add(message.from_user.id)
    bot.send_message(message.chat.id,
        "📢 أرسل الرسالة التي تريد إذاعتها لجميع المستخدمين:")

@bot.message_handler(func=lambda m: m.from_user.id in waiting_broadcast)
def handle_broadcast(message):
    waiting_broadcast.discard(message.from_user.id)
    db    = load_db()
    count = 0
    for u in db["users"].values():
        try:
            bot.send_message(u["id"],
                f"📢 *رسالة من متجر EsamBay:*\n\n{message.text}")
            count += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ تم الإرسال لـ {count} مستخدم.")

# =============================================
#   Callback Queries (الأزرار الداخلية)
# =============================================
@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call):
    cid  = call.message.chat.id
    mid  = call.message.message_id
    data = call.data
    bot.answer_callback_query(call.id)

    # ─ رجوع للتصنيفات ─
    if data == "back_cats":
        bot.edit_message_text(
            "🛒 *متجر EsamBay*\n\nاختر التصنيف 👇",
            cid, mid, parse_mode="Markdown",
            reply_markup=kb_categories()
        )

    # ─ اختيار تصنيف ─
    elif data.startswith("cat_"):
        cat_key = data[4:]
        cat_name = CATEGORIES.get(cat_key, "المنتجات")
        bot.edit_message_text(
            f"{cat_name}\n\nاختر المنتج 👇",
            cid, mid, parse_mode="Markdown",
            reply_markup=kb_products(cat_key)
        )

    # ─ اختيار منتج ─
    elif data.startswith("prod_"):
        pid = data[5:]
        p   = PRODUCTS.get(pid)
        if not p:
            return
        text = (
            f"{p['name']}\n\n"
            f"📝 *التفاصيل:*\n{p['desc']}\n\n"
            f"💰 *الباقات المتاحة:*\n"
        )
        for vname, vprice in p["variants"]:
            text += f"• {vname}: {vprice}\n"
        text += "\n👇 اختر الباقة:"
        bot.edit_message_text(
            text, cid, mid, parse_mode="Markdown",
            reply_markup=kb_variants(pid)
        )

    # ─ اختيار باقة → تأكيد ─
    elif data.startswith("order_"):
        _, pid, vi = data.split("_", 2)
        vi = int(vi)
        p  = PRODUCTS.get(pid)
        if not p:
            return
        vname, vprice = p["variants"][vi]
        text = (
            f"🛒 *تأكيد الطلب*\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📦 المنتج: {p['name']}\n"
            f"📌 الباقة: {vname}\n"
            f"💰 السعر: {vprice}\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"هل تريد تأكيد الطلب؟"
        )
        bot.edit_message_text(
            text, cid, mid, parse_mode="Markdown",
            reply_markup=kb_confirm(pid, vi)
        )

    # ─ تأكيد الطلب النهائي ─
    elif data.startswith("confirm_"):
        _, pid, vi = data.split("_", 2)
        vi  = int(vi)
        p   = PRODUCTS.get(pid)
        if not p:
            return
        vname, vprice = p["variants"][vi]
        user = call.from_user
        save_order(user, p["name"], vname)

        wa_msg = f"مرحباً، أريد طلب: {p['name']} - {vname} - {vprice}"

        bot.edit_message_text(
            f"✅ *تم استلام طلبك!*\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📦 {p['name']}\n"
            f"📌 {vname}\n"
            f"💰 {vprice}\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"سيتواصل معك فريقنا خلال دقائق ✨\n"
            f"أو تواصل معنا مباشرة عبر واتساب 👇",
            cid, mid, parse_mode="Markdown",
            reply_markup=kb_whatsapp(wa_msg)
        )

        # إشعار الأدمن
        try:
            bot.send_message(
                ADMIN_ID,
                f"🛒 *طلب جديد #{len(load_db().get('orders',[]))}!*\n\n"
                f"👤 {user.first_name} {user.last_name or ''}\n"
                f"🆔 `{user.id}`\n"
                f"📛 @{user.username or 'بدون'}\n"
                f"📦 {p['name']}\n"
                f"📌 {vname}\n"
                f"💰 {vprice}\n"
                f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
        except:
            pass

# ─ أي رسالة أخرى ──────────────────────────────
@bot.message_handler(func=lambda m: True)
def handle_other(message):
    bot.send_message(
        message.chat.id,
        "❓ اختر من القائمة أدناه 👇",
        reply_markup=kb_main(message.from_user.id == ADMIN_ID)
    )

# =============================================
#   تشغيل
# =============================================
if __name__ == "__main__":
    print("🤖 EsamBay Bot is running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)

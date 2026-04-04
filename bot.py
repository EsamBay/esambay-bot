import telebot
import json
import os
import subprocess
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
WHATSAPP  = "249129978663"   # بدون +
DB_FILE   = "database.json"

# ══════════════════════════════════════════════
#   منتجات المتجر (مطابقة لكروتي + تفعيلك)
# ══════════════════════════════════════════════
STORE = {

    # ─────────────────────────────────────────
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
                ("6500 جوهرة", "160,000 ج.س"),
            ]
        },
        "⚔️ Clash Royale": {
            "desc": "شحن Clash Royale\n✅ تسليم فوري\n✅ جواهر أصلية",
            "variants": [
                ("80 جوهرة",   "3,000 ج.س"),
                ("500 جوهرة",  "15,000 ج.س"),
                ("1200 جوهرة", "33,000 ج.س"),
                ("2500 جوهرة", "65,000 ج.س"),
            ]
        },
        "🌟 Brawl Stars": {
            "desc": "شحن Brawl Stars\n✅ تسليم فوري\n✅ جواهر أصلية",
            "variants": [
                ("30 جوهرة",  "5,000 ج.س"),
                ("80 جوهرة",  "12,000 ج.س"),
                ("170 جوهرة", "24,000 ج.س"),
                ("360 جوهرة", "48,000 ج.س"),
                ("950 جوهرة", "120,000 ج.س"),
            ]
        },
        "🐉 Mobile Legends": {
            "desc": "شحن Mobile Legends\n✅ تسليم فوري\n✅ ألماس أصلي",
            "variants": [
                ("86 ألماس",   "5,000 ج.س"),
                ("172 ألماس",  "9,000 ج.س"),
                ("257 ألماس",  "13,000 ج.س"),
                ("706 ألماس",  "34,000 ج.س"),
                ("2195 ألماس", "100,000 ج.س"),
            ]
        },
        "🎯 Call of Duty Mobile": {
            "desc": "شحن Call of Duty Mobile\n✅ تسليم فوري\n✅ CP أصلية",
            "variants": [
                ("80 CP",   "5,000 ج.س"),
                ("400 CP",  "22,000 ج.س"),
                ("800 CP",  "42,000 ج.س"),
                ("2000 CP", "100,000 ج.س"),
            ]
        },
        "🌍 Genshin Impact": {
            "desc": "شحن Genshin Impact\n✅ تسليم فوري\n✅ Genesis Crystals",
            "variants": [
                ("60 Crystals",   "3,000 ج.س"),
                ("300 Crystals",  "14,000 ج.س"),
                ("980 Crystals",  "42,000 ج.س"),
                ("1980 Crystals", "82,000 ج.س"),
                ("3280 Crystals", "130,000 ج.س"),
            ]
        },
        "🎱 8 Ball Pool": {
            "desc": "شحن 8 Ball Pool\n✅ تسليم فوري\n✅ عملات أصلية",
            "variants": [
                ("200M عملة",   "8,000 ج.س"),
                ("500M عملة",   "18,000 ج.س"),
                ("1B عملة",     "33,000 ج.س"),
                ("2B عملة",     "60,000 ج.س"),
            ]
        },
        "🩸 Blood Strike": {
            "desc": "شحن Blood Strike\n✅ تسليم فوري\n✅ BC أصلية",
            "variants": [
                ("100 BC",  "4,000 ج.س"),
                ("300 BC",  "11,000 ج.س"),
                ("600 BC",  "21,000 ج.س"),
                ("1500 BC", "50,000 ج.س"),
            ]
        },
        "🌾 Hay Day": {
            "desc": "شحن Hay Day\n✅ تسليم فوري\n✅ ألماس أصلي",
            "variants": [
                ("80 ألماس",   "5,000 ج.س"),
                ("200 ألماس",  "11,000 ج.س"),
                ("450 ألماس",  "23,000 ج.س"),
                ("1000 ألماس", "48,000 ج.س"),
            ]
        },
    },

    # ─────────────────────────────────────────
    "🃏 بطاقات الألعاب": {
        "🎮 بطاقات FreeFire": {
            "desc": "بطاقات FreeFire رقمية\n✅ كود فوري بعد الطلب\n✅ شحن جواهر بأمان",
            "variants": [
                ("100 جوهرة",  "4,000 ج.س"),
                ("310 جوهرة",  "10,000 ج.س"),
                ("1060 جوهرة", "30,000 ج.س"),
                ("2180 جوهرة", "58,000 ج.س"),
            ]
        },
        "🔫 بطاقات PUBG Mobile": {
            "desc": "بطاقات PUBG Mobile\n✅ كود فوري بعد الطلب\n✅ شحن شدات بأمان",
            "variants": [
                ("60 UC",   "6,000 ج.س"),
                ("325 UC",  "22,000 ج.س"),
                ("660 UC",  "42,000 ج.س"),
                ("1800 UC", "100,000 ج.س"),
            ]
        },
        "🎵 بطاقات Razer Gold": {
            "desc": "بطاقات Razer Gold\n✅ مقبولة في آلاف الألعاب\n✅ كود فوري",
            "variants": [
                ("5$",  "15,000 ج.س"),
                ("10$", "28,000 ج.س"),
                ("20$", "54,000 ج.س"),
                ("50$", "130,000 ج.س"),
            ]
        },
        "🍎 بطاقات iTunes": {
            "desc": "بطاقات iTunes / App Store\n✅ كود فوري بعد الطلب\n✅ للـ iPhone والـ iPad",
            "variants": [
                ("7$",   "21,000 ج.س"),
                ("15$",  "43,000 ج.س"),
                ("25$",  "70,000 ج.س"),
                ("50$",  "135,000 ج.س"),
                ("100$", "265,000 ج.س"),
            ]
        },
        "🎮 بطاقات PlayStation": {
            "desc": "بطاقات PlayStation Network\n✅ كود فوري بعد الطلب\n✅ لـ PS4 و PS5",
            "variants": [
                ("10$", "30,000 ج.س"),
                ("20$", "57,000 ج.س"),
                ("50$", "135,000 ج.س"),
                ("100$","265,000 ج.س"),
            ]
        },
        "🎲 بطاقات Yalla Ludo": {
            "desc": "بطاقات Yalla Ludo\n✅ كود فوري بعد الطلب\n✅ شحن الذهب",
            "variants": [
                ("2$",   "6,000 ج.س"),
                ("10$",  "28,000 ج.س"),
                ("50$",  "130,000 ج.س"),
                ("100$", "255,000 ج.س"),
            ]
        },
        "🟥 بطاقات Roblox": {
            "desc": "بطاقات Roblox\n✅ كود فوري بعد الطلب\n✅ Robux أصلية",
            "variants": [
                ("400 Robux",  "12,000 ج.س"),
                ("800 Robux",  "22,000 ج.س"),
                ("1700 Robux", "43,000 ج.س"),
                ("4500 Robux", "110,000 ج.س"),
            ]
        },
        "⚡ بطاقات Fortnite": {
            "desc": "بطاقات Fortnite V-Bucks\n✅ كود فوري بعد الطلب\n✅ V-Bucks أصلية",
            "variants": [
                ("1000 V-Bucks",  "28,000 ج.س"),
                ("2800 V-Bucks",  "70,000 ج.س"),
                ("5000 V-Bucks",  "120,000 ج.س"),
                ("13500 V-Bucks", "280,000 ج.س"),
            ]
        },
        "💻 بطاقات Steam": {
            "desc": "بطاقات Steam\n✅ كود فوري بعد الطلب\n✅ لشراء الألعاب على Steam",
            "variants": [
                ("5$",  "15,000 ج.س"),
                ("10$", "28,000 ج.س"),
                ("20$", "54,000 ج.س"),
                ("50$", "130,000 ج.س"),
                ("100$","255,000 ج.س"),
            ]
        },
        "🟢 بطاقات Xbox": {
            "desc": "بطاقات Xbox Gift Card\n✅ كود فوري بعد الطلب\n✅ لـ Xbox و Microsoft Store",
            "variants": [
                ("5$",  "15,000 ج.س"),
                ("10$", "28,000 ج.س"),
                ("20$", "54,000 ج.س"),
                ("50$", "130,000 ج.س"),
            ]
        },
    },

    # ─────────────────────────────────────────
    "💳 الدفع الإلكتروني": {
        "🛰️ اشتراك Starlink": {
            "desc": "تجديد اشتراك Starlink بالسودان\n✅ تجديد فوري وبأرخص الأسعار\n✅ أرسل بيانات حسابك",
            "variants": [
                ("شهر - Residential",  "45,000 ج.س"),
                ("شهر - Roam",         "130,000 ج.س"),
                ("شهر - Business",     "200,000 ج.س"),
            ]
        },
        "🧾 تسديد فاتورة": {
            "desc": "تسديد أي فاتورة إلكترونية\n✅ Visa / Mastercard / PayPal\n✅ أي موقع في العالم",
            "variants": [
                ("حتى 10$",  "30,000 ج.س"),
                ("حتى 25$",  "70,000 ج.س"),
                ("حتى 50$",  "135,000 ج.س"),
                ("حتى 100$", "265,000 ج.س"),
            ]
        },
        "🎵 شحن عملات TikTok": {
            "desc": "شحن عملات TikTok Live\n✅ إرسال هدايا للبث المباشر\n✅ بأقل الأسعار",
            "variants": [
                ("70 عملة",    "5,000 ج.س"),
                ("350 عملة",   "22,000 ج.س"),
                ("700 عملة",   "42,000 ج.س"),
                ("1400 عملة",  "82,000 ج.س"),
                ("7000 عملة",  "400,000 ج.س"),
            ]
        },
        "🔥 شحن FreeFire بالحساب": {
            "desc": "شحن فري فاير بتسجيل الدخول\n✅ كميات أكبر وأسعار أفضل\n✅ آمن ومضمون",
            "variants": [
                ("100 جوهرة",  "2,500 ج.س"),
                ("310 جوهرة",  "7,000 ج.س"),
                ("520 جوهرة",  "11,000 ج.س"),
                ("1060 جوهرة", "22,000 ج.س"),
            ]
        },
    },

    # ─────────────────────────────────────────
    "📲 سوشال ميديا": {
        "🎵 تزويد TikTok": {
            "desc": "زيادة TikTok\n✅ متابعين / لايكات / مشاهدات\n✅ تسليم سريع وآمن",
            "variants": [
                ("1000 متابع",    "8,000 ج.س"),
                ("5000 متابع",    "35,000 ج.س"),
                ("10000 متابع",   "65,000 ج.س"),
                ("1000 لايك",     "3,000 ج.س"),
                ("10000 مشاهدة",  "2,000 ج.س"),
            ]
        },
        "📘 تزويد Facebook": {
            "desc": "زيادة Facebook\n✅ متابعين / لايكات صفحة\n✅ تسليم سريع",
            "variants": [
                ("1000 متابع",  "8,000 ج.س"),
                ("5000 متابع",  "35,000 ج.س"),
                ("10000 متابع", "65,000 ج.س"),
                ("1000 لايك",   "6,000 ج.س"),
            ]
        },
        "📸 تزويد Instagram": {
            "desc": "زيادة Instagram\n✅ متابعين / لايكات\n✅ تسليم سريع",
            "variants": [
                ("1000 متابع",  "7,000 ج.س"),
                ("5000 متابع",  "30,000 ج.س"),
                ("10000 متابع", "55,000 ج.س"),
                ("1000 لايك",   "3,000 ج.س"),
            ]
        },
        "💬 تزويد WhatsApp": {
            "desc": "خدمات WhatsApp\n✅ أعضاء قناة / مشاهدات\n✅ تسليم سريع",
            "variants": [
                ("1000 عضو قناة",    "10,000 ج.س"),
                ("5000 عضو قناة",    "45,000 ج.س"),
                ("1000 مشاهدة ستوري","2,000 ج.س"),
            ]
        },
        "▶️ تزويد YouTube": {
            "desc": "زيادة YouTube\n✅ مشتركين / مشاهدات\n✅ تسليم سريع",
            "variants": [
                ("1000 مشترك",    "20,000 ج.س"),
                ("5000 مشترك",    "90,000 ج.س"),
                ("10000 مشاهدة",  "5,000 ج.س"),
                ("100000 مشاهدة", "40,000 ج.س"),
            ]
        },
        "✈️ تزويد Telegram": {
            "desc": "زيادة Telegram\n✅ أعضاء قناة / مجموعة\n✅ تسليم سريع",
            "variants": [
                ("1000 عضو",  "12,000 ج.س"),
                ("5000 عضو",  "55,000 ج.س"),
                ("10000 عضو", "100,000 ج.س"),
            ]
        },
        "🐦 تزويد Twitter/X": {
            "desc": "زيادة Twitter/X\n✅ متابعين / لايكات\n✅ تسليم سريع",
            "variants": [
                ("1000 متابع",  "10,000 ج.س"),
                ("5000 متابع",  "45,000 ج.س"),
                ("10000 متابع", "85,000 ج.س"),
            ]
        },
        "👻 تزويد Snapchat": {
            "desc": "زيادة Snapchat\n✅ متابعين / مشاهدات\n✅ تسليم سريع",
            "variants": [
                ("500 متابع",  "18,000 ج.س"),
                ("1000 متابع", "33,000 ج.س"),
                ("5000 متابع", "150,000 ج.س"),
            ]
        },
        "🧵 تزويد Threads": {
            "desc": "زيادة Threads\n✅ متابعين / لايكات\n✅ تسليم سريع",
            "variants": [
                ("1000 متابع",  "8,000 ج.س"),
                ("5000 متابع",  "35,000 ج.س"),
                ("10000 متابع", "65,000 ج.س"),
            ]
        },
    },

    # ─────────────────────────────────────────
    "📱 الاشتراكات": {
        "🎨 أدوبي كريتف كلاود": {
            "desc": "Adobe Creative Cloud\n✅ فوتوشوب، بريمير، إليستريتور\n✅ تفعيل فوري وضمان كامل",
            "variants": [
                ("شهر واحد", "99,000 ج.س"),
                ("3 شهور",   "199,000 ج.س"),
            ]
        },
        "✏️ كانفا برو": {
            "desc": "Canva Pro\n✅ آلاف القوالب الاحترافية\n✅ تفعيل فوري",
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
        "🖼️ فريبيك بريميوم": {
            "desc": "Freepik Premium\n✅ ملايين الصور والمتجهات\n✅ استخدام تجاري",
            "variants": [
                ("شهر واحد", "42,000 ج.س"),
                ("3 شهور",   "110,000 ج.س"),
                ("سنة",      "295,000 ج.س"),
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
            "desc": "ChatGPT Business\n✅ GPT-4 بدون حدود\n✅ استخدام تجاري",
            "variants": [
                ("شهر واحد", "35,000 ج.س"),
            ]
        },
        "💼 LinkedIn Premium": {
            "desc": "LinkedIn Premium Career\n✅ عرض من شاهد ملفك\n🔥 خصم 67%",
            "variants": [
                ("3 شهور", "65,000 ج.س"),
            ]
        },
        "🔒 NordVPN": {
            "desc": "NordVPN\n✅ تصفح آمن ومشفر\n🔥 خصم 34%",
            "variants": [
                ("سنة", "99,000 ج.س"),
            ]
        },
        "🎓 كورسيرا بلاس": {
            "desc": "Coursera Plus\n✅ شهادات معترف بها دولياً\n✅ آلاف الكورسات",
            "variants": [
                ("6 شهور", "99,000 ج.س"),
                ("سنة",    "165,000 ج.س"),
            ]
        },
        "🦜 سوبر دولينجو": {
            "desc": "Duolingo Super\n✅ تعلم اللغات بدون إعلانات\n✅ ميزات حصرية",
            "variants": [
                ("سنة - حساب خاص", "149,000 ج.س"),
                ("سنة - عائلة",    "249,000 ج.س"),
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
    order_id = len(db.get("orders", [])) + 1
    db.setdefault("orders", []).append({
        "id":       order_id,
        "user_id":  user.id,
        "name":     f"{user.first_name or ''} {user.last_name or ''}".strip(),
        "username": user.username or "",
        "category": cat,
        "product":  product,
        "variant":  variant,
        "price":    price,
        "status":   "pending",
        "time":     datetime.now().isoformat(),
    })
    save_db(db)
    return order_id

def get_stats():
    db = load_db()
    return {
        "users":   len(db["users"]),
        "orders":  len(db.get("orders", [])),
        "pending": sum(1 for o in db.get("orders", []) if o.get("status") == "pending"),
        "done":    sum(1 for o in db.get("orders", []) if o.get("status") == "done"),
    }

# ══════════════════════════════════════════════
#   لوحات المفاتيح
# ══════════════════════════════════════════════

def kb_main(is_admin=False):
    """القائمة الرئيسية - أزرار كبيرة أسفل الشاشة"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🛒 المتجر"),
        KeyboardButton("📦 طلباتي"),
        KeyboardButton("📞 تواصل معنا"),
        KeyboardButton("ℹ️ عن المتجر"),
    )
    if is_admin:
        kb.add(
            KeyboardButton("📊 الإحصائيات"),
            KeyboardButton("📢 رسالة جماعية"),
        )
    return kb

def kb_categories():
    """تصنيفات المتجر"""
    kb = InlineKeyboardMarkup(row_width=1)
    for cat in STORE:
        kb.add(InlineKeyboardButton(cat, callback_data=f"CAT|{cat}"))
    return kb

def kb_products(cat):
    """منتجات تصنيف معين"""
    kb = InlineKeyboardMarkup(row_width=1)
    for prod in STORE[cat]:
        kb.add(InlineKeyboardButton(prod, callback_data=f"PROD|{cat}|{prod}"))
    kb.add(InlineKeyboardButton("🔙 رجوع للتصنيفات", callback_data="BACK_CATS"))
    return kb

def kb_variants(cat, prod):
    """باقات منتج معين"""
    kb = InlineKeyboardMarkup(row_width=1)
    variants = STORE[cat][prod]["variants"]
    for i, (vname, vprice) in enumerate(variants):
        kb.add(InlineKeyboardButton(
            f"✅  {vname}  ←  {vprice}",
            callback_data=f"VAR|{cat}|{prod}|{i}"
        ))
    kb.add(InlineKeyboardButton("🔙 رجوع للمنتجات", callback_data=f"CAT|{cat}"))
    return kb

def kb_confirm(cat, prod, vi):
    """تأكيد الطلب"""
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ تأكيد الطلب", callback_data=f"CONFIRM|{cat}|{prod}|{vi}"),
        InlineKeyboardButton("❌ إلغاء",        callback_data=f"PROD|{cat}|{prod}"),
    )
    return kb

def kb_whatsapp(msg=""):
    kb = InlineKeyboardMarkup()
    url = f"https://wa.me/{WHATSAPP}"
    if msg:
        import urllib.parse
        url += "?text=" + urllib.parse.quote(msg)
    kb.add(InlineKeyboardButton("💬 تواصل واتساب", url=url))
    return kb

def kb_after_order(cat, prod, vi):
    """أزرار بعد الطلب"""
    kb = InlineKeyboardMarkup(row_width=1)
    prod_data = STORE[cat][prod]
    vname, vprice = prod_data["variants"][vi]
    import urllib.parse
    msg = f"مرحباً، أريد طلب:\n📦 {prod}\n📌 {vname}\n💰 {vprice}"
    kb.add(
        InlineKeyboardButton("💬 تواصل واتساب لإتمام الطلب",
                             url=f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"),
        InlineKeyboardButton("📦 طلباتي", callback_data="MY_ORDERS"),
        InlineKeyboardButton("🛒 متابعة التسوق", callback_data="BACK_CATS"),
    )
    return kb

# ══════════════════════════════════════════════
#   البوت
# ══════════════════════════════════════════════
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
waiting_broadcast = set()

# ── /start ──────────────────────────────────
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
        except:
            pass

# ── 🛒 المتجر ───────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def btn_store(message):
    bot.send_message(
        message.chat.id,
        "🛒 *اختر التصنيف* 👇",
        reply_markup=kb_categories()
    )

# ── 📦 طلباتي ───────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📦 طلباتي")
def btn_myorders(message):
    db  = load_db()
    uid = str(message.from_user.id)
    orders = [o for o in db.get("orders", []) if str(o.get("user_id")) == uid]
    if not orders:
        bot.send_message(message.chat.id,
            "📦 *طلباتي*\n\nلا توجد طلبات بعد.\n\nاضغط 🛒 المتجر للبدء!")
        return
    text = "📦 *آخر طلباتك:*\n\n"
    for o in reversed(orders[-5:]):
        emoji = "✅" if o.get("status") == "done" else "🟡"
        text += (
            f"━━━━━━━━━━\n"
            f"🔢 طلب #{o['id']}\n"
            f"📦 {o['product']}\n"
            f"📌 {o['variant']} — {o['price']}\n"
            f"{emoji} {'مكتمل' if o.get('status')=='done' else 'معلق'}\n"
        )
    bot.send_message(message.chat.id, text)

# ── 📞 تواصل معنا ────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📞 تواصل معنا")
def btn_contact(message):
    import urllib.parse
    msg = "مرحباً، أحتاج مساعدة 👋"
    kb  = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💬 واتساب",
           url=f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"))
    bot.send_message(
        message.chat.id,
        f"📞 *تواصل معنا*\n\n"
        f"📱 واتساب: +{WHATSAPP}\n"
        f"🕐 يومياً 9ص — 11م\n\n"
        f"⚡ نرد في أسرع وقت!",
        reply_markup=kb
    )

# ── ℹ️ عن المتجر ─────────────────────────────
@bot.message_handler(func=lambda m: m.text == "ℹ️ عن المتجر")
def btn_about(message):
    bot.send_message(
        message.chat.id,
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
        "🔒 آمن ومضمون 100%\n"
        "💬 دعم عبر واتساب"
    )

# ── 📊 إحصائيات (أدمن) ──────────────────────
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
        f"🟡 معلقة: `{s['pending']}`\n"
        f"✅ مكتملة: `{s['done']}`\n"
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

# ── 📢 رسالة جماعية (أدمن) ──────────────────
@bot.message_handler(func=lambda m: m.text == "📢 رسالة جماعية")
def btn_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    waiting_broadcast.add(message.from_user.id)
    bot.send_message(message.chat.id, "📢 أرسل الرسالة الجماعية:")

@bot.message_handler(func=lambda m: m.from_user.id in waiting_broadcast)
def do_broadcast(message):
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
    bot.send_message(message.chat.id, f"✅ أُرسلت لـ {count} مستخدم.")

# ══════════════════════════════════════════════
#   Callback — منطق التنقل الكامل
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

    # ── رجوع للتصنيفات ──
    if data in ("BACK_CATS", "MY_ORDERS"):
        if data == "MY_ORDERS":
            btn_myorders(call.message)
            return
        edit("🛒 *اختر التصنيف* 👇", kb_categories())

    # ── اختيار تصنيف ──
    elif data.startswith("CAT|"):
        cat = data[4:]
        edit(f"{cat}\n\nاختر المنتج 👇", kb_products(cat))

    # ── اختيار منتج ──
    elif data.startswith("PROD|"):
        _, cat, prod = data.split("|", 2)
        p    = STORE[cat][prod]
        text = (
            f"{prod}\n\n"
            f"📝 {p['desc']}\n\n"
            f"💰 *اختر الباقة:*"
        )
        edit(text, kb_variants(cat, prod))

    # ── اختيار باقة ──
    elif data.startswith("VAR|"):
        _, cat, prod, vi = data.split("|", 3)
        vi = int(vi)
        vname, vprice = STORE[cat][prod]["variants"][vi]
        text = (
            f"🛒 *تأكيد الطلب*\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📦 {prod}\n"
            f"📌 {vname}\n"
            f"💰 {vprice}\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"هل تريد تأكيد الطلب؟"
        )
        edit(text, kb_confirm(cat, prod, vi))

    # ── تأكيد الطلب ──
    elif data.startswith("CONFIRM|"):
        _, cat, prod, vi = data.split("|", 3)
        vi    = int(vi)
        user  = call.from_user
        vname, vprice = STORE[cat][prod]["variants"][vi]
        oid   = save_order(user, cat, prod, vname, vprice)

        text = (
            f"✅ *تم استلام طلبك!*\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔢 رقم الطلب: #{oid}\n"
            f"📦 {prod}\n"
            f"📌 {vname}\n"
            f"💰 {vprice}\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"اضغط الزر أدناه للتواصل معنا\nوإتمام الدفع 👇"
        )
        edit(text, kb_after_order(cat, prod, vi))

        # إشعار الأدمن
        try:
            bot.send_message(
                ADMIN_ID,
                f"🛒 *طلب جديد #{oid}!*\n\n"
                f"👤 {user.first_name} {user.last_name or ''}\n"
                f"🆔 `{user.id}`\n"
                f"📛 @{user.username or 'بدون'}\n"
                f"━━━━━━━━━━━\n"
                f"📁 {cat}\n"
                f"📦 {prod}\n"
                f"📌 {vname}\n"
                f"💰 {vprice}\n"
                f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
        except:
            pass

# ── أي رسالة أخرى ──────────────────────────
@bot.message_handler(func=lambda m: True)
def other(message):
    bot.send_message(
        message.chat.id,
        "اضغط *🛒 المتجر* للبدء 👇",
        reply_markup=kb_main(message.from_user.id == ADMIN_ID)
    )

# ══════════════════════════════════════════════
if __name__ == "__main__":
    print("🤖 EsamBay Bot running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)

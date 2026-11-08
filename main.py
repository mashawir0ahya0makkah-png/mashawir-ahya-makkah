import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID", "")
NAME, FROM, TO, PHONE = range(4)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🚕 طلب مشوار جديد"], ["💰 الأسعار"], ["📞 تواصل معنا"]]
    await update.message.reply_text("أهلاً فيك في *مشاوير أحيا مكة* 🕋🚕\n\nنوصلك داخل مكة وخارجها، بسرعة وأمان.\n\nاختر من القائمة:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True), parse_mode="Markdown")
async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 *أسعار مشاوير أحيا مكة*\n\n• داخل أحياء مكة: حسب المسافة\n• من مكة إلى جدة: حسب الاتفاق\n• من مكة إلى المطار: حسب الاتفاق\n\nارسل /start لطلب مشوار جديد", parse_mode="Markdown")
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 *تواصل معنا*\n\nاكتب لنا طلبك هنا، ونرد عليك بأسرع وقت.\n\nلطلب مشوار ارسل /start", parse_mode="Markdown")
async def new_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تمام! 🚕\n\nايش اسمك الكريم؟")
    return NAME
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("من وين نجيك؟ ارسل اسم الحي / المكان")
    return FROM
async def get_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['from'] = update.message.text
    await update.message.reply_text("وين وجهتك؟")
    return TO
async def get_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['to'] = update.message.text
    await update.message.reply_text("ارسل رقم جوالك للتواصل")
    return PHONE
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    d = context.user_data
    msg = f"🚕 *طلب مشوار جديد*\n\n👤 الاسم: {d['name']}\n📍 من: {d['from']}\n🎯 إلى: {d['to']}\n📱 الجوال: {d['phone']}\n🆔 يوزر: @{update.message.from_user.username or 'بدون يوزر'}"
    await update.message.reply_text("تم استلام طلبك ✅\n\nبنتصل فيك بأسرع وقت لتأكيد المشوار والسعر.\n\nشكراً لاختيارك مشاوير أحيا مكة 🕋")
    if ADMIN_ID:
        try:
            await context.bot.send_message(chat_id=int(ADMIN_ID), text=msg, parse_mode="Markdown")
        except:
            pass
    return ConversationHandler.END
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء الطلب، ارسل /start للبدء من جديد")
    return ConversationHandler.END
def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(entry_points=[MessageHandler(filters.Regex("^(🚕 طلب مشوار جديد)$"), new_trip)], states={NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)], FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_from)], TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_to)], PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)]}, fallbacks=[CommandHandler("cancel", cancel)])
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^(💰 الأسعار)$"), prices))
    app.add_handler(MessageHandler(filters.Regex("^(📞 تواصل معنا)$"), contact))
    app.add_handler(conv)
    app.run_polling()
if __name__ == "__main__":
    main()

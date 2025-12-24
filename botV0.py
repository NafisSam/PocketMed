import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

load_dotenv(dotenv_path=r"C:\\Users\\Surface\\projects\\PocketMed\\.env", override=True)

print("ENV loaded:", os.path.exists(r"C:\\Users\\Surface\\projects\\PocketMed\\.env"))
print("OPENAI key exists:", bool(os.getenv("OPENAI_API_KEY")))
print("TELEGRAM token exists:", bool(os.getenv("TELEGRAM_BOT_TOKEN")))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in .env")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

system_prompt = """
You are PocketMed, a calm, concise diabetes information assistant and connected to an electronic health record.

- Your user is a person living with diabetes (mostly type 2) or at risk of diabetes, mostly old age.
- Use simple, clear language. Always answer in fluent Persian.
- Give short answers (2–4 sentences).
- Base your answers on standard diabetes education (lifestyle, monitoring, medications) but DO NOT give exact prescriptions, doses, or treatment orders.
- Always consider the patient's personal info if provided (age, diabetes type, medications, lab values, other conditions).
- If a situation sounds urgent (e.g. very high sugar with symptoms, chest pain, confusion, severe shortness of breath), tell them to seek immediate medical care.

"""

messages = [
    {"role": "system", "content": system_prompt.strip()}                     #strip: تمیز کردن متن و حذف فاصله های اول و آخر
]

def format_patient_profile (profile: dict) -> str:
    """
    این تابع یک دیکشنری پروفایل بیمار را به متن قابل فهم برای مدل تبدیل می‌کند.
    """
    parts = []
    age = profile.get ("age")
    if age is not None:
        parts.append (f"Age: {age}")
    gender = profile.get ("gender")
    if gender:
        parts.append (f"Gender: {gender}")
    dtype = profile.get ("diabetes_type")
    if dtype:
        parts.append (f"Diabetes_type: {dtype}")
    duration = profile.get ("duration_years")
    if duration is not None:
        parts.append (f"Diabetes duration (years): {duration}")
    meds = profile.get ("meds")
    if meds:
        parts.append ("Current medication: " + ", ".join (meds))
    others = profile.get ("other_conditions")
    if others:
        parts.append ("Other conditions: " + ", ".join (others))
    hba1c = profile.get ("latest_hba1c")
    if hba1c is not None:
        parts.append (f"Latest HbA1c: {hba1c}")
    if not parts:
        return "No specific patient profile was provided"
    return "Patient profile: " + " | ".join (parts)


def ask_diabetes(question: str, patient_profile: dict | None = None) -> str:
    local_messages = []

    # system prompt
    local_messages.append({
        "role": "system",
        "content": system_prompt.strip()
    })

    if patient_profile is not None:
        profile_text = format_patient_profile(patient_profile)
        local_messages.append({
            "role": "user",
            "content": profile_text
        })

    local_messages.append({
        "role": "user",
        "content": question
    })

    response = client.responses.create(
        model="gpt-4o-mini",
        input=local_messages,
        temperature=0.2,
        max_output_tokens=300
    )

    return response.output_text


async def start(update, context):
    await update.message.reply_text(
        "سلام 👋\n"
        "من دستیار دیابت PocketMed هستم.\n"
        "سوال‌های مربوط به دیابت را بپرس؛ من یک توضیح کوتاه و آموزشی می‌دهم.\n"
        "یادت باشد: من جای پزشک را نمی‌گیرم."
    )


async def handle_message(update, context):
    user_text = (update.message.text or "").strip()
    user_data = context.user_data   # حافظه مخصوص این کاربر

    # اگر هنوز پروفایل ندارد، بساز
    if "profile" not in user_data:
        user_data["profile"] = {}

    profile = user_data["profile"]

    # ---- دریافت اطلاعات ساده از کاربر ----
    if user_text.startswith("سن"):
        profile["age"] = int(user_text.replace("سن", "").strip())
        await update.message.reply_text("سن ذخیره شد.")
        return

    if user_text.startswith("جنس"):
        profile["gender"] = user_text.replace("جنس", "").strip()
        await update.message.reply_text("جنس ذخیره شد.")
        return

    if user_text.startswith("دیابت"):
        profile["diabetes_type"] = user_text.replace("دیابت", "").strip()
        await update.message.reply_text("نوع دیابت ذخیره شد.")
        return

    if user_text.startswith("دارو"):
        meds = user_text.replace("دارو", "").strip()
        profile["meds"] = [m.strip() for m in meds.split(",")]
        await update.message.reply_text("داروها ذخیره شد.")
        return

    # ---- نمایش خلاصه ----
    if user_text.lower() == "summary":
        if not profile:
            await update.message.reply_text("هنوز اطلاعاتی ثبت نشده.")
            return

        summary = format_patient_profile(profile)
        await update.message.reply_text(summary)
        return

    # ---- سؤال پزشکی ----
    answer = ask_diabetes(user_text, profile if profile else None)
    await update.message.reply_text(answer)

def main ():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler (CommandHandler("start", start))
    app.add_handler (MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("PocketMed Telegram bot is running...")
    app.run_polling ()


if __name__ == "__main__":
    main()

import os
import hashlib
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters



load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    exit(1)

def is_jpeg(file_path):
    JPEG_MAGIC_BYTES = b'\xFF\xD8\xFF'
    JPEG_APP_MARKERS = {0xE0, 0xE1, 0xE2, 0xE3, 0xE8}
    try:
        with open(file_path, 'rb') as file:
            magic_bytes = file.read(4)  # Read the first 4 bytes

            if len(magic_bytes) < 4:
                return False

            if magic_bytes[:3] != JPEG_MAGIC_BYTES:
                return False

            app_marker = magic_bytes[3]
            if app_marker in JPEG_APP_MARKERS:
                return True
            else:
                return False


    except Exception as e:
        print(f"An error occurred: {e}")
        return False


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temp_file = 'temp.img'
    try:
        photo = update.message.photo[-1]

        file = await photo.get_file()
        await file.download_to_drive(temp_file)

        if is_jpeg(temp_file):
            sha256_hash = hashlib.sha256()
            with open(temp_file, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            os.remove(temp_file)

            await update.message.reply_text(f"SHA256 Hash: {sha256_hash.hexdigest()}")
            print(f"SHA256 Hash: {sha256_hash.hexdigest()}")
        else:
            await update.message.reply_text("Error Only JPG/JPEG images are supported")
            print("Error Only JPG/JPEG images are supported")


    except Exception as e:
        print(f"error in handle_photo: {e}")
        await update.message.reply_text("An error occurred while processing the photo")

async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Error: Only JPG/JPEG images are supported.")
    print("Error: Only JPG/JPEG images are supported.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    text_handler = MessageHandler(filters.ALL & ~filters.PHOTO, handle_other)

    app.add_handler(photo_handler)
    app.add_handler(text_handler)

    print("Boti is running... :)")
    app.run_polling()

if __name__ == "__main__":
    main()

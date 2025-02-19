import requests
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from io import BytesIO

# Apply nest_asyncio for Google Colab
nest_asyncio.apply()

# Replace with your actual bot token from BotFather
TOKEN = "YOUR_BOT_TOKEN"

# TradingView Chart URL (Using BTC/USD chart)
TRADINGVIEW_IMAGE_URL = "https://s3.tradingview.com/snapshots/t/T7AnU6L1.png"

async def get_bitcoin_chart():
    """Fetches the latest Bitcoin chart from TradingView."""
    response = requests.get(TRADINGVIEW_IMAGE_URL)

    if response.status_code != 200:
        return None, "❌ Error fetching the TradingView chart. Try again later."

    image_stream = BytesIO(response.content)
    return image_stream, "📊 Live Bitcoin (BTC) Chart from TradingView"

async def chart(update: Update, context: CallbackContext) -> None:
    """Handles /chart command and sends the latest Bitcoin chart."""
    image_stream, message = await get_bitcoin_chart()

    if image_stream:
        await update.message.reply_photo(image_stream, caption=message)
    else:
        await update.message.reply_text(message)

async def run_bot():
    """Starts the bot asynchronously."""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("chart", chart))

    print("✅ Bitcoin Chart Bot is running on Google Colab...")
    await app.run_polling()

# Run the bot in Google Colab
loop = asyncio.get_event_loop()
loop.create_task(run_bot())

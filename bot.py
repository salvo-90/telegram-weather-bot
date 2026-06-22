import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("8838030262:AAEPqjwPu9UuLUaatBh9r8rH8Tn5AY2HEeY")

# === coordinate città ===
def get_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}
    response = requests.get(url, params=params)
    data = response.json()
    
    if "results" not in data:
        return None, None
    
    return data["results"][0]["latitude"], data["results"][0]["longitude"]

# === meteo ===
def get_weather(city):
    lat, lon = get_coordinates(city)
    
    if lat is None:
        return "Città non trovata 😢"
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    temp = data["current_weather"]["temperature"]
    return f"A {city} ci sono {temp}°C 🌡️"

# === bot ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Scrivi /meteo Roma")

async def meteo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Inserisci una città")
        return
    
    city = " ".join(context.args)
    result = get_weather(city)
    await update.message.reply_text(result)

# === run ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meteo", meteo))
    
    print("Bot avviato...")
    app.run_polling()

if __name__ == "__main__":
    main()

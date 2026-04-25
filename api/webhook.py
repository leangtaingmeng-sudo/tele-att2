from fastapi import FastAPI, Request
import os
from telegram import Update, Bot

app = FastAPI()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def handle_response(text: str) -> str:
    if text.lower() == 'hi':
        return "hi from da web"
    return "I didn't catch that."
@app.get("/api/webhook")
async def check_health():
    return {"status": "The bot is awake and listening!"}
@app.post("/api/webhook")
async def webhook_handler(request: Request):
    # Parse the incoming JSON from Telegram
    data = await request.json()
    
    # CRITICAL FIX: Open the bot connection ONLY when handling the request
    async with Bot(token=TOKEN) as bot:
        # Convert the JSON into a python-telegram-bot Update object
        update = Update.de_json(data, bot)
        
        # Handle the message
        if update.message and update.message.text:
            user_text = update.message.text
            chat_id = update.message.chat_id
            
            # --- YOUR AI LOGIC GOES HERE ---
            reply = handle_response(user_text)
            
            # Send the response back asynchronously 
            await bot.send_message(
                chat_id=chat_id, 
                text=f"The AI is processing: {user_text}"
            )
            
            # Send the actual generated reply
            await update.message.reply_text(reply)
            
    # Always return a 200 OK so Telegram knows the message was received
    return {"ok": True}

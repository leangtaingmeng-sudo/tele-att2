from fastapi import FastAPI, Request
import os
from telegram import Update, Bot
app = FastAPI()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TOKEN = "8609582807:AAH7Sqp3BJ4XetaoTiZVRT2ycrh9B3rzy9o"
bot = Bot(token=TOKEN)

def handle_reponse(text:str)->str:
    if text.lower() == 'hi':
        return "hi from da web"
    return "fuck u nigger"
@app.post("/api/webhook")
async def webhook_handler(request: Request):
    # Parse the incoming JSON from Telegram
    data = await request.json()
    
    # Convert the JSON into a python-telegram-bot Update object
    update = Update.de_json(data, bot)
    
    # 3. Handle the message
    if update.message and update.message.text:
        user_text = update.message.text
        chat_id = update.message.chat_id
        
        # --- YOUR AI LOGIC GOES HERE ---
        reply = handle_reponse(user_text)
        
        # Send the response back asynchronously 
        await bot.send_message(
            chat_id=chat_id, 
            text=f"The AI is processing: {user_text}"
        )
        await update.message.reply_text(reply)
        
    # Always return a 200 OK so Telegram knows the message was received
    return {"ok": True}
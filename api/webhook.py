from fastapi import FastAPI, Request
import os
from telegram import Update, Bot
from dataclasses import dataclass, field
from typing import Any
from  bot import query_huggingface
app = FastAPI()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
# agent = Agent(model="qwen2.5-coder-0.5b-instruct-f1")
ai_mode = False
def handle_response(text:str)->str:
    if text.lower() == 'hi':
        return "hi from da web"
    elif ai_mode == True:
        return query_huggingface(text)
    return "fuck u nigger"
def ai_mode_command():
    global ai_mode
    ai_mode = not ai_mode

@app.get("/api/webhook")
async def check_health():
    return {"status": "The bot is awake and listening!"}
@app.post("/api/webhook")
async def webhook_handler(request: Request):
    # Parse the incoming JSON from Telegram
    data = await request.json()
    
    # Convert the JSON into a python-telegram-bot Update object
    
    async with Bot(token=TOKEN) as bot:
    # 3. Handle the message
        update = Update.de_json(data, bot)
        if update.message and update.message.text:
            user_text = update.message.text
            chat_id = update.message.chat_id
            if user_text.startswith("/start"):
                await update.message.reply_text("Hello digger, i am a very smart telegram Bot")
            elif user_text.startswith("/help"):
                await update.message.reply_text("Bigger, I am here to help")
            elif user_text.startswith("/ai"):
                ai_mode_command()
                await update.message.reply_text("rigger, you can now chat with an ai")        
            # --- YOUR AI LOGIC GOES HERE ---
            else:
                reply = handle_response(user_text)
                await update.message.reply_text(reply)
        
    # Always return a 200 OK so Telegram knows the message was received
    return {"ok": True}

from telegram import Update, Bot
import asyncio

tokenTelegram=""
chatId=""

async def enviarMensajePrivado(mensaje):
    bot=Bot(token=tokenTelegram)

    await bot.send_message(
        chat_id=chatId,
        text=mensaje
    )
mensaje=input("Ingrese su mensaje: ")
asyncio.run(enviarMensajePrivado(mensaje))
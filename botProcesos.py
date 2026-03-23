#Importacion de dependencias
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters,ContextTypes
from multiprocessing import Process,Queue
import time

def tareaN(texto,cola):
    print("Procesando Mensaje...")
    time.sleep(5)
    resultado=f"Mensaje Procesado {texto}"
    cola.put(resultado)

#funcion de comunicacion
async def verificacion(update:Update,cola:Queue):
    while cola.empty():
        print("Sin solicitudes")
    resultado=cola.get()
    await update.message.reply_text(resultado)

async def responder(update:Update,context:ContextTypes.DEFAULT_TYPE):
    mensajeUsuario=update.message.text
    cola=Queue()
    proceso=Process(target=tareaN,args=(mensajeUsuario,cola))
    proceso.start()
    await update.message.reply_text("Procesando...")

    context.application.create_task(verificacion(update,cola))

tokenTelegram=""
app=ApplicationBuilder().token(tokenTelegram).build()
app.add_handler(MessageHandler(filters.TEXT,responder))
print("Bot Iniciado...")
app.run_polling()
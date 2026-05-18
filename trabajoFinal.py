from flask import Flask
from flask_socketio import SocketIO, send
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes
)

import threading
import asyncio
import eventlet

# CONFIGURAR TELEGRAM


tokenTelegram = ""
chatID = "TU_CHAT_ID"

# Necesario para SocketIO
eventlet.monkey_patch()

# Crear Flask
app = Flask(__name__)

# Configurar SocketIO
socket = SocketIO(
    app,
    cors_allowed_origins="*"
)

# Crear BOT Telegram
botTelegram = ApplicationBuilder().token(tokenTelegram).build()

# Crear loop global
loop_telegram = asyncio.new_event_loop()


# HTML


@app.route("/")
def index():
    return """
    <h1>Servidor Chat Activo</h1>
    """

# =========================
# SOCKET MENSAJES WEB
# =========================

@socket.on("message")
def recibirMensaje(mensaje):

    print("Mensaje WEB:", mensaje)

    # Reenviar a todos los clientes
    send(f"WEB: {mensaje}", broadcast=True)

    # Enviar a Telegram
    asyncio.run_coroutine_threadsafe(
        enviarTelegram(mensaje),
        loop_telegram
    )

# ENVIAR A TELEGRAM


async def enviarTelegram(mensaje):

    try:
        await botTelegram.bot.send_message(
            chat_id=chatID,
            text=f"WEB: {mensaje}"
        )

    except Exception as e:
        print("Error Telegram:", e)


# RECIBIR DESDE TELEGRAM


async def recibirTelegram(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    usuario = update.message.from_user.first_name
    mensaje = update.message.text

    texto = f"Telegram {usuario}: {mensaje}"

    print(texto)

    # Enviar al chat web
    socket.send(texto)

# INICIAR BOT


def iniciarBot():

    asyncio.set_event_loop(loop_telegram)

    botTelegram.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            recibirTelegram
        )
    )

    print("BOT TELEGRAM ACTIVO")

    botTelegram.run_polling()


if __name__ == "__main__":

    # Hilo del bot
    hilo = threading.Thread(target=iniciarBot)

    hilo.start()

    print("Servidor iniciado")

    socket.run(
        app,
        host="0.0.0.0",
        port=5000
    )
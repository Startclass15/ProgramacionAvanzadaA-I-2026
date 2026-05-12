from flask import Flask
from flask_socketio import SocketIO, send
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler,filters,ContextTypes
import threading
import asyncio
import eventlet

#Configurar Bot telegram
tokenTelegram=""
chatID=""


# Necesario para SocketIO
eventlet.monkey_patch()

# Crear la app
app = Flask(__name__)

#cONECTAR AL BOT
botTelegram=ApplicationBuilder().token(tokenTelegram).build()

# Configurar SocketIO
socket = SocketIO(
    app,
    cors_allowed_origins="*"
)

# Ruta principal
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chat en Tiempo Real</title>

<style>

body{
    font-family: Arial;
    background:#f2f2f2;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}

.chat-container{
    width:95%;
    max-width:450px;
    background:white;
    border-radius:10px;
    overflow:hidden;
    box-shadow:0 0 10px rgba(0,0,0,0.2);
}

.chat-header{
    background:#007bff;
    color:white;
    padding:15px;
    text-align:center;
    font-size:20px;
    font-weight:bold;
}

#chat{
    height:400px;
    overflow-y:auto;
    padding:10px;
    background:#fafafa;
}

.mensaje{
    background:#e4e6eb;
    padding:10px;
    border-radius:10px;
    margin-bottom:10px;
    word-wrap:break-word;
}

.controls{
    padding:10px;
    border-top:1px solid #ddd;
}

.input-group{
    display:flex;
    gap:10px;
    margin-bottom:10px;
}

input{
    flex:1;
    padding:10px;
    border:1px solid #ccc;
    border-radius:5px;
}

button{
    padding:10px 15px;
    border:none;
    background:#007bff;
    color:white;
    border-radius:5px;
    cursor:pointer;
}

button:hover{
    background:#0056b3;
}

#btn-entrar{
    background:#28a745;
}

#btn-entrar:hover{
    background:#1e7e34;
}

</style>

</head>
<body>

<div class="chat-container">

    <div class="chat-header">
        Chat Tiempo Real
    </div>

    <div id="chat"></div>

    <div class="controls">

        <div class="input-group">
            <input type="text" id="nombre" placeholder="Tu nombre">
            <button id="btn-entrar" onclick="guardarNombre()">
                Entrar
            </button>
        </div>

        <div class="input-group">
            <input type="text" id="mensaje" placeholder="Escribe un mensaje">
            <button onclick="enviar()">
                Enviar
            </button>
        </div>

    </div>

</div>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>

<script>

var socket = io();

var nombre = "";

function guardarNombre(){

    let input = document.getElementById("nombre");

    if(input.value.trim() == ""){
        alert("Ingrese su nombre");
        return;
    }

    nombre = input.value;

    input.disabled = true;

    document.getElementById("btn-entrar").disabled = true;

    agregarMensaje("Sistema", nombre + " se unió al chat");
}

function enviar(){

    let mensajeInput = document.getElementById("mensaje");

    let mensaje = mensajeInput.value;

    if(nombre == ""){
        alert("Debe ingresar su nombre");
        return;
    }

    if(mensaje.trim() == ""){
        return;
    }

    socket.send(nombre + ": " + mensaje);

    mensajeInput.value = "";
}

socket.on("message", function(msg){

    let chat = document.getElementById("chat");

    let div = document.createElement("div");

    div.className = "mensaje";

    if(msg.includes(":")){

        let partes = msg.split(":");

        div.innerHTML =
            "<strong>" + partes[0] + ":</strong> " +
            partes.slice(1).join(":");

    }else{
        div.innerText = msg;
    }

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;

});

function agregarMensaje(usuario, texto){

    let chat = document.getElementById("chat");

    let div = document.createElement("div");

    div.className = "mensaje";

    div.innerHTML = "<strong>" + usuario + ":</strong> " + texto;

    chat.appendChild(div);

}

</script>

</body>
</html>
"""

# Evento de mensajes
@socket.on("message")
def recibirMensaje(mensaje):

    print("Mensaje:", mensaje)

    send(f"Web:{mensaje}", broadcast=True)

    #Enviar a Telegram
    asyncio.run_coroutine_threadsafe(
        enviarTelegram(mensaje),loop_telegram)


#Funcion para enviar a telegram
async def enviarTelegram(mensaje):
    await botTelegram.bot.send_message(
        chat_id=chatID,
        text=f"WEB: {mensaje}"
    )

#Funcion para recibir de telegram
async def recibirTelegram(update:Update, context:ContextTypes.DEFAULT_TYPE):
    usuario=update.message.from_user.first_name
    mensaje=update.message.text
    texto=f"Telegram {usuario}: {mensaje}"

    #Puente de comunicacion entre telegram y servidor Web
    #socket.emit("message",texto)
    print(texto)
    socket.send(texto)

#Configurar el Bot
def iniciarBot():
    global loop_telegram

    loop_telegram=asyncio.new_event_loop
    asyncio.set_event_loop(loop_telegram)
    botTelegram.add_handler(MessageHandler(filters.TEXT,recibirTelegram))
    print("BOT TELEGRAM ACTIVO")
    botTelegram.run_polling()

# Ejecutar servidor
if __name__ == "__main__":
    hilo=threading.Thread(target=iniciarBot)
    hilo.start()

    puerto = 5000

    print("Servidor iniciado")

    socket.run(
        app,
        host="0.0.0.0",
        port=puerto
    )
from flask import Flask
from flask_socketio import SocketIO, send
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler,filters,ContextTypes
import threading
import asyncio

#Configurar Bot telegram
tokenTelegram=""
chat_id=""


# Crear la app
app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")

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
        /* Estilos generales */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .chat-container {
            width: 100%;
            max-width: 450px;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Cabecera */
        .chat-header {
            background-color: #007bff;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
        }

        /* Área de mensajes */
        #chat {
            height: 400px;
            padding: 15px;
            overflow-y: auto;
            background-color: #ffffff;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        #chat p {
            margin: 0;
            padding: 8px 12px;
            border-radius: 15px;
            background-color: #e9ecef;
            max-width: 80%;
            word-wrap: break-word;
            font-size: 0.95rem;
            line-height: 1.4;
        }

        /* Controles de entrada */
        .controls {
            padding: 15px;
            border-top: 1px solid #eee;
            background: #f9f9f9;
        }

        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }

        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            outline: none;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus {
            border-color: #007bff;
        }

        button {
            padding: 10px 15px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }

        button:hover {
            background-color: #0056b3;
        }

        button#btn-entrar {
            background-color: #28a745;
        }

        button#btn-entrar:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">Sala de Chat</div>

    <div id="chat">
        <!-- Los mensajes aparecerán aquí -->
    </div>

    <div class="controls">
        <div class="input-group">
            <input type="text" id="nombre" placeholder="Tu nombre...">
            <button id="btn-entrar" onclick="guardarNombre()">Entrar</button>
        </div>
        
        <div class="input-group">
            <input type="text" id="mensaje" placeholder="Escribe un mensaje...">
            <button onclick="enviar()">Enviar</button>
        </div>
    </div>
</div>

<!-- Librería Socket.IO -->
<script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>

<script>
    var socket = io();
    var nombre = "";

    function guardarNombre(){
        var inputNombre = document.getElementById("nombre");
        if(inputNombre.value.trim() !== ""){
            nombre = inputNombre.value;
            inputNombre.disabled = true;
            document.getElementById("btn-entrar").disabled = true;
            document.getElementById("btn-entrar").innerText = "Listo";
        }
    }

    function enviar(){
        var mensajeInput = document.getElementById("mensaje");
        var mensaje = mensajeInput.value;

        if(nombre === "" || mensaje === ""){
            alert("Debe ingresar nombre y mensaje");
            return;
        }

        socket.send(nombre + ": " + mensaje);
        mensajeInput.value = "";
    }

    socket.on("message", function(mensaje){
        var chat = document.getElementById("chat");
        var p = document.createElement("p");
        
        // Formato simple para diferenciar el nombre del mensaje
        if(mensaje.includes(":")) {
            let partes = mensaje.split(":");
            p.innerHTML = `<strong>${partes[0]}:</strong> ${partes.slice(1).join(":")}`;
        } else {
            p.textContent = mensaje;
        }

        chat.appendChild(p);
        chat.scrollTop = chat.scrollHeight;
    });
</script>

</body>
</html>
    """

# Evento de mensaje
@socket.on("message")
def conexionMensaje(mensaje):
    send(mensaje, broadcast=True)

# Ejecutar servidor
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    socket.run(app, host="0.0.0.0", port=puerto)
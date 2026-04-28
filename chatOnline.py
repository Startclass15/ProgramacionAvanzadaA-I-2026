#Importar librerias
from flask import Flask
from flask_socketio import SocketIO, send
import os
from eventlet.green.threading import Event

#Crear la instancia de flask
app=Flask(__name__)
socket=SocketIO(app, cors_allowed_origins="*")

mensajeEvento=Event()
ultimoMensaje=""

#Crear las rutas
@app.route("/")
def index():
    return """  
    <h2>Chat en tiempo real</h2>
<input type="text" id="nombre" placeholder="Ingrese su nombre">
<button onclick=guardarNombre()>Entrar</button>
<br>
<br>
<div id="chat">
</div>

<input type="text" id="mensaje" placeholder="Ingrese el mensaje">
<button onclick=enviar()>Enviar</button>

<script>
    var socket=io();
    var nombre="";

    function guardarNombre(){
        nombre=document.getElementById("nombre").value;
    }

    function eviar(){
        var mensaje=document.getElementById("mensaje").value;
        socket.send(nombre+ ": ",+mensaje);
    }
    socket.on("message",function(mensaje){
        var chat=document.getElementById("chat");
        chat.innerHTML += "<p>"+mensaje+"</p>";
    }

);
</script>

"""
@socket.on("message")
def conexionMensaje(mensaje):
    global ultimoMensaje
    ultimoMensaje=mensaje
    send(mensaje,broadcast=True)
    mensajeEvento.clear()

if __name__=="__main__":
    puerto=int(os.environ.get("puerto",5000))
    socket.run(app, host="0.0.0.0",port=puerto)
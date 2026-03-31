#Paso 1. Importar dependencias
import cv2
import os 
from multiprocessing import Process
from telegram import Update
from telegram.ext import ApplicationBuilder,MessageHandler,filters,ContextTypes
import uuid #dependencia para generar id aleatorios


tokenTelegram=""

#Paso2. Crear la funcion para procesar la Imagen
def procesarImagen(rutaEntrada,rutaSalida):
    try:
        #Paso3. Cargar un modelo de reconocimiento facial
        reconocimiento=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

        imagen=cv2.imread(rutaEntrada) #leer la imagen
        if imagen is None:
            print("Error al obtener las imagenes...")
            return False
        
        #Aplicar los filtros de escala de grises 
        grises=cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
        rostros=reconocimiento.detectMultiScale(grises,1.3,5) 

        if len(rostros) == 0:
            print("No se detectaron rostros")

        #Escalas de deteccion
        #1.1=Mas precisa pero es mas lento(puede detectar mas rostros)
        #1.3=Balanceado (puede omitir algunos rostros mas pequeños)
        #1.5=La mas rapida pero puede no detectar bien

        #Escala de Seguridad
        #3=Detecta mas pero puede brindar falsos positivos
        #5=Balanceado 
        #8= El mas estricto por la cantidad de pruebas 
        for (x,y,w,h) in rostros:
            cv2.rectangle(imagen,(x,y),(x+w,y+h),(0,255,0),2)
        
        #Paso 4. Guardar la imagen
        cv2.imwrite(rutaSalida,imagen)
        print("Imagen Procesada...")
        return True

    except Exception as error:
        print("Error al procesar la imagen...",error)
        return False

#Paso5. Funcion Obtener Imagenes desde telegram
async def obtenerImagen(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.photo:
            return 

        #obtener la imagen de telegram
        foto=update.message.photo[-1]
        archivo=await foto.get_file()

        #optimizacion de nombres archivos temporales
        nombre=str(uuid.uuid4())
        rutaEntrada=f"entrada_{nombre}.jpg"
        rutaSalida=f"salida_{nombre}.jpg"

        await archivo.download_to_drive(rutaEntrada)

        proceso=Process(target=procesarImagen,args=(rutaEntrada,rutaSalida))
        proceso.start()
        proceso.join()  # ⚠️ bloquea pero lo dejamos como pediste (no borrar)

        # Espera extra por seguridad (evita errores en disco lento)
        import time
        time.sleep(0.5)

        if os.path.exists(rutaSalida):
            with open(rutaSalida, "rb") as img:
                await update.message.reply_photo(photo=img)
        else:
            await update.message.reply_text("Error al detectar rostros")

        # 🔥 LIMPIEZA DE ARCHIVOS TEMPORALES
        if os.path.exists(rutaEntrada):
            os.remove(rutaEntrada)
        if os.path.exists(rutaSalida):
            os.remove(rutaSalida)

    except Exception as error:
        print("Error al conectar con el bot",error)
        await update.message.reply_text("Error al procesar")


#Paso 6. Funcion principal
def main():
    app=ApplicationBuilder().token(tokenTelegram).build()
    app.add_handler(MessageHandler(filters.PHOTO, obtenerImagen))
    print("Bot Funcionando")
    app.run_polling()

if __name__=="__main__":
    main()
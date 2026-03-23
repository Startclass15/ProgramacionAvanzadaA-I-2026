#Paso 1. Importacion de dependencias
from multiprocessing import Process
import os 
import numpy as np
from PIL import Image 

#Paso 2. Conectar google drive
from google.colab import drive
drive.mount('/content/drive')

rutaImagenes="/content/drive/MyDrive/dataImagenes"

def procesarImagenes(listaRutas,resultados):
  for ruta in listaRutas:
    try:
      img=Image.open(ruta)
      img=img.resize((100,100))
      imagenArray=np.array(img)
      resultados.append(imagenArray)
    except:
      pass

rutaImagenes="/content/drive/MyDrive/dataImagenes"

def procesarImagenes(listaRutas,resultados):
  for ruta in listaRutas:
    try:
      img=Image.open(ruta)
      img=img.resize((100,100))
      imagenArray=np.array(img)
      resultados.append(imagenArray)
    except:
      pass

  
#funcion para cargar las imagenes
def cargar(carpeta):
  ruta=[]
  for archivo in os.listdir(carpeta):
    ruta.append(os.path.join(carpeta,archivo))
  return ruta


if __name__=="__main__":
  carpetaPerro=os.path.join(rutaImagenes,"Perro")
  carpetaGato=os.path.join(rutaImagenes,"Gato")

  rutaPerro=cargar(carpetaPerro)
  rutaGato=cargar(carpetaGato)
  total=rutaPerro+rutaGato
  print(len(total))

  #Division de procesos (2 procesos)
  division=len(total)/2
  procesoPerro=total[:division]
  procesoGato=total[division:]

  manager=Manager()
  resultados=manager.list()

  proceso1=Process(target=procesarImagenes,args=(procesoPerro,resultados))
  proceso2=Process(target=procesarImagenes,args=(procesoGato,resultados))

  proceso1.start()
  proceso2.start()

  proceso1.join()
  proceso2.join()
  print("Procesamiento completo")
  print("Resultados procesamiento",resultados) 
  print("Tamaño de resultados",len(resultados))
import time
import threading #hilos

def tareaN(n):
    for tarea in range(500):
        print(f"Tarea completada {tarea}")
        time.sleep(5)

hilo1=threading.Thread(target=tareaN,args=("Hilo 1",))
hilo2=threading.Thread(target=tareaN,args=("Hilo 2",))

hilo1.start()
hilo2.start()
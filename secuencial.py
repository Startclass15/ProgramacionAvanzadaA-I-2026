#Simulacion de varias tareas secuencias
import time

def tareaN(n):
    print(f"Tarea iniciada...{n}")
    time.sleep(0.01)
    print("Tarea Finalizada")

inicio=time.time()

for tarea in range(500):
    tareaN(tarea)

fin=time.time()

print(f"Tiempo en completar {inicio} - final: {fin}")

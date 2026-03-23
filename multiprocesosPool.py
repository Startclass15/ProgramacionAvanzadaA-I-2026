from multiprocessing import Pool
import time

def tareaN(n):
    time.sleep(0.001)
    return n

inicio=time.time()

with Pool(2) as proceso:
    proceso.map(tareaN, range(1))

final=time.time()
print("Tiempo total inicio:",inicio, "final",final )
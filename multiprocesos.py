from multiprocessing import Process #Dependencia de multiprocesos
import time

def tareaN(n):
    print("Procesando ",n)
    time.sleep(2)

inicio=time.time()

procesos=[]
for proceso in range(4):
    p=Process(target=tareaN, args=(proceso,))
    procesos.append(p)
    p.start()

for p in procesos:
    p.join()

final=time.time()

print("Tiempo total inicio:",inicio, "final",final )
print(final-inicio)


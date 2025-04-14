import threading
import time
import queue

class ServidorCentral:
    def __init__(self):
        self.recurso_livre = True 
        self.fila_solicitacoes = queue.Queue()  
        self.lock = threading.Lock() 

    def solicitar_acesso(self, cliente_id):
        print(f"Cliente {cliente_id} solicitou acesso ao recurso.")
        self.fila_solicitacoes.put(cliente_id) 
        self.processar_solicitacao()

    def processar_solicitacao(self):
        with self.lock: 
            if self.recurso_livre and not self.fila_solicitacoes.empty():
                cliente_id = self.fila_solicitacoes.get() 
                self.recurso_livre = False
                print(f"Cliente {cliente_id} obteve acesso ao recurso.")
                threading.Thread(target=self.usar_recurso, args=(cliente_id,)).start()

    def usar_recurso(self, cliente_id):
        print(f"Cliente {cliente_id} está usando o recurso...")
        time.sleep(2)  
        print(f"Cliente {cliente_id} terminou de usar o recurso.")
        self.liberar_recurso()

    def liberar_recurso(self):
        with self.lock:
            self.recurso_livre = True
            print("Recurso liberado.")
            self.processar_solicitacao()  

def cliente(servidor, cliente_id):
    servidor.solicitar_acesso(cliente_id)

if __name__ == "__main__":
    servidor = ServidorCentral()
   
    num_clientes = 5
    threads = []
    for i in range(num_clientes):
        t = threading.Thread(target=cliente, args=(servidor, i))
        threads.append(t)
        t.start()
        time.sleep(0.5)  

    for t in threads:
        t.join()
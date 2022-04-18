import socket
import time

def msgSend(message, connexion):
    connexion.sendall(bytes(message, "utf-8"))
    time.sleep(0.01)
    
def msgRecv(connexion):
    message = connexion.recv(256).decode()
    time.sleep(0.01)
    return message
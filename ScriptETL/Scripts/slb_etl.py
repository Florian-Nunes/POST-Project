import mysql.connector
from mysql.connector import errorcode
import json

###################################################################
#                          Script SLB                             #
###################################################################

#_________________________________________________________________#
#__________________Connexion a la base de donnee__________________#
config = {
    'user' : 'XXXX',
    'password' : 'XXXX',
    'host' : 'localhost',
    'database' : 'myetl',
    'raise_on_warnings' : True
}

try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("L'utilisateur ou le mot de passe n'est pas correct")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("La bdd n'existe pas")
    else:
        print(err)

    exit()
#_________________________________________________________________#
#______________Recuperation des donnees dans le json______________#

fileslb = open("/home/flo/Bureau/formation django/ScriptETL/SLB/slb.json", "r")
slbcontent = fileslb.read()
slb_objpython = json.loads(slbcontent) #transforme les donnees en obj python

cursorInsert = cnx.cursor()

memSLBId = []
data_SLB_2 = {}
#boucle for pour parcourir les elements du tableau, puis creation d'un second dictionnaire qui contient nos informations
for i in slb_objpython[0]:
    data_SLB_2[i['LoadBalancerId']]  = {
        'SLBName': i['LoadBalancerName'],
        'SLBIp': i['Address'],
        'SLBNetworkType': i['NetworkType'],
        'SLBPort': '',
        'SLBProtocol': '',
        'SLBAlgorithm': '',
        'SLBPersistence': 0,
        'SLBStatus': ''
    }
#variable temp pour stocker ID et bool pour indiquer si on doit continuer a collecter les informations
temp_id=''
temp_bool=False
#boucle for pour parcourir les elements de slb_objpython a partir de l'index 1 pour ajouter les informations supplémentaire
for i in slb_objpython[1:]:
    if temp_bool:
        temp_verif=0
        if 'Scheduler' in i:
            data_SLB_2[temp_id]['SLBAlgorithm'] = i['Scheduler']
        if 'PersistenceTimeout' in i:
            data_SLB_2[temp_id]['SLBPersistence'] = i['PersistenceTimeout']
        temp_bool=False

    if 'ListenerPortsAndProtocal' in i:
        temp_port = []
        temp_protocol = []
        for c in i['ListenerPortsAndProtocal']['ListenerPortAndProtocal']:
            temp_port.append(str(c['ListenerPort']))
            temp_protocol.append(str(c['ListenerProtocal']))

        data_SLB_2[i['LoadBalancerId']]['SLBPort'] = ','.join(temp_port)
        data_SLB_2[i['LoadBalancerId']]['SLBProtocol'] = ','.join(temp_protocol)
        data_SLB_2[i['LoadBalancerId']]['SLBStatus'] = i['LoadBalancerStatus']
        temp_id=i['LoadBalancerId']
        temp_bool=True
#on utilise la methode join pour joindre les elements d'une liste en une chaine de caractere
memSLBId = data_SLB_2.keys()

#for va parcourir les entrees dans le dictionnaire dataSLB2, pour chaque entree depuis key, on creer un autre dic slb insert qui contient les informations qu'on ve enregistrer
for key in data_SLB_2:

    data_SLB_Insert = {
        'SLBName' : data_SLB_2[key].get('SLBName','NULL'),
        'SLBId' : key,
        'SLBIp' : data_SLB_2[key].get('SLBIp','NULL'),
        'SLBPort' : data_SLB_2[key].get('SLBPort','NULL'),
        'SLBEnvironment' : 'NULL',
        'SLBProtocol' : data_SLB_2[key].get('SLBProtocol','NULL'),
        'SLBNetworkType' : data_SLB_2[key].get('SLBNetworkType','NULL'),
        'SLBAlgorithm' : data_SLB_2[key].get('SLBAlgorithm','NULL'),
        'SLBPersistence' : int(data_SLB_2[key].get('SLBPersistence', 0)),
        'SLBStatus' : data_SLB_2[key].get('SLBStatus','NULL')
    }

    verifActionSLB = ("SELECT COUNT(*) FROM ETL_slb WHERE SLBId = '%s'")
    verifActionSLB_val = (data_SLB_Insert['SLBId'],)
    cursorInsert.execute(verifActionSLB, verifActionSLB_val)
    resultVerifSLB = cursorInsert.fetchall()
    print(resultVerifSLB)
#condition if pour verifer si le slb existe deja, puis instruction sql pour ajouter les variable en utilisant cursorinsert
    if resultVerifSLB[0]>0:
        deleteActionSLB = ("delete from ETL_slb where SLBId = '%s'")
        cursorInsert.execute(deleteActionSLB, verifActionSLB_val)
    
    addActionSLB = ("INSERT INTO ETL_slb (SLBName, SLBId, SLBIp, SLBPort, SLBEnvironment, SLBProtocol, SLBNetworkType, SLBAlgorithm, SLBPersistence, SLBStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    addActionSLB_val = (
        data_SLB_Insert['SLBName'],
        data_SLB_Insert['SLBId'],
        data_SLB_Insert['SLBIp'],
        data_SLB_Insert['SLBPort'],
        data_SLB_Insert['SLBEnvironment'],
        data_SLB_Insert['SLBProtocol'],
        data_SLB_Insert['SLBNetworkType'],
        data_SLB_Insert['SLBAlgorithm'],
        data_SLB_Insert['SLBPersistence'],
        data_SLB_Insert['SLBStatus']
        )
    cursorInsert.execute(addActionSLB, addActionSLB_val)

#_________________________________________________________________#
#____________Load des donnees dans la bdd via requetes____________#

    
    # addActionSLB = ("INSERT INTO SLB"
    # "(SLBName, SLBId, SLBIp, SLBPort, SLBEnvironment, SLBProtocol, SLBNetworkType, SLBAlgorithm, SLBPersistence, SLBStatus"
    # "VALUES (%(SLBName)s, %(SLBId)s, %(SLBIp)s, %(SLBPort)s, %(SLBEnvironment)s, %(SLBProtocol)s, %(SLBNetworkType)s, %(SLBAlgorithm)s, %(SLBPersistence)s, %(SLBStatus)s)")

#_________________________________________________________________#
#_______________Verification des donnees dans la db_______________#

StillExistActionSLB = ("SELECT * FROM ETL_slb")
cursorInsert.execute(StillExistActionSLB)
StillExistResultSLB = cursorInsert.fetchall()

for row in StillExistResultSLB:
    if row[2] not in memSLBId:
        deleteActionSLB = ("delete from ETL_slb where SLBId = %s")
        adr = (row[2],)
        cursorInsert.execute(deleteActionSLB, adr)
        print(row[2],"a ete supprime")
# #_________________________________________________________________#
# #__________Commit des donnees et fermeture des connexions_________#
cnx.commit()
cursorInsert.close()
cnx.close()
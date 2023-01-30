import mysql.connector
from mysql.connector import errorcode
import json
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import time

###################################################################
#                          Script ETL_ecs                             #
###################################################################

#_________________________________________________________________#
#__________________Connexion a la base de donnee__________________#
config = {
    'user' : 'infra',
    'password' : 'infra',
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

fileobj = open("/home/flo/Bureau/formation django/ScriptETL/ECS/ecs.json", "r")
jcontent = fileobj.read()
obj_python = json.loads(jcontent)

cursorInsert = cnx.cursor()

memHostName = []

for i in obj_python["Instances"]["Instance"]:
    Instancename = (i["InstanceName"])
    # print(Instancename)
    Hostname = (i["HostName"])
    memHostName.append(Hostname)
    #print (Hostname)
    Primaryipadd = (i["NetworkInterfaces"]["NetworkInterface"][0]["PrimaryIpAddress"])
    #print (Primaryipadd)
    OSVersion = (i["OSName"])
    # print (OSVersion)
    InstanceType = (i["InstanceTypeFamily"])
    # print (InstanceType)
    Cpu = (i["Cpu"])
    # print (Cpu)
    Memory = (i["Memory"])
    # print (Memory)
    Status = (i["Status"])
    # print (Status)
    HardwareInfo = (i["InstanceBandwidthRx"])
    # print (HardwareInfo)
    VSwitch = (i["VpcAttributes"]["VSwitchId"])
    # print (VSwitch)
    SecurityGroup = ";".join(i["SecurityGroupIds"]["SecurityGroupId"])
    # print (SecurityGroup)

    data_utilisateur = {
        'InstanceName' : Instancename,
        'HostName' : Hostname,
        'PrimaryIpAddress' : Primaryipadd,
        'OSName' : OSVersion,
        'InstanceTypeFamily' : InstanceType,
        'Cpu' : Cpu,
        'Memory' : Memory,
        'Status' : Status,
        'InstanceBandwidthRx' : HardwareInfo,
        'VSwitchID' : VSwitch,
        'SecurityGroupId' : SecurityGroup,
        'Lastseen' : datetime.datetime.now()
    }
#_________________________________________________________________#
#____________Load des donnees dans la bdd via requetes____________#

    verifAction = ("SELECT COUNT(*) FROM ETL_ecs WHERE HostName = %(HostName)s")
    cursorInsert.execute(verifAction, data_utilisateur)
    resultVerif = cursorInsert.fetchall()
    #print(resultVerif)

    if resultVerif[0][0]>0:
        deleteAction = ("delete from ETL_ecs where HostName = %(HostName)s")
        cursorInsert.execute(deleteAction, data_utilisateur)
        
    addAction = ("INSERT INTO ETL_ecs"
    "(InstanceName, HostName, PrimaryIpAddress, OSName, InstanceTypeFamily, Cpu, Memory, Status, InstanceBandwidthRx, VSwitchID, SecurityGroupId, Lastseen)"
    "VALUES (%(InstanceName)s, %(HostName)s, %(PrimaryIpAddress)s, %(OSName)s, %(InstanceTypeFamily)s, %(Cpu)s, %(Memory)s, %(Status)s, %(InstanceBandwidthRx)s, %(VSwitchID)s, %(SecurityGroupId)s, %(Lastseen)s)")

    cursorInsert.execute(addAction, data_utilisateur)
    #print (cursorInsert.rowcount, " ETL_ecs has been added")

#_________________________________________________________________#
#___________________Creation du fichier de log____________________#
    
    logfile = "/home/flo/Bureau/formation django/ScriptETL/ECS/log_source/ecs_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('Hostname : %s was added on the ECS', Hostname)
#_________________________________________________________________#
#_______________Verification des donnees dans la db_______________#

StillExistAction = ("SELECT * FROM ETL_ecs")
cursorInsert.execute(StillExistAction)
StillExistResult = cursorInsert.fetchall()

for row in StillExistResult:
    if row[2] not in memHostName:
        deleteAction = ("update ETL_ecs set Status = 'Removed' where HostName = %s")
        adr = (row[2],)
        cursorInsert.execute(deleteAction, adr)
        print(row[2],"was update")
#_________________________________________________________________#
#__________Commit des donnees et fermeture des connexions_________#
cnx.commit()
cursorInsert.close()
cnx.close()


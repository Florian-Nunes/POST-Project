import mysql.connector
from mysql.connector import errorcode
import json
from pprint import pprint

###################################################################
#                          Script RDS                             #
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

fileRDS = open("/home/flo/Bureau/formation django/ScriptETL/RDS/rds.json", "r")
RDScontent = fileRDS.read()
RDS_objpython = json.loads(RDScontent)

cursorInsert = cnx.cursor()

memRDSId = []
data_RDS = []
data_RDS_2 = {}
count = 0

for i in RDS_objpython:
    RDSId = ""
    RDSIp = ""
    RDSPort = ""
    RDSCpu = ""
    RDSMemory = ""
    RDSIops = ""
    RDSMaxConnection = ""
    RDSEngine = ""
    RDSInstanceType = ""
    RDSVSwitch = ""
    RDSStatus = ""
    if "Items" in i:
        if "DBInstanceAttribute" in i["Items"] and len(i["Items"]["DBInstanceAttribute"])>0:
            if "DBInstanceId" in i["Items"]["DBInstanceAttribute"][0]:
                if i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"] not in data_RDS:
                    data_RDS.append(i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"])
                    data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]] = {}
            RDSCpu = (i["Items"]["DBInstanceAttribute"][0]["DBInstanceCPU"])
            RDSMemory = (i["Items"]["DBInstanceAttribute"][0]["DBInstanceMemory"])
            RDSIops = (i["Items"]["DBInstanceAttribute"][0]["MaxIOPS"])
            RDSMaxConnection = (i["Items"]["DBInstanceAttribute"][0]["MaxConnections"])
            RDSEngine = (i["Items"]["DBInstanceAttribute"][0]["Engine"])
            RDSInstanceType = (i["Items"]["DBInstanceAttribute"][0]["DBInstanceType"])
            RDSVSwitch = (i["Items"]["DBInstanceAttribute"][0]["VSwitchId"])
            RDSPort = (i["Items"]["DBInstanceAttribute"][0]["Port"])
            RDSStatus = (i["Items"]["DBInstanceAttribute"][0]["DBInstanceStatus"])
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSMemory'] = RDSMemory
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSCpu'] = RDSCpu
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSIops'] = RDSIops
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSMaxConnection'] = RDSMaxConnection
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSEngine'] = RDSEngine
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSInstanceType'] = RDSInstanceType
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSVSwitch'] = RDSVSwitch
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSPort'] = RDSPort
            data_RDS_2[i["Items"]["DBInstanceAttribute"][0]["DBInstanceId"]]['RDSStatus'] = RDSStatus

        else:
            if "DBInstance" in i["Items"]:
                if len(i["Items"]["DBInstance"])>0:
                    for c in i["Items"]["DBInstance"]:
                        if c["DBInstanceId"] not in data_RDS:
                            data_RDS.append(c["DBInstanceId"])
                            data_RDS_2[c["DBInstanceId"]] = {}

    else:
        if "DBInstanceNetInfos" in i:
            RDSIp = (i["DBInstanceNetInfos"]["DBInstanceNetInfo"][0]["IPAddress"])
            temp_id = i["DBInstanceNetInfos"]["DBInstanceNetInfo"][0]["ConnectionString"].split('.')[0].replace(' ','')
            data_RDS_2[temp_id]['RDSIp'] = RDSIp

#_________________________________________________________________#
#____________Load des donnees dans la bdd via requetes____________#

for key in data_RDS_2:
    data_RDS_Insert = {
        'RDSId' : key,
        'RDSIp' : data_RDS_2[key].get('RDSIp', 'NULL'),
        'RDSPort' : int(data_RDS_2[key].get('RDSPort', 0)),
        'RDSCpu' : int(data_RDS_2[key].get('RDSCpu', 0)),
        'RDSMemory' : int(data_RDS_2[key].get('RDSMemory', 0)),
        'RDSIOPS' : data_RDS_2[key].get('RDSIops', 0),
        'RDSMaxConnection' : data_RDS_2[key].get('RDSMaxConnection', 0),
        'RDSEngine' : data_RDS_2[key].get('RDSEngine', 'NULL'),
        'RDSInstanceType' : data_RDS_2[key].get('RDSInstanceType', 'NULL'),
        'RDSVSwitch' : data_RDS_2[key].get('RDSVSwitch', 'NULL'),
        'RDSStatus' : data_RDS_2[key].get('RDSStatus', 'NULL')
    }
    #pprint(data_RDS_Insert)
    #pprint(data_RDS_Insert)
    verifActionRDS = ("SELECT COUNT(*) FROM ETL_rds WHERE RDSId = %(RDSId)s")
    cursorInsert.execute(verifActionRDS, data_RDS_Insert)
    resultVerifRDS = cursorInsert.fetchall()
    #print(resultVerifRDS)

    if resultVerifRDS[0][0]>0:
        deleteActionRDS = ("delete from ETL_rds where RDSId = %(RDSId)s")
        cursorInsert.execute(deleteActionRDS, data_RDS_Insert)
        
    addActionRDS = ("INSERT INTO ETL_rds (RDSId, RDSIp, RDSPort, RDSCpu, RDSMemory, RDSIOPS, RDSMaxConnection, RDSEngine, RDSInstanceType, RDSVSwitch, RDSStatus ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    addActionRDS_val = (
        data_RDS_Insert['RDSId'],
        data_RDS_Insert['RDSIp'],
        data_RDS_Insert['RDSPort'],
        data_RDS_Insert['RDSCpu'],
        data_RDS_Insert['RDSMemory'],
        data_RDS_Insert['RDSIOPS'],
        data_RDS_Insert['RDSMaxConnection'],
        data_RDS_Insert['RDSEngine'],
        data_RDS_Insert['RDSInstanceType'],
        data_RDS_Insert['RDSVSwitch'],
        data_RDS_Insert['RDSStatus']
        )
    cursorInsert.execute(addActionRDS, addActionRDS_val)
    print (cursorInsert.rowcount, "RDS ajoute.")
    print("____________________________")
    pprint(data_RDS_Insert)
#_________________________________________________________________#
#_______________Verification des donnees dans la db_______________#

# StillExistActionRDS = ("SELECT * FROM RDS")
# cursorInsert.execute(StillExistActionRDS)
# StillExistResultRDS = cursorInsert.fetchall()

# for row in StillExistResultRDS:
#     if row[2] not in memRDSId:
#         deleteActionRDS = ("delete from RDS where RDSId = %s")
#         adr = (row[2],)
#         cursorInsert.execute(deleteActionRDS, adr)
#         print(row[2],"a ete supprime")
#_________________________________________________________________#
#__________Commit des donnees et fermeture des connexions_________#
cnx.commit()
cursorInsert.close()
cnx.close()
pprint(data_RDS_2)
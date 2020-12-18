import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging

import csv
import matplotlib.pyplot as plt
import os

def exportarCSV(datosRef, nameArchive):
    with open(f'{nameArchive}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ["Documento","fecha"]

        for i in range(1,31):
            header.append(f'P{i}')
        writer.writerow(header)
        for doc in dataset:
            body = []
            body.append(u"{}".format(doc.id))
            datasetUser = db.collection("Respuestas").document(u"{}".format(doc.id)).get().to_dict()
            keyordered = sorted(datasetUser.keys())
            if len(keyordered) != 0:
                for key in keyordered:
                    body.append(key)
                    for response in datasetUser[key]:
                        if(key != "ultima hora"):
                            body.append(response)
                    writer.writerow(body)
                    for i in range(1,len(body)):
                        body.pop(-1)

def ingresarUsuario(dataBaseRef):
    documento = input('Ingrese Dni: ')
    nombre = input('Ingrese el nombre: ')
    mail = input('Ingrese un mail: ')
    dataBaseRef.collection(u'DataUsuarios').add(
        {
            u'documento': int(documento), 
            u'nombre': u'{}'.format(nombre),
            u'mail': u'{}'.format(mail)
        }
    )
    dniN = documento + "-" + nombre[0] 
    dataBaseRef.collection(u'Respuestas').document(dniN).set({})

def graficarDatos(dataset):
    y = []
    valuesordered = []
    flag = True
    i = 0
    for doc in dataset:
        i+=1
        print(f'{i}. {doc.id}')
        listaPacientes.append(doc.id)

    optGraf = int(input('-> '))
    datasetUser = db.collection("Respuestas").document(listaPacientes[optGraf-1]).get().to_dict()
    keyordered = sorted(datasetUser.keys())
    for key in keyordered:
        valuesordered.append(datasetUser[key])
    print('ingrese "a" para retroceder, "d" o espacio para avanzar y "e" para salir del graficador')
    i = 0
    while flag:
        # optPreGraf = int(input(f'pregunta a graficar(1-{len(valuesordered[0])}) -> '))
        for b in range(0, len(keyordered)):
            y.append(valuesordered[b][i])    
        plt.figure(figsize=(13,5))
        plt.ion
        plt.ylim(0,7)
        plt.title(f'pregunta {i+1}')
        print(y)
        plt.bar(keyordered,y)
        plt.show(block=False)
        optGrafNav = input('->')
        plt.close()
        y.clear() 
        if  optGrafNav == 'a' :
            if i-1 < 0:
                i=29
            else:
                i-=1
        elif optGrafNav == 'd' or optGrafNav == '':
            if i+1 > 29:
                i = 0
            else:
                i+=1
        elif optGrafNav == 'e':
            flag=False
    print('saliendo del graficador')
        
#acceso a cloud firebase
# cred = credentials.Certificate("C:/Users/cfran/Desktop/serviceAccountKey.json")
cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "PROJECT_ID",
        "private_key_id": "PRIVATE_KEY_ID",
        "private_key": "PRIVATE_KEY",
        "client_email": "CLIENT_EMAIL",
        "client_id": "CLIENT_ID",
        "auth_uri": "AUTH_URI",
        "token_uri": "TOKEN_URI",
        "auth_provider_x509_cert_url": "PROVIDER_CERT_URL",
        "client_x509_cert_url": "CLIENT_CERT_URL"
    }   
)
firebase_admin.initialize_app(cred)
#acceso al documento de usuario

db = firestore.client()

x = []
_y = []
loop = True
while loop:
    dataset = db.collection("Respuestas").stream()
    print("1. exportar respuestas a CSV")
    print("2. ingresar un nuevo usuario a la BD")
    print("3. graficar datos de usuario")
    print("4. salir")

    opt = input("-> ")
    if opt == '1':
        print("exportando el archivo")
        exportarCSV(dataset, "test")
        print("exportacion finalizada")
        print("=============================")

    elif opt == '2':
        ingresarUsuario(db)
        print("=============================")
        print("usuario creado")
        print("=============================")
    elif opt == '3':
        listaPacientes = []
        print('Lista de usuarios')
        graficarDatos(dataset)

    elif opt == '4':
        loop = False

    else:
        print('opcion elegida o caracter ingresado desconocido')
        print("=============================")

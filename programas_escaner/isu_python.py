import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests, sys, time, os

import PyCmdMessenger

ARDUINO = True
SERVIDOR = True

BASE_URL = "http://localhost:8000/"
STATUS_URL = BASE_URL + "comensales/status"
SEND_URL = BASE_URL + "comensales/newcode?qr={}&pass=hola"

#Las buenas variables globales gitanas
comidas_actuales_servidas = 0
last_qr_code = ""
same_qr_retries = 0
comida_actual = "Ninguna"

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        if str(barcodeType)!= "QRCODE":
            break
        
        print("Barcode: "+barcodeData +" | Type: "+barcodeType)
        return str(barcodeData)
    return ""

def imprimir_modo_espera():
    global c
    c.send("print2", "{} {}".format(comidas_actuales_servidas, comida_actual), "Please scan code")

def codigo_leido(barcode:str):
    global last_qr_code
    if last_qr_code == barcode:
        print("Nos acaba de mostrar este qr, así que nada")
        return False
    last_qr_code = barcode
    if SERVIDOR:
        response = requests.get(SEND_URL.format(barcode))
        res = response.json()
        if res['status'] == 200:
            global comidas_actuales_servidas
            comidas_actuales_servidas = res['comidas_turno']
            print("Comida añadida con éxito")
            if ARDUINO:
                global c
                global comida_actual
                print_name = "{}".format(res['display_name'] if len(res['display_name']) < 16 else res['display_name'][0:15])
                c.send("print2", "{} {}".format(comidas_actuales_servidas, comida_actual), "{}".format(print_name))
                c.send("ok_sound")
            time.sleep(3)
            return True
        elif res['status']==409:
            print("Este ({}) ya ha pasado su código".format(barcode))
            if ARDUINO:
                print_name = res['display_name'] if len(res['display_name']) < 16 else res['display_name'][0:15]
                c.send("print2", "{}".format(print_name), "Duplicated scan!")
                c.send("fail_sound")
            time.sleep(3)
        else:
            print("Nunca deberíamos llegar aquí. Comprueba el server anda")
        



# Conexión al arduino
if ARDUINO:
    arduino = PyCmdMessenger.ArduinoBoard("/dev/ttyUSB0",baud_rate=19200)

    comandos_arduino = [
        ["ping",""],
        ["pong",""],
        ["conectando", ""],
        ["print_high", "s"],
        ["print2", "ss"],
        ["print_low", "s"],
        ["ok_sound",""],
        ["fail_sound",""],
        ["apagar",""]
        ]

    c = PyCmdMessenger.CmdMessenger(arduino, comandos_arduino)

    #Comprobar que tenemos arduino

    c.send("ping")
    rec = c.receive()
    if rec[0] == "pong":
        print("Arduino conectado")
    else:
        print("No hay conexión con el arduino")
        ARDUINO = False

    c.send("conectando")

#Delay inicial para asegurarnos que estamos conectados a internet
print("Espera que me conecte")
time.sleep(5)
print("Trying to ping server")

if SERVIDOR:
    response = requests.get(STATUS_URL)
    if response.json()['status'] == 200:
        print("Conectados con éxito. Seguimos")
        res = response.json()
        print(res)
        comidas_actuales_servidas = res['comidas_turno']
        comida_actual = res['comida_activa']
    else:
        print("Error de conexión. Abortando")
        sys.exit(1)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
#codec = 0x47504A4D  # MJPG
cap.set(cv2.CAP_PROP_FPS, 20.0)
#cap.set(cv2.CAP_PROP_FOURCC, codec)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#cap.open(0)
if ARDUINO and SERVIDOR:
    imprimir_modo_espera()

while True:
    ret, frame = cap.read()
    value = decoder(frame)
    if len(value)!= 0:
        if value == "ApagarQr":
            print("Apagando el sistema")
            if ARDUINO:
                c.send("apagar")
            os.system("poweroff")
        if value.find("Fran") != -1:
            codigo_leido(value)
            if SERVIDOR:
                response = requests.get(STATUS_URL)
                if response.json()['status'] == 200:
                    print("Conectados con éxito. Seguimos")
                    res = response.json()
                    print(res)
                    comidas_actuales_servidas = res['comidas_turno']
                    comida_actual = res['comida_activa']
                else:
                    print("Algo ha ido de culo, la hemos liao. Revisa esta vaina loca")
        else:
            codigo_leido(value)
        imprimir_modo_espera()


    
import cv2
import numpy as np
import pyttsx3
import engineio
import PySimpleGUI as sg
from tkinter import *

global frame
global window

def speak(text):
        engineio = pyttsx3.init()
        voices = engineio.getProperty('voices')
        engineio.setProperty('rate', 130)    # Aquí puedes seleccionar la velocidad de la voz
        engineio.setProperty('voice',voices[0].id)
        engineio.say(text)
        engineio.runAndWait()

def dibujar(mask,color,nomc,frame):
    _,contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 3000:
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
            if (nomc == "azul"):
                    window['texto'].update('El color es azul')
                    speak("el color es" + nomc)
            if (nomc == "rojo"):
                    window['texto'].update('El color es rojo')
                    speak("el color es" + nomc)
            if (nomc == "verde"):
                    window['texto'].update('El color es verde')
                    speak("el color es" + nomc)

#interfaz de usuario
def ventana():
        #lbltext = texto
        azulBajo = np.array([100,100,20],np.uint8)
        azulAlto = np.array([125,255,255],np.uint8)

        verdeBajo = np.array([46,100,20],np.uint8)
        verdeAlto = np.array([75,255,255],np.uint8)

        redBajo1 = np.array([0,100,20],np.uint8)
        redAlto1 = np.array([5,255,255],np.uint8)
        redBajo2 = np.array([175,100,20],np.uint8)
        redAlto2 = np.array([179,255,255],np.uint8)

        font = cv2.FONT_HERSHEY_SIMPLEX
                        
        cap = cv2.VideoCapture(0)
        sg.theme('LightGrey1')
        
        image_elem = window['-image-']

        #Iniciamos la lectura y actualizacion
        while cap.isOpened():
                #Obtenemos informacion de la interfaz grafica y video
                event, values = window.read(timeout=0)
                ret, frame = cap.read()

                #Si tomamos foto
                if event == 'Preguntar':
                        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                        maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
                        maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
                        maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
                        maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
                        maskRed = cv2.add(maskRed1,maskRed2)
                        
                        dibujar(maskAzul,(255,0,0),"azul",frame)
                        dibujar(maskVerde,(46,100,20),"verde",frame)
                        dibujar(maskRed,(0,0,255),"rojo",frame)
                if event == 'Limpiar':
                        
                        ventana()

                #Mandamos el video a la GUI
                imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
                image_elem.update(data=imgbytes)
                #numero = numero + 1

#Definimos los elementos de la interfaz grafica
layout = [[sg.Image(filename='', key='-image-')],[sg.Button('Limpiar'),sg.Button('Preguntar'),sg.Text(size=(10,2),key='texto')]]
#Creamos la interfaz grafica
window = sg.Window('Detectar colores',layout,no_titlebar=False,location=(0, 0))

ventana()

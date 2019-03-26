#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from functools import partial
import cv2
import Tkinter as tk
import locale
import socket
import sys
import threading
import os
import time
import numpy


#Vars:
host= ''	
mediaPfad=''
mWindow='Apotheke'
cap=''
delay=''
showKassenzeile = False
artikelbezeichnung=''
menge=''
einzelbetrag=''
listeBilder=[]
listeFilme=[]
t=''
windowHeight=500
windowWidth=820

appExit = False
mySocket=''


#cv2.resizeWindow("Apotheke",windowWidth,windowHeight)




def getConfigs():
	global host
	global port
	global delay
	configFile = open("config.txt","r")
	for line in configFile:
		if line.split("=")[0] == "host":
			host = line.split("=")[1]
		if line.split("=")[0] == "port":
			port = int(line.split("=")[1])
			print ("Port:" ,port)
		if line.split("=")[0] == "delay":
			delay = int(line.split("=")[1])
		print (line)

def cleanExit():
	global appExit
	print ("EXIT-EXIT-EXIT")	
	appExit = True

def setKassenzeile():
	
	if globals()["showKassenzeile"]:
		font=cv2.FONT_HERSHEY_SIMPLEX
		if len(globals()["artikelbezeichnung"]) > 35:
			globals()["artikelbezeichnung"] = globals()["artikelbezeichnung"][0:30]
			globals()["artikelbezeichnung"] = globals()["artikelbezeichnung"]+"..."
		# Rechteck (links oben, rechts unten, Farbe,  Strichstärke)
		cv2.rectangle(frame,(0,435), (810,530), (0,0,0),-1) 
		cv2.putText(frame,"Artikel",(5,460), font, 0.5,(255,255,255),1)
		cv2.putText(frame,"Menge",(450,460), font, 0.5,(255,255,255),1)
		cv2.putText(frame,"Betrag",(650,460), font, 0.5,(255,255,255),1)
		cv2.line(frame,(0,470),(810,470),(255,255,255),1)
		cv2.putText(frame,globals()["artikelbezeichnung"],(5,500), font, 0.7,(255,255,255),1)
		cv2.putText(frame,globals()["menge"],(450,500), font, 0.7,(255,255,255),1)
		cv2.putText(frame,globals()["einzelbetrag"] + "  CHF",(650,500), font, 0.7,(255,255,255),1)

def getAllMedia():
	globals()["mediaPfad"] = os.getcwd()+"/assets/"
	dateiListe = os.listdir(mediaPfad)
	for datei in dateiListe:	
		dateiTyp = datei[datei.rfind("."):len(datei)]
		print ("Typ: " , dateiTyp)
		if dateiTyp == ".png" or dateiTyp == ".jpg" or dateiTyp == ".jpeg" :
			print("Ein Bild: " , str(datei))
			globals()["listeBilder"].append(str(datei))
		elif dateiTyp == ".mp4" or dateiTyp == ".ogg":
			print ("Ein Film :" ,str(datei))
			globals()["listeFilme"].append(str(datei))

def dataTransfer(conn):
	global appExit	
	global kassenzeile
	#print("in dataTransfer")
	# schleife zum empfangen und versenden von Daten bis Ende
	while (not appExit):
		#Recieve Data
		data = conn.recv(1024) #Daten empfangen
		print(data)
		if data:
			print("Raw: ",data)
			data = data.decode('utf-8')
			print("Empfangen", data)
			if data.find("|"):			
				dataMessage = data.split('|') # commando holen
				command = dataMessage[0]
				if command == "Exit":					
					cleanExit()
				elif command == 'GET':
					print("GET")
					print(dataMessage[1])
					try:						
						print(dataMessage[1])
						globals()["artikelbezeichnung"]=  dataMessage[1]
						globals()["menge"]=  dataMessage[3]
						globals()["einzelbetrag"]=  dataMessage[2]
						globals()["showKassenzeile"]=True       
					finally:
						print("Break")			
						break				
				elif command=='WERB':
					print("WERB")
					try:	
						globals()["showKassenzeile"]=False
						setKassenzeile()  
					finally:
						break
				elif command=='QRAN':
					try:	
						print("QRCode an")
						param.showQRCode(str(dataMessage[1]))
						
					finally:					
						break
				elif command=='QRAUS':
					try:	
						print("QRCode aus")
						param.closeQRCode()	
						
					finally:					
						break
				else:									
					break

def startServerThread():
	global appExit
	global host
	socketServer = globals()["mySocket"]
	print("Starte Server thread")
	
	socketServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("Socket Created")
	try:
		socketServer.bind((host,port))
	except socket.error as e:			
		print ("Mein Socketerror: " , str(e))
		if e.errno==98:
			print(str(e))
			socketServer.close()					
	print("socket bind complete")
	socketServer.listen(100) #eine Verbindung
	while (not appExit):
		print("listen")
		conn, addr = socketServer.accept()
		print("connected to :"+addr[0]+":"+str(addr[1]))	
		dataTransfer(conn)
	socketServer.close()
	print ("Server beendet")
		
def playVideo(pfadMedia, filepath):    
    global cap
    global appExit
    global mWindow    
    pfadFilm = pfadMedia+filepath
    cv2.namedWindow(mWindow,flags=cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(mWindow,-5,-80)
    cap = cv2.VideoCapture(pfadFilm)
    isRunning = True 
    while isRunning : 
        global frame  
        if not appExit:
            ret, frame = cap.read()
            isRunning = ret
        else:
            isRunning=False
        if ret :
            if(globals()["showKassenzeile"]) : 
                  setKassenzeile()                   
            cv2.imshow(mWindow, frame)             
        if cv2.waitKey(25) & 0xFF == ord('q') :
            isRunning = False
            appExit = True           
        print ("cap release")
    cap.release() 
    #cv2.destroyAllWindows()
    print ("Window destroyd")
     
    
def playImage(pfadMedia, filepath):
	global frame
	global appExit
	global mWindow
	global delay;
	if not appExit:
		pfadBild = pfadMedia+filepath
		print("Zeige : " ,pfadBild)
		millisEnd = 0
		cv2.namedWindow(mWindow,flags=cv2.WINDOW_AUTOSIZE)
		cv2.moveWindow(mWindow,-5,-80)
		while delay * 200 >  millisEnd and not appExit:
			frame = cv2.imread(pfadBild,1) 
			#millisStart  =  int(round(time.time()))
			if(globals()["showKassenzeile"]): 
				setKassenzeile()
				cv2.imshow(mWindow, frame)
			else:     
				cv2.imshow(mWindow, frame)			
			if cv2.waitKey(1) & 0xFF == ord('q') :
				isRunning = False
				appExit = True
			millisEnd +=1  #int(round(time.time()))
			print ("Timespan jetzt :" , millisEnd)
			#timespan += millisEnd - millisStart 
		#cv2.destroyAllWindows()




def doMultimedia():
	global appExit	
	for i in range (len(listeFilme)):
		if (not appExit):
			playVideo(mediaPfad, str(listeFilme[i]))
			pass
		else:
			print("Filme beendet")
			print("Appexit : " ,appExit)
			break	
	for i in range (len(listeBilder)):
		if (not appExit):
			playImage(mediaPfad, str(listeBilder[i]))
		else:
			print("Bilder beendet")
			print("Appexit : " ,appExit)
			break

def closeSocket():	
	global host
	global port
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,port))
		s.sendall(str.encode("Exit|0815"))
		s.close()
	except:
		pass




def main():
	global appExit
	getConfigs()
	getAllMedia()
	#eigenen Thread erstellen target -> funktion die Aufgerufen werden soll, name -> thread wird benannt(idFlag)	
	myThread = threading.Thread(target = startServerThread, name = "ServerThread" )
	myThread.start()
	while not appExit:
		doMultimedia()
	print("AppExit: " ,appExit)
	print ("closeSocket")
	cv2.destroyAllWindows();
	closeSocket()



main()

sys.exit()

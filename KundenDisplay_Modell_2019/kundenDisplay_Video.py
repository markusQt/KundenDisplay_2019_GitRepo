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
myMainGui=''
mediaPfad=''
mWindow=''
kasseWindow=''
showKassenzeile = False
kasseninfo=''
listeBilder=[]
listeFilme=[]
t=''
port=9999
appExit = False


def setKassenzeile():
	
	if globals()["showKassenzeile"]:
		font=cv2.FONT_HERSHEY_SIMPLEX
		if len(globals()["kasseninfo"]) > 35:
			globals()["kasseninfo"] = globals()["kasseninfo"][0:30]
			globals()["kasseninfo"] = globals()["kasseninfo"]+"..."
		cv2.line(frame,(12,100), (250,100), (255,0,0),15) 
		cv2.putText(frame,globals()["kasseninfo"],(10,500), font, 2,(0,0,0),2)

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
						globals()["kasseninfo"]=  dataMessage[1]
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
	print("Starte Server thread")
	global mySocket
	mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("Socket Created")
	try:
		mySocket.bind((host,port))
	except socket.error as e:			
		if e.errno==98:
			#print(str(e))
			mySocket.close()					
	print("socket bind complete")
	mySocket.listen(100) #eine Verbindung
	while (not appExit):
		print("listen")
		conn, addr = mySocket.accept()
		print("connected to :"+addr[0]+":"+str(addr[1]))	
		dataTransfer(conn)
	mySocket.close()
	print ("Server beendet")
		
def playVideo(pfadMedia, filepath):    
    global cap
    global appExit
    pfadFilm = pfadMedia+filepath
    cap = cv2.VideoCapture(pfadFilm)
    isRunning = True 
    while isRunning : 
        global frame  
        ret, frame = cap.read()
        isRunning = ret
        if ret :
            if(globals()["showKassenzeile"]): 
                  setKassenzeile()                   
            cv2.imshow(mWindow, frame)             
        if cv2.waitKey(25) & 0xFF == ord('q') or appExit == True:
            isRunning = False
            appExit = True
            break
        #cv2.waitKey(25) & 0xFF   
    print ("cap release")
    cap.release() 
    cv2.destroyWindow(mWindow)
    print ("Window destroyd")
     
    
def playImage(pfadMedia, filepath):
	global frame
	global appExit
	if not appExit:
		pfadBild = pfadMedia+filepath
		print("Zeige : " ,pfadBild)
		
		millisStart = 0
		millisEnd = 0
		delayInMilSecs = 3000;
		millisSecStart=0
		timespan = 0
		while delayInMilSecs >  timespan:
			frame = cv2.imread(pfadBild,1) 
			millisStart  =  int(round(time.time() * 1000))
			if(globals()["showKassenzeile"]): 
				setKassenzeile()
				cv2.imshow(mWindow, frame)
			else:     
				cv2.imshow(mWindow, frame)
			millisEnd =  int(round(time.time() * 1000))
			timespan += millisEnd - millisStart
			print ("Timespan jetzt :" , timespan)
			if cv2.waitKey(1) & 0xFF == ord('q') or appExit == True:
				isRunning = False
				appExit = True
				break
	cap.release() 
	cv2.destroyWindow(mWindow)

def doSlide():
	global root
	print("picture")	
	for x in range (len(listeBilder)):
		print(mediaPfad+listeBilder[x])
		photo1 = tk.PhotoImage(file=mediaPfad+listeBilder[x])
		print(type(root))
		picture = tk.Label(root,image = photo1)
		picture.pack()
		time.sleep(2)


def doMultimedia():
	global appExit	
	for i in range (len(listeFilme)):
		if (not appExit):
			playVideo(mediaPfad, str(listeFilme[i]))
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

def cleanExit():
	global appExit
	
	try:
		appExit = True 
	except:
		print ("Keine Fenster zu schliessen")	
	finally:
		quit()


def main():
	global appExit
	getAllMedia()
	#eigenen Thread erstellen target -> funktion die Aufgerufen werden soll, name -> thread wird benannt(idFlag)	
	myThread = threading.Thread(target = startServerThread, name = "ServerThread" )
	myThread.start()
	while not appExit:
		doMultimedia()
		#doSlideshow()
	print("Appexit zurueck in while : " ,appExit)
	if appExit:
		quit()

if (__name__ == '__main__'):
	main()

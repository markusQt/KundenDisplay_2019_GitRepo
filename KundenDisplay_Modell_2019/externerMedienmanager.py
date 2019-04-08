#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os 
import sys
import subprocess
import time
import tkinter
from  datetime  import datetime
import cv2
import numpy

#Vars:
size_810_x_520=(800,510)
breiteFilm=810
hoeheFilm=530
pfadZuMedia = ""
f=""
fehler = False
fehler=False
pfadZuMedia=""
modus=""
txtInfo=""
app=""

def exitApp():
	sys.exit()
	
def getConfigs():
	global pfadZuMedia
	global fehler
	print ("App: ",sys.argv[0])
	mfile = sys.argv[0]
	pathname = os.path.dirname(mfile)
	print ("Execpath: ",pathname)
	configFile = open("/home/apo/etc/configMedia.txt","r")
	try:
		for line in configFile:
			if line.split("=")[0] == "sourceMedia":
				pfadZuMedia = line.split("=")[1].strip('\n').strip()
		print ("sourceMedia:",pfadZuMedia)
	except:
		fehler = True

def deleteOldFiles():
	global pfadZuMedia
	#aktuelles Datum ermitteln	
	tmpDateToday= datetime.now()
	dateToday = str(tmpDateToday.day)+"."+str(tmpDateToday.month)+"."+str(tmpDateToday.year)[2:4]
	#print (dateToday)
	dateToQuery= datetime.strptime(dateToday,"%d.%m.%y")
	#print (dateToQuery)
	#print ("Programm greift auf :",pfadZuMedia,"zu.")
	#print(dateToday)
	try:
		for f in os.listdir(pfadZuMedia):
			tmpFilename = pfadZuMedia+f			
			if os.path.isfile(tmpFilename) and "@" in tmpFilename :			
				#print ("Treffer :",tmpFilename)
				tmpsplit = tmpFilename.split("@")
				tag = tmpsplit[1][0:2]
				monat = tmpsplit[1][2:4]
				jahr = tmpsplit[1][4:6]
				#print ("extrahiert :" ,tag,".",monat,".",jahr)
				tmpDateOfFile=tag + "." + monat + "." + jahr
				dateOfFile= datetime.strptime(tmpDateOfFile,"%d.%m.%y")
				if dateToQuery < dateOfFile:
					print("passt no: ", tmpFilename)
				else:
					print("have to kill: ",tmpFilename)
					os.remove(tmpFilename)
	except Exception as e:
		print("Fehler:", e)
		fehler = True

def renameFiles():
	global fehler
	global pfadZuMedia
	try:
		for f in os.listdir(pfadZuMedia):
			if os.path.isfile(pfadZuMedia+f):			
				os.rename(pfadZuMedia+f,(pfadZuMedia+f).replace(" ",""))
	except Exception as e:
		print("Fehler:", e)
		fehler = True


def konvertiereMedien():
	global f
	global pfadZuMedia
	global fehler
	global size_810_x_520
	global breiteFilm
	global hoeheFilm
	global txtInfo
	global app
	txtInfo.insert("end", "Konvertierung  wird gestartet , bitte warten ..... \n")
	app.update()
# richtigen Pfad zu den unkonvertierten Bildern angeben eventuell ueber Config ermitteln!
	print ("##############################################################")
	print ("#  Konvertierung der Bilder                                  #")
	print ("##############################################################")
	try:
		for f in os.listdir(pfadZuMedia):
			if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".JPG") or f.endswith(".JPEG") or f.endswith(".png") or f.endswith(".PNG"):
				txtInfo.insert("end",  "Bilddatei : " + f  + " wurde gefunden\n")
				app.update()
				tmpImage = Image.open(pfadZuMedia+f)
				mFilename, mFileextension = os.path.splitext(f)
				if not mFilename[0:2] =="K_":
					txtInfo.insert("end", "Konvertierung  von -> : " + mFilename + "\n")
					txtInfo.insert("end", "Bitte warten ....\n")
					txtInfo.see("end")
					app.update()
					#neue resize funktion:
					img = cv2.imread(pfadZuMedia+f,cv2.IMREAD_UNCHANGED)
					resizedImage = cv2.resize(img,size_810_x_520,interpolation = cv2.INTER_AREA)
					cv2.imwrite(pfadZuMedia+"K_{}.png".format(mFilename),resizedImage)
					#tmpImage.thumbnail((800,480))
					#tmpImage.save(pfadZuMedia+"K_{}.png".format(mFilename))
					# loeschen des Originals
					os.remove(pfadZuMedia+f)
				print (mFilename)
	except Exception as e:
		print("Fehler:", e)
		fehler = True
	print ("##############################################################")
	print ("#  Konvertierung der Filmdateien                             #")
	print ("##############################################################")
	try:	
		cmd=""
		f=""
		#txtInfo.insert("end",  "Suche Filme in : " + pfadZuMedia + "\n")
		print ("Suche Filme in : " , pfadZuMedia)
		for f in os.listdir(pfadZuMedia):
			dateiDest=""
			dateiSrc=""
			
			if f.endswith(".mp4"):
				txtInfo.insert("end", "Filmdatei : " + f + " wurde gefunden\n")
				app.update()
				mFilename, mFileextension = os.path.splitext(f)
				print(mFilename)
				if not mFilename[0:2]=="K_":
					#print ("Film gefunden: " ,f.replace(" ",""))
					txtInfo.insert("end", "Konvertierung  von -> : " + mFilename + "\n")
					txtInfo.insert("end", "Bitte warten ....\n")
					txtInfo.see("end")
					app.update()
					dateiDest = pfadZuMedia +"K_"+ mFilename.replace(" ","") + ".mp4"
					#txtInfo.insert("end",dateiDest)
					#app.update()
					dateiSrc = pfadZuMedia + f
					#print (dateiSrc)
				else:
					dateiDest=""
					dateiSrc=""
			if len(dateiSrc) > 4 and len(dateiDest) > 4 and len(str(breiteFilm)) > 0 and len(str(hoeheFilm)) > 0 :
				cmd = "ffmpeg -y -i " + dateiSrc + " -s " + str(breiteFilm) +":"+ str(hoeheFilm) +" "+ dateiDest
				try:
					subprocess.check_output(cmd.split(" "))
					#loeschen des Originals
					os.remove(pfadZuMedia+f)
				except Exception as e:
					txtInfo.insert("end","Fehler konvertierung des Films : " + e)
					fehler = True
			else:
				#print("kein mp4")
				pass
	except Exception as e:
		txtInfo.insert("end","Fehler dursuchen des Verzeichnisses: " + e)
	fehler = True
	txtInfo.insert("end","\n\n\n-----------------------------------------------------------------------")
	txtInfo.insert("end","\n\n## Konvertierung der Mediendateien erfolgreich beendet ##")
	txtInfo.insert("end","\n\n## Bitte beenden Sie das Programm ueber die Schaltflaeche Ende ##\n\n")
	txtInfo.see("end")
def main():	
	global modus 
	if len(sys.argv) > 1:
		modus = str(sys.argv[1])
	print("werde im modus : " , modus, " gestartet")	
	if modus == "del":
		getConfigs()
		deleteOldFiles()
		sys.exit()
	else:
		global txtInfo
		global app
		getConfigs()
		app = tkinter.Tk();
		app.title("Media Manager")
		btnStartConvert = tkinter.Button(app, text="Start",width=50, command=konvertiereMedien).grid(row=1, column=0,sticky='w')
		btnExitConvert = tkinter.Button(app, text="Ende",width=50, command=exitApp).grid(row=1, column=0,sticky='e')
		txtInfo = tkinter.Text(app,bg="#000",fg="#fff",width="105",font=("Arial", 14))
		txtInfo.grid(row=0, column=0,sticky='w')		
		txtInfo.insert("end", "\nDas Programm Media Manager konvertiert die Mediendateien, welche sich in dem  \n")
		txtInfo.insert("end", "Ordner Propharma befinden. Dies ist noeitg um die Medien dem Kundendisplay\n")
		txtInfo.insert("end", "im richtigen Format zur Verfuegung zu stellen.\n\n\n")
		txtInfo.insert("end", "Um den Konvertierungsvorgang zu starten die Schaltflaeche Start druecken \n\n")
		txtInfo.insert("end", "Die Schaltflaeche Ende beendet dieses Programm\n")
		# nötig für autoscroll:
		txtInfo.see("end")
		#if not fehler:
		#	renameFiles()
		#else:
		#	sys.exit()
		#if not fehler:
		#	konvertiereMedien()
			#sys.exit()
		#else:
		#	sys.exit()
		app.mainloop()
if __name__=="__main__":
	main()

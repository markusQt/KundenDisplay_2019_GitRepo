#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os 
import sys
import subprocess
import kundenDisplay_Video

#Vars:
size_810_x_520=(810,520)
breiteFilm=810
hoeheFilm=530
pfadZuMedia = ""
f=""
fehler = False
localfile="*"
remotehost=""
remotefile=""
user=""
host=""
ipRemote=""
port=""

def leereMedienordner():
	try:
		for f in os.listdir(pfadZuMedia):
			if os.path.isfile(pfadZuMedia+f):			
				os.remove(pfadZuMedia+f)
	except Exception as e:
		print("Fehler:", e)
		fehler = True

def renameFiles():
	try:
		for f in os.listdir(pfadZuMedia):
			if os.path.isfile(pfadZuMedia+f):			
				os.rename(pfadZuMedia+f,(pfadZuMedia+f).replace(" ",""))
	except Exception as e:
		print("Fehler:", e)
		fehler = True

def getConfigs():
	global remotehost
	global remotefile
	global user
	global ipRemote
	global pfadZuMedia
	global host
	global fehler
	configFile = open("config.txt","r")
	try:
		for line in configFile:
			if line.split("=")[0] == "host":
				host = line.split("=")[1].strip('\n').strip()
			if line.split("=")[0] == "remotefile":
				remotefile = line.split("=")[1].strip('\n').strip()
			if line.split("=")[0] == "user":
				user = line.split("=")[1].strip('\n').strip()
			if line.split("=")[0] == "ip_remote":
				ipRemote = line.split("=")[1].strip('\n').strip()
			if line.split("=")[0] == "destinationMedia":
				pfadZuMedia = line.split("=")[1].strip('\n').strip()
		print ("Remote IP:",ipRemote)
		print ("Remotefile:",remotefile)
		print ("user:",user)
		print ("PfadZuMedia:",pfadZuMedia)
	except:
		fehler = True

def copyFiles():
	global fehler
	global localfile
	global remotehost
	global remotefile
	global ipRemote
	global pfadZuMedia
	global host
	global user
	remotefile += "*"
	remotehost= user+"@"+ipRemote
	print (remotehost)
	print ("Remoteordner:" , remotefile)
	cmd ="scp "+ remotehost+":"+remotefile+ " "+pfadZuMedia
	print (cmd)
	try:
		subprocess.check_output(cmd.split(" "))
	except:
		fehler = True
		print ("#####################################################################")
		print ("#  Beim Kopieren ist ein Fehler aufgetreten Programm wird verlassen #")
		print ("#####################################################################")
		sys.exit()


def konvertiereMedien():
	global f
	global pfadZuMedia
	global fehler
	global size_810_x_520
	global breiteFilm
	global hoeheFilm

# richtigen Pfad zu den unkonvertierten Bildern angeben eventuell ueber Config ermitteln!
	print ("##############################################################")
	print ("#  Konvertierung der Bilder                                  #")
	print ("##############################################################")
	try:
		for f in os.listdir(pfadZuMedia):
			if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".JPG") or f.endswith(".JPEG") or f.endswith(".png") or f.endswith(".PNG"):
				tmpImage = Image.open(pfadZuMedia+f)
				mFilename, mFileextension = os.path.splitext(f)
				tmpImage.thumbnail(size_810_x_520)
				tmpImage.save(pfadZuMedia+"{}_810x520.png".format(mFilename))
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
		print ("Suche Filme in : " , pfadZuMedia)
		for f in os.listdir(pfadZuMedia):
			dateiDest=""
			dateiSrc=""
			
			if f.endswith(".mp4"):
				print(f)
				mFilename, mFileextension = os.path.splitext(f)
				print(mFilename)
				#print ("Film gefunden: " ,f.replace(" ",""))
				dateiDest = pfadZuMedia + mFilename.replace(" ","") + "_" + str(breiteFilm) + "x" + str(hoeheFilm) + ".mp4"
				print(dateiDest)
				dateiSrc = pfadZuMedia + f
				#print (dateiSrc)
			if len(dateiSrc) > 0 and len(dateiDest) > 0 and len(str(breiteFilm)) > 0 and len(str(hoeheFilm)) > 0 :
				cmd = "ffmpeg -y -i " + dateiSrc + " -s " + str(breiteFilm) +":"+ str(hoeheFilm) +" "+ dateiDest
				print(cmd)
				try:
					subprocess.check_output(cmd.split(" "))
					#loeschen des Originals
					os.remove(pfadZuMedia+f)
				except Exception as e:
					print("Fehler konvertierung des Films : ", e)
					fehler = True
			else:
				print("kein mp4")
	except Exception as e:
		print("Fehler dursuchen des Verzeichnisses: ", e)
		fehler = True


def main():
	global fehler
	print ("##############################################################")
	print ("# Starte Kopieren und Konvertieren der Mediendateien         #")
	print ("##############################################################")
	print ("##############################################################")
	print ("#  (1)Hole die Konfigurationseinstellungen                   #")
	print ("##############################################################")
	getConfigs()
	if fehler:
		print ("Fehler bei Ausfuehrung getConfigs")
		sys.exit()
	print ("##############################################################")
	print ("#  (2)Leere den Medienordner                                 #")
	print ("##############################################################")
	leereMedienordner()
	if fehler:
		print ("Fehler bei Ausfuehrung leereMedienordner")
		sys.exit()
	print ("##############################################################")
	print ("#  (3)Starte kopieren der Medien                             #")
	print ("##############################################################")
	print ("##############################################################")
	print ("#  Hinweis: Passwortloser Zugang muss per SSH bestehen       #")
	print ("##############################################################")
	copyFiles()
	if fehler:
		print ("Fehler bei Ausfuehrung copyFiles")
		sys.exit()
	print ("##############################################################")
	print ("#  Kopieren beendet                                          #")
	print ("##############################################################")
	#weil es immer Problemem mit Leerzeichen geben wird
	renameFiles()
	print ("##############################################################")
	print ("#  (4)Aufbereiten der Medien wird gesartet                   #")
	print ("##############################################################")
	konvertiereMedien()
	if fehler:
		print ("Fehler bei Ausfuehrung konvertiereMedien")
		sys.exit()
	print ("##############################################################")
	print ("# Aufbereiten der Medien beendet Kundendisplay wird gesartet #")
	print ("##############################################################")
	kundenDisplay_Video.startDisplay()
	sys.exit()
	
if __name__== "__main__":
	main()

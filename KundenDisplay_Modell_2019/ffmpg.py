#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess

ret = "-1"

def neustartSelect(i):
	if i == 1:
		print ("Das Programm ffmpeg kann nicht gestartet werden")
		print ("Programm beenden oder neu starten ? [j/n]?")
	else:
		print ("Programm beenden oder neu starten ? [j/n]?")	
	neustart = str(input())
	print("Neustart ?: ",neustart)
	if neustart == 'j' :
		ffmpeg()
	else:
		print ("Programm beendet !")
		quit(0)	

def ffmpeg():
	subprocess.call("clear",shell=True)
	print(	"###################################\n"
			"#Willkommen im Programm ffmpeg.py.#\n"
			"###################################")
	print("Das Programm dient dazu um Filmdateien zu modifizieren")
	print("\n\n\t (1) = Modus Film skalieren")
	print("\n\t Hinweis -> Filme für Raspberry immer 810 x 530 skalieren")
	print ("\nModus auswaehlen:\n")	

	modus = int(input())

	if modus == 1:
		print ("Modus Film skalieren aktiviert")
		print ("Eingabe Pfad der Quelldatei:")
		dateiSrc = 	str(input())		
		print ("Eingabe Pfad der Zieldatei ohne Dateiendung:")
		dateiDest = str(input())
		print ("Eingabe Skalierung Breite:")
		breite= str(input())
		print ("Eingabe Skalierung Hoehe:")
		hoehe=str(input())
		dateiDest = dateiDest+"_"+breite+"x"+hoehe+".mp4"
		if len(dateiSrc) > 0 and len(dateiDest) > 0 and len(breite) > 0 and len(hoehe) > 0 :
			cmd = "ffmpeg -i " + dateiSrc + " -s " + breite +":"+ hoehe +" "+ dateiDest
			print(cmd)
			try:
				# [global]wird benötigt um auf die globale Variable zgreifen zu können
				global ret
				ret = subprocess.check_output(cmd,shell=True)											
			except:					
				print ("Ausgabe: ", ret)
				neustartSelect(1)				
			if ret != "0":
				print ("Ausgabe: ", ret)
				neustartSelect(0)			
		else:
			print ("Ausgabe: ", ret)
			neustartSelect(1)
				
	else:
		print ("Modus ",str(modus), " noch nicht bekannt")
		neustartSelect(1)		
	neustartSelect(0)
	
ffmpeg()



#ls_output = subprocess.call('ls -l' ,universal_newlines = True , shell = True)


#Benutzer
USER="markuswi@"
#Rechner auf dem die Ressourcen liegen
RECHNER=192.168.215.110
#pfad zu den Bildern fuer Display
SRC_DIR="/home/markuswi/Kundendisplaybilder/*"
#pfad in welchen die Mediendateien abgelegt werden
TARGET_DIR="/home/apo/pgm/Kundendisplay/Displaybilder/"


echo "kopiere von "$SRC_DIR" nach "$TARGET_DIR 

scp $USER$Rechner":"$SRC_DIR $TARGET_DIR

exit 0

 

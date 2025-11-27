# 25_26_TP_Capteurs_Bus_Soltani-Menjli
## Réaliser par :
- Ezer SOLTANI
- Fakhri MENJLI
## Objectif de TP:
mettre en place l'ensemble des composants suivant:

![image1](architecture%20de%20syst%C3%A8me.PNG)

 ## TP 1:Bus I2C
 ### Capteur BMP280 :
1. les adresses I²C possibles pour ce composant:
   * 0x76 : lorsque SDO est connecté à la masse (GND).
   * 0x77 : lorsque SDO est connecté à la tension d'alimentation (VDD).
2. le registre et la valeur permettant d'identifier ce composant:
   * l'adresse 0xD0 et la valeur est 0x58.
3. le registre et la valeur permettant de placer le composant en mode normal
   * Le registre ctrl_meas à l'adresse 0xF4 et Les bits doivent être à "11" en Mode normale.
4. Registres d’étalonnage du composant :
   * Les valeurs d’étalonnage sont stockées dans les registres calib00 à calib25, correspondant aux adresses mémoire allant de 0x88 à 0xA1.
5. Registres contenant la température (et leur format) :Les données de température sont réparties sur trois registres :
   * temp_msb à l’adresse 0xFA : contient les bits 15 à 8,
   * temp_lsb à l’adresse 0xFB : contient les bits 7 à 0,
   * temp_xlsb à l’adresse 0xFC : contient les bits 7 à 4   
6. Registres contenant la pression (et leur format) :Les données de pression sont réparties sur trois registres :
   * press_msb à l’adresse 0xF7 : contient les bits 15 à 8,
   * press_lsb à l’adresse 0xF8 : contient les bits 7 à 0,
   * press_xlsb à l’adresse 0xF9 : contient les bits 7 à 4
7. les fonctions permettant le calcul de la température et de la pression compensées, en format entier 32 bits:

![image2](architecture%20de%20syst%C3%A8me.PNG)


import serial
import time

# Configuration du port série
# Remplacez '/dev/ttyS0' par '/dev/ttyAMA0' si nécessaire (selon votre Pi)
try:
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
except serial.SerialException:
    try:
        ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    except serial.SerialException:
        print("Erreur: Impossible d'ouvrir le port série. Vérifiez la configuration.")
        exit(1)

def send_command(command):
    # Nettoyer le buffer d'entrée avant d'envoyer
    ser.reset_input_buffer()
    
    # Envoyer la commande avec le caractère de fin de ligne '\n'
    full_command = command + '\n'
    ser.write(full_command.encode('utf-8'))
    
    # Lire la réponse (bloquant jusqu'au timeout ou fin de ligne)
    response = ser.readline().decode('utf-8').strip()
    return response

def get_temperature():
    resp = send_command("GET_T")
    print(f"Temperature: {resp}")
    return resp

def get_pressure():
    resp = send_command("GET_P")
    print(f"Pression: {resp}")
    return resp

def set_k(value):
    resp = send_command(f"SET_K={value}")
    print(f"Set K ({value}): {resp}")
    return resp

def get_k():
    resp = send_command("GET_K")
    print(f"Coefficient K: {resp}")
    return resp

def get_angle():
    resp = send_command("GET_A")
    print(f"Angle: {resp}")
    return resp

# Boucle de test principale
if __name__ == "__main__":
    print("Démarrage du test de communication STM32 <-> Raspberry Pi")
    print(f"Port utilisé : {ser.name}")
    
    try:
        while True:
            print("\n--- Nouvelle lecture ---")
            get_temperature()
            get_pressure()
            get_angle()
            get_k()

            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme.")
        ser.close()

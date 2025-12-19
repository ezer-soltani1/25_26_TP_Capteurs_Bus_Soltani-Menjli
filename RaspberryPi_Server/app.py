from flask import Flask, jsonify, request, abort, render_template
import serial
import time
import threading

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html')

# --- Serial Configuration ---
serial_lock = threading.Lock()
try:
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
except serial.SerialException:
    try:
        ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    except serial.SerialException:
        print("WARNING: Serial port not found. Running in simulation mode.")
        ser = None

def send_stm32_command(command):
    if ser is None:
        return "SIMULATION_ACK"

    with serial_lock:
        try:
            ser.reset_input_buffer()
            full_command = command + '\n'
            ser.write(full_command.encode('utf-8'))
            response = ser.readline().decode('utf-8').strip()
            return response
        except Exception as e:
            print(f"Serial Error: {e}")
            return "ERR_SERIAL"

# --- Variables Globales ---
temp_history = []
pres_history = []
current_scale = 1.0


@app.route('/temp/', methods=['POST'])
def create_temp():
    #Create POST temp/: Retrieve new temperature from STM32
    resp = send_stm32_command("GET_T")
    val = resp
    try:
        if "T=" in resp:
            val_str = resp.split('=')[1].split('_')[0]
            val = float(val_str)
    except:
        pass
    
    new_entry = {"id": len(temp_history), "value": val, "raw": resp, "timestamp": time.time()}
    temp_history.append(new_entry)
    return jsonify(new_entry), 201

@app.route('/temp/', methods=['GET'])
def get_all_temps():
    #Retrieve GET temp/: Return all previous temperatures
    return jsonify(temp_history)

@app.route('/temp/<int:id>', methods=['GET'])
def get_temp_by_id(id):
    #Retrieve GET temp/x: Return temperature #x
    if 0 <= id < len(temp_history):
        return jsonify(temp_history[id])
    abort(404)

@app.route('/temp/<int:id>', methods=['DELETE'])
def delete_temp_by_id(id):
    #Delete DELETE temp/x: Delete temperature #x
    if 0 <= id < len(temp_history):
        deleted = temp_history.pop(id)
        return jsonify(deleted), 200
    abort(404)

@app.route('/pres/', methods=['POST'])
def create_pres():
    #Create POST pres/: Retrieve new pressure from STM32
    resp = send_stm32_command("GET_P")
    val = resp
    try:
        if "P=" in resp:
            val_str = resp.split('=')[1].replace('Pa', '')
            val = float(val_str)
    except:
        pass
        
    new_entry = {"id": len(pres_history), "value": val, "raw": resp, "timestamp": time.time()}
    pres_history.append(new_entry)
    return jsonify(new_entry), 201

@app.route('/pres/', methods=['GET'])
def get_all_pres():
    #Retrieve GET pres/: Return all previous pressures
    return jsonify(pres_history)

@app.route('/pres/<int:id>', methods=['GET'])
def get_pres_by_id(id):
    #Retrieve GET pres/x: Return pressure #x
    if 0 <= id < len(pres_history):
        return jsonify(pres_history[id])
    abort(404)

@app.route('/pres/<int:id>', methods=['DELETE'])
def delete_pres_by_id(id):
    #Delete DELETE pres/x: Delete pressure #x
    if 0 <= id < len(pres_history):
        deleted = pres_history.pop(id)
        return jsonify(deleted), 200
    abort(404)

@app.route('/scale/', methods=['GET'])
def get_scale():
    #Retrieve GET scale/: Return scale (K)
    # Sync with STM32 to be sure
    resp = send_stm32_command("GET_K")
    return jsonify({"scale": current_scale, "stm32_resp": resp})

@app.route('/scale/<float:val>', methods=['POST'])
def update_scale(val):
    #Update POST scale/x: Change scale (K) for x
    global current_scale
    current_scale = val
    # Send to STM32
    cmd = f"SET_K={val:.2f}"
    resp = send_stm32_command(cmd)
    return jsonify({"scale": current_scale, "stm32_resp": resp})

@app.route('/angle/', methods=['GET'])
def get_angle():
    #Retrieve GET angle/: Return angle (temp x scale)
    resp = send_stm32_command("GET_A")
    return jsonify({"angle_raw": resp})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

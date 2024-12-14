import serial
import pynmea2
import logging
import time
import random

# Logging setup
timestamp = time.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(f"log_output_{timestamp}.txt"),
        logging.StreamHandler()
    ]
)

# GPS setup
GPS_PORT = "/dev/ttyAMA0"
GPS_BAUDRATE = 9600
try:
    gps_serial = serial.Serial(GPS_PORT, baudrate=GPS_BAUDRATE, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
except Exception as e:
    logging.error(f"Failed to initialize GPS: {e}")
    gps_serial = None

# INA219 simulation (as smbus unavailable in this environment)
def read_ina219():
    voltage = round(random.uniform(3.0, 12.0), 2)
    current = round(random.uniform(0.1, 2.0), 2)
    return f"Voltage: {voltage:.2f}V, Current: {current:.2f}mA"

# Simulated GPS data
def read_gps():
    if gps_serial:
        try:
            newdata = gps_serial.readline().decode('iso-8859-1')
            if newdata.startswith("$GNGGA"):
                newmsg = pynmea2.parse(newdata)
                return f"Latitude: {newmsg.latitude}, Longitude: {newmsg.longitude}, Altitude: {newmsg.altitude}m"
        except Exception as e:
            logging.error(f"GPS read error: {e}")
    # Simulated GPS data
    latitude = round(random.uniform(-90.0, 90.0), 6)
    longitude = round(random.uniform(-180.0, 180.0), 6)
    altitude = round(random.uniform(0, 5000), 2)
    return f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}m"

# Simulated DHT22 data
def read_dht22():
    temperature = round(random.uniform(-10.0, 40.0), 2)
    humidity = round(random.uniform(10.0, 90.0), 2)
    return f"Temperature: {temperature}C, Humidity: {humidity}%"

# Gyroscope and Accelerometer simulation
def read_gyro_accel():
    Ax = round(random.uniform(-2.0, 2.0), 2)
    Ay = round(random.uniform(-2.0, 2.0), 2)
    Az = round(random.uniform(-2.0, 2.0), 2)
    Gx = round(random.uniform(-250.0, 250.0), 2)
    Gy = round(random.uniform(-250.0, 250.0), 2)
    Gz = round(random.uniform(-250.0, 250.0), 2)
    return f"Gx: {Gx:.2f}°/s, Gy: {Gy:.2f}°/s, Gz: {Gz:.2f}°/s, Ax: {Ax:.2f}g, Ay: {Ay:.2f}g, Az: {Az:.2f}g"

# Placeholder for LoRa functionality
def setup_lora():
    logging.info("LoRa setup simulated. SX127x module unavailable.")

def transmit_lora(data):
    logging.info(f"Simulated LoRa transmission: {data}")

# Collect sensor data
def collect_data():
    gps_data = read_gps()
    dht_data = read_dht22()
    ina_data = read_ina219()
    gyro_accel_data = read_gyro_accel()
    return f"{gps_data}\n{dht_data}\n{ina_data}\n{gyro_accel_data}"

# Combined LoRa handling without threading
def lora_handler():
    logging.info("Starting simulated LoRa handler")
    counter = 0
    while True:
        # Simulate transmission every 5 seconds
        if counter % 5 == 0:
            data = collect_data()
            transmit_lora(data)

        # Simulate reception every 10 seconds
        if counter % 10 == 0:
            logging.info("Simulated data received: Hello, LoRa!")

        time.sleep(1)
        counter += 1

# Main execution
if __name__ == "__main__":
    try:
        setup_lora()

        # Run LoRa handler in the main loop to avoid threading
        lora_handler()

    except KeyboardInterrupt:
        logging.info("Terminating program")

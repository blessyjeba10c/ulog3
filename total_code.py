# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Example for using the RFM9x Radio with Raspberry Pi.
Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
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
    voltage = round(random.uniform()
    current = round(random.uniform()
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
    temperature = round(random.uniform()
    humidity = round(random.uniform()
    return f"Temperature: {temperature}C, Humidity: {humidity}%"

# Gyroscope and Accelerometer simulation
def read_gyro_accel():
    Ax = round(random.uniform()
    Ay = round(random.uniform()
    Az = round(random.uniform()
    Gx = round(random.uniform()
    Gy = round(random.uniform()
    Gz = round(random.uniform()
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

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)
    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        display.text('RX: ', 0, 0, 1)
        display.text(packet_text, 25, 0, 1)
        time.sleep(1)

    if not btnA.value:
        # Send Button A
        display.fill(0)
        button_a_data = bytes("Button A!\r\n", "utf-8")
        rfm9x.send(button_a_data)
        display.text('Sent Button A!', 25, 15, 1)
    elif not btnB.value:
        # Send Button B
        display.fill(0)
        button_b_data = bytes("Button B!\r\n", "utf-8")
        rfm9x.send(button_b_data)
        display.text('Sent Button B!', 25, 15, 1)
    elif not btnC.value:
        # Send Button C
        display.fill(0)
        button_c_data = bytes("Button C!\r\n", "utf-8")
        rfm9x.send(button_c_data)
        display.text('Sent Button C!', 25, 15, 1)
    display.show()
    time.sleep(0.1)

 
 

import serial
from time import sleep
import requests



ser = serial.Serial("/dev/ttyS0", 9600)
ENDPOINT = "http://10.0.0.120:3000/name"

while True:
    received_data = ser.read()
    sleep(0.3)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    print(received_data)
    
    received_data = received_data.decode()
    
    split_data = received_data.split('$')
    
    
    
    try:
        gnrmc_string = split_data[4]
    except IndexError:
        continue
    
    gnrmc_list = gnrmc_string.split(",")
    
    if gnrmc_list[0] != "GNRMC":
        continue


    latitude = gnrmc_list[3]
    longitude = gnrmc_list[5]


    data = {"longitude":longitude,
            "latitude":latitude}

    send_data = requests.post(url=ENDPOINT, json=data)
    
    print(send_data.text)
    
    
    
    
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

    latitude_data = gnrmc_list[3]
    latitude_dir = gnrmc_list[4]
    longitude_data = gnrmc_list[5]
    longitude_dir = gnrmc_list[6]

    print(latitude_data)
    print(longitude_data)

    latitude_data_decimal = float(latitude_data[2:])
    longitude_data_decimal = float(longitude_data[3:])

    latitude_data_int = int(float(latitude_data)/100)
    longitude_data_int = int(float(longitude_data)/100)

    # print(latitude_data_int)
    # print(longitude_data_int)


    # print(latitude_data_decimal)
    # print(longitude_data_decimal)

    latitude = latitude_data_int + (latitude_data_decimal/60)
    longitude = longitude_data_int + (longitude_data_decimal/60)

    if latitude_dir == "N":
        latitude = +latitude
    else:
        latitude = -latitude

    if longitude_dir == "E":
        longitude = +longitude
    else:
        longitude = -longitude

    print(latitude)
    print(longitude)

    data = {"lat":latitude,
            "lng":longitude}

    send_data = requests.post(url=ENDPOINT, json=data)
    
    print(send_data.text)
    
    
    
    
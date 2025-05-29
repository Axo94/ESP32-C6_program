# boot.py
# Inicializácia a pripojenie na WiFi pre ESP32 (MicroPython)
import time
import network
import webrepl
 
#Premenná pre wi-fi pripojenie
WIFI_SSID = 'INSPIREA'
WIFI_PASSWORD = 'Creative@2020'
 
# Premenné pre statickú IP adresu
# Uprav podľa svojej siete
STATIC_IP = '10.70.73.202'
SUBNET_MASK = '255.255.255.0'
GATEWAY = '10.70.73.1'
DNS = '8.8.8.8'
 
def connect_wifi(ssid, password, ip, subnet, gateway, dns):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Nastavenie statickej IP adresy
    wlan.ifconfig((ip, subnet, gateway, dns))
    
    print('Pripájam sa na WiFi...')
    wlan.connect(ssid, password)
    timeout = 20  # max 20 sekúnd
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
    if wlan.isconnected():
        print('Pripojené:', wlan.ifconfig())
    else:
        print('Nepodarilo sa pripojiť na WiFi.')
 
# Pripojenie na WiFi pri štarte
connect_wifi(WIFI_SSID, WIFI_PASSWORD, STATIC_IP, SUBNET_MASK, GATEWAY, DNS)
 
# Spustenie WebREPL pre programovanie cez WiFi
webrepl.start()
 
 

import machine
import onewire
import ds18x20
import time
from machine import Pin
import neopixel
import time
import utime
import os

np = neopixel.NeoPixel(Pin(8), 1)
# Pripojenie dátového pinu (žltý) na GPIO10
dat = machine.Pin(1)

# Inicializácia OneWire a DS18B20
ow = onewire.OneWire(dat)
ds = ds18x20.DS18X20(ow)

# Vyhľadanie senzorov na zbernici (môže byť viac)
roms = ds.scan()
print('Nájdené senzory:', roms)
teploty = []
# Nastavte si limitnú teplotu podľa potreby
LIMIT_TEMP = 30.0  # napríklad 30°C

while True:
    for i in range(5):
        ds.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            temp = ds.read_temp(rom)
            print(temp, '°C')
            # Získaj aktuálny čas v čitateľnom tvare (YYYY-MM-DD HH:MM:SS)
            timestamp = utime.time()
            t = utime.localtime(timestamp)
            timestr = f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"
            # Skontroluj počet riadkov v súbore a ak je viac ako 400, vymaž ho
            try:
                with open("heatstat.txt", "r") as stat:
                    lines = stat.readlines()
                if len(lines) > 1200:
                    with open("heatstat.txt", "w") as stat:
                        stat.write("")
            except OSError:
                pass  # súbor ešte neexistuje
            with open("heatstat.txt", "a") as stat:
                if temp > LIMIT_TEMP:
                    stat.write("Teplota bola prekrocena:  ")
                    stat.flush()
                    os.sync()
                stat.write(f"{timestr};{temp:.2f} °C\n")
                stat.flush()
                os.sync()
            if temp > LIMIT_TEMP:
                print('Teplota prekročila limit:', temp, '°C')
                
                np[0] = (0, 255, 0)  # GRB: zelená = zle (prekročený limit)
                np.write()
            else:
                np[0] = (255, 0, 0)  # GRB: červená = dobre (v norme)
                np.write()
        time.sleep(3)

# pamata si to 1h a potom sa zmaze a zapisuje nanovo

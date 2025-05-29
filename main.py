from machine import Pin
import neopixel
import time

np = neopixel.NeoPixel(Pin(8), 1)

# Funkcia na plynulý prechod medzi dvoma farbami
def fade_color(start, end, steps, delay=0.01):
    for i in range(steps):
        r = int(start[0] + (end[0] - start[0]) * i / steps)
        g = int(start[1] + (end[1] - start[1]) * i / steps)
        b = int(start[2] + (end[2] - start[2]) * i / steps)
        np[0] = (r, g, b)
        np.write()
        time.sleep(delay)

# Zoznam farieb na prechádzanie (červená, zelená, modrá, späť na červenú)
colors = [
    (255, 0, 0),   # červená
    (0, 255, 0),   # zelená
    (0, 0, 255),   # modrá
    (255, 0, 0)    # späť na červenú
]

while True:
    for i in range(len(colors) - 1):
        fade_color(colors[i], colors[i+1], steps=100, delay=0.01)


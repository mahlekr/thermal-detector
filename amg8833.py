import os
import math
import time
import busio
import board
import adafruit_amg88xx
import numpy as np
import pygame
from scipy.interpolate import griddata
from pygame import mixer
from colour import Color

# sensor input
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

#low range of the sensor (this will be blue on the screen)
MINTEMP = 26.

#high range of the sensor (this will be red on the screen)
MAXTEMP = 32.

#how many color values we can have
COLORDEPTH = 1024

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

#initialize the sensor
sensor = adafruit_amg88xx.AMG88XX(i2c)

# pylint: disable=invalid-slice-index
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]
# pylint: enable=invalid-slice-index

#sensor is an 8x8 grid so lets do a square
height = 240
width = 240

#the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

displayPixelWidth = width / 30
displayPixelHeight = height / 30

lcd = pygame.display.set_mode((width, height))
lcd.fill((255, 0, 0))

# set the pygame windows name
pygame.display.set_caption('temp.')

# create a font object
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf',20)

pygame.display.update()
pygame.mouse.set_visible(False)

lcd.fill((0, 0, 0))
pygame.display.update()

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
    #let the sensor initialize
    time.sleep(.1) 

    # 8x8 array
    arr = np.array(amg.pixels)
    temp= arr.max()
    print('temperature:', temp)

    # play sound
    if int(temp) in range(28,32):
        mixer.init()
        mixer.music.load('OK.mp3')
        mixer.music.play()
    elif int(temp) in range(32,42):
        mixer.init()
        mixer.music.load('WARN.mp3')
        mixer.music.play()
    else:
        print ("Temperature is NOT detected")

    #read the pixels
    pixels = []
    for row in sensor.pixels:
        pixels = pixels + row
    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

    #perform interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')

    #draw everything
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)],
                             (displayPixelHeight * ix, displayPixelWidth * jx,
                              displayPixelHeight, displayPixelWidth))

    # display text
    if int(temp) in range(28,32):
        text = font.render('OK', False, (255,255,255))
        lcd.blit(text,(0,0))
    elif int(temp) in range(32,42):
        text = font.render('WARN', False, (255,0,0))
        lcd.blit(text,(0,0))     

    pygame.display.update()

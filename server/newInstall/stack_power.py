#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

#Met en place la numerotation electronique de la puce
GPIO.setmode(GPIO.BCM)

#Desactive les warnings
GPIO.setwarnings(False)

#Pinlist
map_stack_gpio = {1:18,2:25,3:12,4:21}

#Configure les pins precises en mode sortie
for k1 in map_stack_gpio:
	GPIO.setup(map_stack_gpio[k1], GPIO.OUT)

#Allume une stack/Envoie le courant sur un pin
def powerup_stack(n):
	GPIO.output(map_stack_gpio[n], GPIO.LOW)
	#print ("ON")

#Eteint une stack/Bloque le courant sur un pin
def powerdown_stack(n):
	GPIO.output(map_stack_gpio[n], GPIO.HIGH)
	#print ("OFF")

#Purge les ressources utilisees
def cleanup():
	GPIO.cleanup()

# Powerdown stacks
for k in map_stack_gpio:
	powerdown_stack(k)
	

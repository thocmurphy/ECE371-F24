"""
Blinks the Pico LTE's on board LED with 2.5 second frequency
"""

from machine import Pin, Timer

USER_LED = Pin(22, mode=Pin.OUT)

timer = Timer()

def blink(timer):
    USER_LED.toggle()
    
    
timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)

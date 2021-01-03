from machine import Pin
import time
relay_in = Pin(13, Pin.OUT)
button = Pin(12, Pin.IN, Pin.PULL_UP)


def open_lamp(pin):
    if pin.value() == 0:
        return
    while pin.value() == 1:
        time.sleep_ms(100)
    relay_in.value(not relay_in.value())


# IRQ_RISING  上升沿触发
# IRQ_FALLING 下降沿触发
button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=open_lamp)

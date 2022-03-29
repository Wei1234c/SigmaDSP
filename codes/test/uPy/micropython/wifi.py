import config
import network

import led



# WiFi network _________________________
def wait_for_wifi():
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')

        sta_if.active(True)
        sta_if.connect(config.SSID, config.PASSWORD)

        while not sta_if.isconnected():
            pass

    print('Network configuration:', sta_if.ifconfig())

    led.blink_on_board_led(times = 2)

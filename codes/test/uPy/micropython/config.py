import sys


IS_MICROPYTHON = sys.implementation.name == 'micropython'

# Hardware **********************
ON_BOARD_LED_PIN_NO = 5
ON_BOARD_LED_HIGH_IS_ON = False
LED_ON_ms = 3
LED_OFF_ms = 0

# Avoid some pins of ESP32,
# see: https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
I2C_SCL_PIN_ID = 18
I2C_SDA_PIN_ID = 5
RESET_PIN_ID = 19

# WiFi **********************
SSID = 'SSID'
PASSWORD = 'PASSWORD'

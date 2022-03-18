# SigmaStudio TCPIP Channel Tools Box
![](https://raw.githubusercontent.com/Wei1234c/TCPi/master/jpgs/Sigma%20TCPi%20server.png)
## What is this?
- This is a Python package, with which you can:
    - Remotely control SigmaDSP through TCP/IP channel.
        - With SigmaStudio or Python program.
    - Use ESP32 / PC as a client.
    - Use ESP32 / PC as the server. 
    - Can also **read data from** SigmaDSP over TCP/IP channel.
    - Can read/write **EEPROM**.
    

## Why?
- I was [playing with SigmaDSP (ADAU1701/ADAU1401)](https://github.com/Wei1234c/SigmaDSP), and often need to switch between USBi and [FTDI FT232H](https://www.google.com/search?q=ftdi+ft232h&sxsrf=APq-WBvh8jByLE89c5v9AHCrUAZXqxOAmA:1646325613903&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjCrZrrsKr2AhVL05QKHeoaD4gQ_AUoAXoECAEQAw&biw=1396&bih=585&dpr=1.38).
- With SigmaDSP TCP/IP channel, SigmaStudio and Python program can share the same channel to access SigmaDSP, no more switching.
- Remote access is always a huge advantage.

## Design and Features
- Coverage of SigmaDSP's memory space:
    - Can access data of program RAM, parameter RAM, and also **EEPROM**, just assign the address to read/write.
- Can also read data from SigmaDSP
    - Not only writing data to, but can also **read data from** SigmaDSP via TCP/IP channel.
- A client can be:
    - A PC running SigmaStudio
    - A PC running Python program
    - An ESP32 running MicroPython
- A server can be:
    - A PC with Python enviornment
        - Using USB-I2C converter (like FTDI FT232H) to access SigmaDSP.
        - [Using USBi as an USB-I2C converter](https://github.com/Wei1234c/USBi) to access SigmaDSP.        
    - An ESP32 with MicroPython enviornment 
        - Using its I2C port to access SigmaDSP.  


## How to use it
- For using ESP32 as the server:
    - Download [TCPi_uPy.rar](https://github.com/Wei1234c/TCPi/raw/master/notebooks/tools/TCPi_uPy.rar).
    - Unzip it and edit the following items in file `config.py`:
        - LED, on your ESP32 module:
            - ON_BOARD_LED_PIN_NO, ON_BOARD_LED_HIGH_IS_ON
        - I2C connection:
            - I2C_SCL_PIN_ID, I2C_SDA_PIN_ID: with which pins the ESP32 should use to connect with ADAU1701.
            - Avoid some pins of ESP32, see [ESP32 GPIO guide](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/).
        - WiFi:
            - SSID, PASSWORD 
    - Upload all file to ESP32.
    - In ESP32's terminal interface, type `import test_tcpi_upy`, it will show it's IP when WiFi connection is established.
        - The default port number is 8086.
        - You can write `import test_tcpi_upy` into file `main.py`, so it will run as a Sigma TCP/IP channel server after each boot.
    - Follow [AD's instruction](https://wiki.analog.com/resources/tools-software/sigmastudio/usingsigmastudio/tcpipchannels_) to connect to the server.
- Please also see [here](https://github.com/Wei1234c/TCPi/tree/master/notebooks/Functional%20test) and [here](https://github.com/Wei1234c/TCPi/tree/master/codes/test/pc) for examples.  


## Test Results
- [Control SigmaDSP with SigmaStudio through TCP/IP Channel, using ESP32 as the server](https://youtu.be/fecBbvJBepI) 
- [Control SigmaDSP with Python program through TCP/IP Channel, using ESP32 as the server](https://youtu.be/0D95nNcjJ2Q)
    
## Supported Chips
- ADAU1701
- ADAU1702
- ADAU1401
- ADAU1401A

## Limitations
- Not high speed, obvious latency. 
- Need more memory to accommdate the data SigmaStudio uploads all at once. ESP32 with 8MB PSRAM is preferred.

## Dependencies
- [Utilities](https://github.com/Wei1234c/Utilities)
### SigmaDSP Toolbox Proxy


[![SigmaDSP PC Control Test](https://raw.githubusercontent.com/Wei1234c/SigmaDSP/master/jpgs/demo_equip_setup.png)](https://youtu.be/XHlZtDsa4oE)     


### What is This?
- This is a Python package, which...:
    - Control SigmaDSP (e.g. ADAU1401/ADAU1701) from PC (with an USB-I2C converter, e.g. FTDI FT232H) by:
        - Reads the XML file of SigmaStudio project and generates proxy objects.
        - These objects represent SigmaStudio Toolbox algorithms in your project, and offer functions like set_frequency, set_dB, set_coefficients... correspondingly.
        
        
### Why This?
- ADAU1401/ADAU1701 are precious for DSP tasks, but I would like to tune filter coefficients automatically, therefore need to control DSP functions on the fly.
- SigmaStudio supports scripting from Python, see [SigmaStudio Scripting from Python](https://wiki.analog.com/resources/tools-software/sigmastudio/usingsigmastudio/scripting/python). However, I would prefer that the same package can be used on Windows / Linux, PC / RPi / ESP32 without modification. 

### Design and Features  
- PC control: Can control DSP hardware's behavior from PC, so resources (like Python, AI) are available for filter tuning.
- Coverage of SigmaStudio Toolbox: one-to-one class mapping for each SigmaStudio Toolbox algorithm (most of them are not tested yet though).
- Easy to use: only the XML file of SigmaStudio project is required. "Factory" will render every thing you need.
- Serialization: 
    - Load from:  
        - files: 
            - Binary (bytearray) file
            - SigmStudio text files (e.g. NumBytes_IC_1.dat, TxBuffer_IC_1.dat)
            - SigmaStudio project.xml
        - EEPROM
    - Save to:   
        - files: 
            - Binary (bytearray) file
            - Text file (converted from binary file)
        - EEPROM  
        
### Supported Chips
- ADAU1701
- ADAU1702
- ADAU1401
- ADAU1401A

### Documents  

- [Object Hierarchy](https://wei1234c.blogspot.com/2022/03/sigmadsp-agents-object-hierarchy.html)  
 
- [ADAU1401 Functional Test](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/ADAU1401%20Functional%20Test.ipynb)  

- [ADAU1401.Control Functional Test](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/ADAU1401.Control%20Functional%20Test.ipynb)  

- [ADAU1401 RAM / EEPROM Functional Test](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/ADAU1401%20RAM%20EEPROM%20Functional%20Test.ipynb)  

- [Message Functional Test](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/Message%20Functional%20Test.ipynb)  

- [XML Related Classes Functional Test](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/XML%20Related%20Classes%20Functional%20Test.ipynb)  

- [Factory Functional Test](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/Factory%20Functional%20Test.ipynb)  

- [Cell Functional Test](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/Cell%20Functional%20Test.ipynb)  

- [Functional Demostration](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/Functional%20Demostration.ipynb) 


### Dependencies

- [Signal_Generators](https://github.com/Wei1234c/Signal_Generators)  

- [Bridges](https://github.com/Wei1234c/Bridges)  

- [Utilities](https://github.com/Wei1234c/Utilities)

- [FTDI FT232H](https://www.google.com/search?q=ftdi+ft232h&sxsrf=APq-WBvh8jByLE89c5v9AHCrUAZXqxOAmA:1646325613903&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjCrZrrsKr2AhVL05QKHeoaD4gQ_AUoAXoECAEQAw&biw=1396&bih=585&dpr=1.38)  

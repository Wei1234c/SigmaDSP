### SigmaDSP tools box.


[![SigmaDSP PC Control Test](https://raw.githubusercontent.com/Wei1234c/SigmaDSP/master/jpgs/demo_equip_setup.png)](https://youtu.be/XHlZtDsa4oE)     



### Why This?
  ADAU1401/ADAU1701 are precious for DSP tasks, but I would like to tune filter coefficients automatically, therefor need to control DSP funcitons on the fly.  

### Design and Features  
- PC control: Can control DSP hardware's behavior from PC, so resources (like Python, AI) are available for filter tuning.
- Coverage of SigmaStudio Toolbox: one-to-one class mapping for each SigmaStudio Toolbox algorithm (most of them are not tested yet though).
- Easy to use: only the XML file of SigmaStudio project is required. "Factory" will render every thing you need.
- Serialization: 
    - Load from:  
        - files: 
            - Binary (bytearray) file
            - SigmStudio text files (eg. NumBytes_IC_1.dat, TxBuffer_IC_1.dat)
            - SigmaStudio project.xml
        - EEPROM
    - Save to:   
        - files: 
            - Binary (bytearray) file
            - Text file (converted from binary file)
        - EEPROM  
        
### Supported Chips
- ADAU1701
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
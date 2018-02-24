# G-Code-Injector
G-Code postprozessor tool for Slic3r generated G-Code

## How to use it?

### Add "Before layer change G-Code" in Slic3r
1. Go to "Printer Settings" -> "Custom G-Code" -> "Before layer change G-Code"
2. Add ";LAYER:[layer_num]"
3. Save modified Printer Settings
4. Slice your model
5. Save the .gcode

### Modify your .gcode with G-Code-Injector Python Script
1. use the python with arguments as shown below

Syntax:  
  -s   STARTVALUE  -  start value, for example 190 when creating a heattower  
  -e   ENDVALUE    -  end value, for example 240 when creating a heattower  
  -i   INCREMENT   -  increment value, for example 5 when creating a heattower  
  -sl  STARTLAYER  -  start layer, first Layer for injection, for example 10  
  -l   LAYERCOUNT  -  layer count, change value every x Layer  
  -g   GCODE       -  G-Code that will be injected, for example M104 when creating a heattower  
  -p   PARAMETER   -  parameter that will be injected, for example S when creating a heattower  
  -f   GCODEFILE   -  the .gcode file to process  
  


#### Example Nr 1:
./GC-Injector.py -s 190 -e 250 -i 5 -sl 20 -l 25 -g M104 -p S -f TempTower.gcode

It will add to .gcode file:  
@Layer 20 : M104 S195  
@Layer 45 : M104 S200  
@Layer 70 : M104 S205  
....  

Temperatur will first be modified at layer 20 to 195°, then temperatur will increase 5° every 25 layer.

#### Example Nr 2:
./GC-Injector.py -s 1000 -e 5000 -i 500 -sl 10 -l 30 -g M201 -p X -f ACC_Tower.gcode

It will add to .gcode file:  
@Layer 20 : M201 X1500  
@Layer 45 : M201 X2000  
@Layer 70 : M201 X2500  
....

Acceleration for X-axis (Repetier style G-Code) will first be modified at layer 10 to ACC 1500, then acceleration will increase 500 every 30 layer.

Repeat with Y axis if you want.


#### FAQ:
1. If you receice a "permission denied" message, try "chmod u+rx GC_Injector.py"


------------

#### credits:
based on script by quirxi
https://www.thingiverse.com/thing:2615842

#!/usr/bin/env python

import argparse, sys

# parse arguments
parser = argparse.ArgumentParser(description="Postprocess a gcode file exported from Slic3r.")
requiredData = parser.add_argument_group('required arguments')
requiredData.add_argument('-s', '--startValue', type=int, help="start Value, for example 190 when creating a heattower", required=True)
requiredData.add_argument('-e', '--endValue',   type=int, help="end Value, for example 240 when creating a heattower", required=True)
requiredData.add_argument('-i', '--increment',  type=int, help="increment Value, for example 5 when creating a heattower", required=True)
requiredData.add_argument('-sl', '--StartLayer', type=int, help="StartLayer, first Layer for injection, for example 10", required=True)
requiredData.add_argument('-l', '--LayerCount', type=int, help="LayerCount, change value every x Layer", required=True)
requiredData.add_argument('-g', '--GCode', type=str, help="G-Code that will be injected, for example M104 when creating a heattower", required=True)
requiredData.add_argument('-p', '--Parameter', type=str, help="Paramter that will be injected, for example S when creating a heattower", required=True)
requiredData.add_argument('-f', '--GCodeFile', help="The .gcode file to process.", required=True)
requiredData.add_argument('-b', '--Begin', help="Select Start Layer", required=False)
args = parser.parse_args()

# create output filename
outFile="OUT_" + args.GCodeFile;

# show parsed arguments
print("\nG-Code-Injector\n")
print("startValue: {}".format(args.startValue))
print("endValue:   {}".format(args.endValue))
print("increment:  {}".format(args.increment))
print("StartLayer:  {}".format(args.StartLayer))
print("LayerCount:  {}".format(args.LayerCount))
print("GCode:  {}".format(args.GCode))
print("Parameter:  {}".format(args.Parameter))
print("GCodeFile: \"{}\"".format(args.GCodeFile))
print("outFile: \"{}\"".format(outFile))
print("")

# parse gcode file
try:
    gcodeInput = open(args.GCodeFile, 'r')
    gcodeOutput = open(outFile, 'w')
    currentLayerNr=args.StartLayer;
    currentValue=args.startValue
    layerList=[];
    step=args.increment;
    
    # depending if values should rise or decrease in layers we need to make sure we get the direction of step right:
    if args.startValue < args.endValue:
        step = abs(step)
    else:
        step = abs(step) * -1
    # print("step: {}".format(step))
    
    # make the list of layers where acceleration needs to be changed        
    for i in range(args.startValue,args.endValue+step,step):
        #print("currentValue: {}".format(currentValue));
        layerList.append(";LAYER:" + str(currentLayerNr) + '\n')
        #print("-> layerLine: \"{}\"".format(layerList[-1]))
        currentLayerNr+=args.LayerCount
        currentValue+=step
        
    currentLayer=args.StartLayer;
    currentValue=args.startValue
    currentLayerStr=layerList.pop(0)

    for LINE in gcodeInput:
        gcodeOutput.write(LINE)
        if currentLayerStr != "" and LINE.find(currentLayerStr)!=-1:
            # beginning from layer 10 insert after each xx (LayerCount) layer the right acceleration gcode ( M201 an M202 ).
            gcodeOutput.write(args.GCode + " " + args.Parameter + str(currentValue) + '\n')
            print("-> " + args.GCode + " " + args.Parameter + str(currentValue) + " " + str(currentLayerStr))
            currentValue+=step
            if layerList: 
                currentLayerStr=layerList.pop(0)
            else:
                currentLayerStr = "";
except (IOError, OSError) as e:
    print ("I/O error({0}) in \"{1}\": {2}".format(e.errno, e.filename, e.strerror))
except: #handle other exceptions such as attribute errors
   print ("Unexpected error:", sys.exc_info()[0])
else:
    gcodeInput.close()
    gcodeOutput.close()

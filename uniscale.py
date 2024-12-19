#Universal Scale will allow you to scale your object regardless the unit. 
#(Ex. if you want an object to be 6 ft but you're in cm on Maya, this tool will automatically scale your object to the 6 ft equivalent in cm (182.88 cm) ||

#Currently a WIP and is meant to be a continuation of Simple Rigging Automation Pt. 2

import maya.cmds as cmds 

#Learning how to do classes at the moment and implementing it into the window, need to look further into the meaning of (object) 
class UnitsToUnits(object):
    # Window construction
    def conversion(conv):
        conv.window = 'convertWindow'
        conv.title = 'Unit Scale Window'   
        conv.size = (400, 350) 
        conv.createUnitWindow()  
        
    # Window creation 
    def createUnitWindow(conv):
        if cmds.window(conv.window, exists=True):
            cmds.deleteUI(conv.window, window=True)
            
        conv.window = cmds.window(conv.window, title=conv.title, widthHeight=conv.size)
        conv.button = cmds.button()
        cmds.showWindow(conv.window)
        
# Create an instance of the UnitsToUnits class
unitscale = UnitsToUnits()
unitscale.conversion()

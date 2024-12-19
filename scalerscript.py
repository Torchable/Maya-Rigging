## Simple Rigging Automation Pt. 2
# Scales objects in the GEO_GRP category of the automaterig Pt. 1. Would be used if your character is not in scale with how you wanted it to be. 
# Colin Cheng
#
# Input: Scale Size 
# Output: Uniform scale at a specific number
#

import maya.cmds as cmds 

def scaler():
    inp = int(input())
    scalechar = cmds.ls('*_GEO_GRP')

    cmds.xform(scalechar, worldSpace=True, pivots=(0,0,0))
    cmds.xform(scalechar, scale=(inp, inp, inp))

scaler()

# Simple Rigging Automation Pt. 1
# Creates necessary groups for starting the rigging process 
# Colin Cheng
#
# Input: Prefix name 
# Output: Multiple categorized groups for beginning the rigging process 
#
# 1/20/24

import maya.cmds as cmds

def riggroups(groups):
#User input for prefix name
    x = cmds.promptDialog(title= 'RIG Group Setup', message='Insert Prefix Name')
    if x == 'Confirm':
        x = cmds.promptDialog(query = True, text = True)
        
    elif x == 'dismiss':
        return
    
#Checks if a rig group already exists and deletes it
    rigListexist = cmds.ls('*_RIG')
    if len (rigListexist) > 0:
        cmds.delete(rigListexist)
    groups(x)
        
#Creation of groups
def groups(x):
    CTRL = cmds.group(em=True, n= x + '_CTRL_GRP')
    GEO = cmds.group(em=True, n= x + '_GEO_GRP')
    JNT = cmds.group(em=True, n= x + '_JNT_GRP')
    notouch = cmds.group(em=True, n= x + '_notouch_GRP')
    DEF = cmds.group(em=True, n= x + '_DEF_GRP')
    IK = cmds.group(em=True, n= x + '_IK_GRP')

#Creation of rig group
    RIG = cmds.group(CTRL, GEO, JNT, notouch, DEF, IK, n= x + '_RIG')

riggroups(groups)

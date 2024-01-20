# Simple Rigging Automation Pt. 1
# Creates Necessary groups for starting the rigging process 
# Colin Cheng
#
# Input: Prefix name 
# Output: Multiple categorized groups for beginning the rigging process 
#
# 1/20/24

import maya.cmds as cmds

def main():
#User input for prefix name
    x = cmds.promptDialog(title= 'RIG Group Setup', message='Insert Prefix Name')
    if x == 'Confirm':
        x = cmds.promptDialog(query = True)

    global RIG
    
#Ensures only one RIG group is created
    if cmds.objExists(RIG):
        cmds.delete(RIG)
        
#Creation of groups
    CTRL = cmds.group(em=True, n= x + '_' + 'CTRL_GRP')
    GEO = cmds.group(em=True, n= x + '_' + 'GEO_GRP')
    JNT = cmds.group(em=True, n= x + '_' + 'JNT_GRP')
    notouch = cmds.group(em=True, n= x + '_' + 'notouch_GRP')
    DEF = cmds.group(em=True, n= x + '_' + 'DEF_GRP')
    IK = cmds.group(em=True, n= x + '_' + 'IK_GRP')

#Creation of rig group
    RIG = cmds.group(CTRL, GEO, JNT, notouch, DEF, IK, n= x + '_' + 'RIG')

main()

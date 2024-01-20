import maya.cmds as cmds

#user input for prefix name
x = input()

#creation of groups
CTRL = cmds.group(em=True, n= x + '_' + 'CTRL_GRP')
GEO = cmds.group(em=True, n= x + '_' + 'GEO_GRP')
JNT = cmds.group(em=True, n= x + '_' + 'JNT_GRP')
notouch = cmds.group(em=True, n= x + '_' + 'notouch_GRP')
DEF = cmds.group(em=True, n= x + '_' + 'DEF_GRP')
IK = cmds.group(em=True, n= x + '_' + 'IK_GRP')

#creates rig group
RIG = cmds.group(CTRL, GEO, JNT, notouch, DEF, IK, n= x + '_' + '_RIG')
import maya.cmds as cmds 

def directconnect():
    selecting = cmds.ls(selection=True)
    trs = ['.translate', '.rotate', '.scale']
    for i in range(3):
        connect_1 = selecting[0] + trs[i]
        connect_2 = selecting[1] + trs[i]   
        connectattr_trs = cmds.connectAttr(connect_1, connect_2, force= True)

directconnect()

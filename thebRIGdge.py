6# The bRIGdge 
# by Colin Cheng 
# 
#  The bRIGdge is a window I created that saves time creating commonly used custom controls for your rig.
# To use, drag the .py file into your Maya file and it will run.

import maya.cmds as cmds
import maya.mel as mm


#offset group attribute 
def createoffset():
    if cmds.checkBox('createoffset', query=True, v=True):
        cmds.group()

#gimbal lock fix attribute
def gimbalfix():
    if cmds.checkBox('gimbal', query=True, value=True):
        cmds.addAttr(ln='RotationOrder', k = True, attributeType= 'enum', en='xyz:yzx:zxy:xzy:yxz:zyx')
        cmds.connectAttr('.RotationOrder', '.rotateOrder')

#Creates an FK IK Switch with selected control
def switch(createoffset):
    createoffset = cmds.checkBox('createoffset', query=True, v=True)
    switchlist = ['.translateX','.translateY','.translateZ','.rotateX','.rotateY','.rotateZ','.scaleX','.scaleY','.scaleZ','.visibility']
    if cmds.checkBox('fkikswitch', query = True, v= True):
        if createoffset == False:
            cmds.warning('It is recommended that you have "Create offset Group" turned on when using this feature')
        cmds.addAttr(ln='FKIKSwitch', niceName='FK IK Switch', k = True, attributeType= 'enum', en='FK:IK')
        for x in range(len(switchlist)):
            cmds.setAttr(switchlist[x], lock= True, k=False)
            x += x + 1

#Runs checkbox statememts 
def queries():
    gimbalfix()
    switch(createoffset)
    createoffset()
    
#Creates Circle Control 
def CreateCircle():
    createcircle = cmds.circle(nr=(0,1,0))
    queries()

#Creates Cube Control
def CreateCube():
    cubecreate = mm.eval('curve -d 1 -p 0.5 0.5 -0.5 -p 0.5 0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 ;')
    queries()

#Creates Gear Control
def CreateGear():
    creategear = mm.eval('curve -d 1 -p -0.22961 0 0.92388 -p -0.206649 0 1.02388 -p -0.114805 0 1.12388 -p 0.114805 0 1.12388 -p 0.206649 0 1.02388 -p 0.22961 0 0.92388 -p 0.490923 0 0.81564 -p 0.577869 0 0.870115 -p 0.713523 0 0.875882 -p 0.875882 0 0.713523 -p 0.870115 0 0.577869 -p 0.81564 0 0.490923 -p 0.92388 0 0.22961 -p 1.02388 0 0.206649 -p 1.12388 0 0.114805 -p 1.12388 0 -0.114805 -p 1.02388 0 -0.206649 -p 0.92388 0 -0.22961 -p 0.81564 0 -0.490923 -p 0.870115 0 -0.577869 -p 0.875882 0 -0.713523 -p 0.713523 0 -0.875882 -p 0.577869 0 -0.870115 -p 0.490923 0 -0.81564 -p 0.22961 0 -0.92388 -p 0.206649 0 -1.02388 -p 0.114805 0 -1.123879 -p -0.114805 0 -1.123879 -p -0.206649 0 -1.023879 -p -0.22961 0 -0.923879 -p -0.490923 0 -0.81564 -p -0.577869 0 -0.870115 -p -0.713524 0 -0.875882 -p -0.875882 0 -0.713523 -p -0.870115 0 -0.577869 -p -0.81564 0 -0.490923 -p -0.92388 0 -0.22961 -p -1.02388 0 -0.206649 -p -1.123879 0 -0.114805 -p -1.123879 0 0.114805 -p -1.023879 0 0.206649 -p -0.923879 0 0.22961 -p -0.81564 0 0.490923 -p -0.870115 0 0.57787 -p -0.875882 0 0.713524 -p -0.713523 0 0.875883 -p -0.577869 0 0.870115 -p -0.490923 0 0.81564 -p -0.22961 0 0.92388 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 ;')
    queries()

#Creates Icosagon Control 
def CreateIco():
    createico = mm.eval('curve -d 1 -p -0.276393 0.850651 -0.447214 -p 0.276393 0.850651 0.447214 -p -0.723607 0.525731 0.447214 -p -0.276393 0.850651 -0.447214 -p -0.894427 -7.81933e-08 -0.447214 -p -0.723607 0.525731 0.447214 -p -0.723607 -0.525731 0.447214 -p -0.894427 -7.81933e-08 -0.447214 -p -0.276393 -0.850651 -0.447214 -p -0.723607 -0.525731 0.447214 -p -0.723607 0.525731 0.447214 -p 0 0 1 -p -0.723607 -0.525731 0.447214 -p 0.276393 -0.850651 0.447214 -p 0 0 1 -p 0.276393 0.850651 0.447214 -p -0.276393 0.850651 -0.447214 -p 0.723607 0.525731 -0.447214 -p 0.276393 0.850651 0.447214 -p 0.894427 0 0.447214 -p 0 0 1 -p 0.276393 -0.850651 0.447214 -p 0.723607 -0.525731 -0.447214 -p 0.894427 0 0.447214 -p 0.723607 0.525731 -0.447214 -p 0 0 -1 -p 0.723607 -0.525731 -0.447214 -p -0.276393 -0.850651 -0.447214 -p -0.894427 -7.81933e-08 -0.447214 -p 0 0 -1 -p -0.276393 0.850651 -0.447214 -p 0 0 -1 -p -0.276393 -0.850651 -0.447214 -p 0.723607 -0.525731 -0.447214 -p 0.276393 -0.850651 0.447214 -p 0.894427 0 0.447214 -p 0.276393 -0.850651 0.447214 -p -0.276393 -0.850651 -0.447214 -p 0.723607 -0.525731 -0.447214 -p 0.723607 0.525731 -0.447214 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 ;')
    queries()

#Creates Arrow Control
def CreateArrow():
    createarrow = mm.eval('curve -d 1 -p 1 0 0 -p 1 0 -2 -p -1 0 -2 -p -1 0 0 -p -2 0 0 -p 0 0 2 -p 2 0 0 -p 1 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;')
    queries()
#Creates Square Control
def CreateSquare():
    createsquare = mm.eval('curve -d 1 -p 5 0 -5 -p -5 0 -5 -p -5 0 5 -p 5 0 5 -p 5 0 -5 -k 0 -k 1 -k 2 -k 3 -k 4 ;')
    queries()
    
#Creates joints by input #
def CreateJoints():
    jseq = int(input())
    jnum = 0
    for i in range(jseq):
        cmds.joint(p= (jnum, 0, 0))
        jnum = jnum + 1         

#makes a new window for controls  
def window():
    #Deletes old window
    mywindow = 'Custom Control Window'
    if cmds.window(mywindow, exists=True):
        cmds.deleteUI(mywindow, window = True)  

    #Creates window layout
    mywindow = cmds.window('The bRIGdge', iconName='bRIGdge window', widthHeight=(300, 500))
    windowview = cmds.showWindow(mywindow)
    clayout = cmds.columnLayout(adjustableColumn=True )
    separate = cmds.separator(h=10, style = 'shelf')
    cmds.text(l= 'Welcome to the bRIGdge', al ='center', font='fixedWidthFont', rs = False, w=100, h =25 )
    #Command buttons 
    cmds.separator(h=10, style= 'shelf')
    cmds.separator(h=10)
    JointCreate = cmds.button( label='Create Joint Sequence', command = 'CreateJoints()') 
    cmds.separator(h=10) 
       
    CircleControl = cmds.button( label='Create Circle Control', command= 'CreateCircle()')
    cmds.separator(h=3, style = 'none')
    CubeControl = cmds.button( label='Create Cube Control', command = 'CreateCube()')
    cmds.separator(h=3, style = 'none')
    GearControl = cmds.button( label='Create Gear Control', command = 'CreateGear()')
    cmds.separator(h=3, style = 'none')
    IcosagonControl = cmds.button( l='Create Icosagon Control', command = 'CreateIco()')
    cmds.separator(h=3, style = 'none')
    ArrowControl = cmds.button (l = 'Create Arrow Control', command = 'CreateArrow()')
    cmds.separator(h=3, style = 'none')
    SquareControl = cmds.button (l = 'Create Square Control', command = 'CreateSquare()')
    
    cmds.separator(h=10)          
    CreateOffset = cmds.checkBox('createoffset', label='Create Offset Group', v = False)
    GimbalFix = cmds.checkBox ('gimbal', label = 'Rotation Order', v = False)
    FKIKSwitch = cmds.checkBox('fkikswitch', label = 'FK IK Switch', v = False)
    cmds.setParent( '..' )
        
window()

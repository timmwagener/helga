#"Newton"
#arash Hosseini 19.03.2014

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel



#/check window exist/
if cmds.window("dynamo", exists = True):
    cmds.deleteUI("dynamo")

if cmds.window("dynamo_locators", exists=True):
    cmds.deleteUI("dynamo_locators")

if cmds.window("dupSpecialX", exists=True):
    cmds.deleteUI("dupSpecialX")

if cmds.window("dupSpecialY", exists=True):
    cmds.deleteUI("dupSpecialY")

if cmds.window("dupSpecialZ", exists=True):
    cmds.deleteUI("dupSpecialZ")

#/main window/
def UI():
    cmds.warning("Welcome to Newton. For more Information press the Help Button.")
    window = cmds.window("dynamo", title = "Jelly", w =330, h=400, mnb=True, mxb=False, menuBar=True,sizeable=False)
    cmds.scrollLayout( 'scrollLayout' )
    #/menu/
    cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1, columnWidth=300)
    cmds.menu( label='Duplicate Special', tearOff=True )
    cmds.menuItem(subMenu=True,label='X Axis')
    cmds.menuItem(label='X Translate',command=duplicateSpecialX)
    cmds.setParent( '..', menu=True )
    cmds.menuItem(subMenu=True,label='Y Axis')
    cmds.menuItem( label='Y Translate',command=duplicateSpecialY)
    cmds.setParent( '..', menu=True )
    cmds.menuItem(subMenu=True,label='Z Axis')
    cmds.menuItem( label='Z Translate',command=duplicateSpecialZ)
    cmds.setParent('..',menu=True)
    cmds.menuItem(label='Maya Interface', command=mayaInterface)
    cmds.menu( label='Help', tearOff=True )
    cmds.menuItem(label='Help')
    cmds.menuItem(label='Info')


    cmds.columnLayout( columnAttach=('both', 3), rowSpacing=1, columnWidth=300)
    #/image/
    imagePath = cmds.internalVar(upd = True) + "icons/newton.jpg"
    #cmds.image(w = 200, h = 120, image = imagePath)


    cmds.columnLayout( adjustableColumn=True )
    cmds.frameLayout( label='Locators', bgc=(0.7,0.2,0.2),w=250,cll=True,borderStyle='out' )
    cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1, columnWidth=285)
    cmds.button(label="Create Locator on Vertex",command=createVertexOnPoint)
    cmds.button(label="Create Locator on Space",command=createLocator)
    cmds.button(label="Snap Object to Target",command=snapLocatorToTarget)
    cmds.button(label="Create Locator based on Target Matrix",command=createLocatorOnCenter)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout( label='Data', bgc=(0.7,0.2,0.2),cll=True,borderStyle='in' )
    cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1, columnWidth=285)
    locatorsNumberOptionMenu = cmds.textScrollList("locatorsNumberOptionMenu",w=100, h = 100)
    cmds.button(label="Show Locators",h=50,command=loadLoc)
    cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1,100),(2,100),(3,80)])
    cmds.text(label="Set Start Number",align='left')
    cmds.textField('startLoc')
    cmds.button(label="Set",command=setStartNumber)
    cmds.text(label="Set End Number",align='left')
    cmds.textField('endLoc')
    cmds.button(label="Set",command=setEndNumber)
    cmds.text(label="Set Mesh", align='left')
    cmds.textField('SMesh')
    cmds.button(label="Set",command=queryMesh)
    cmds.text(label='Point Lock', align='left')
    pointLockOptionMenu = cmds.optionMenu("pointLockOptionMenu",w=180)
    cmds.menuItem(label='1.Base')
    cmds.menuItem(label='2.Tip')
    cmds.menuItem(label='3.BothEnds')
    cmds.text(label="")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout( label='Build',bgc=(0.7,0.2,0.2),cll=True, borderStyle='in' )
    cmds.columnLayout( columnAttach=('both', 3), rowSpacing=1, columnWidth=290)
    cmds.button(label="Build without Mesh",bgc=(0.5,0.7,0.5),h=40,command=buildwitoutMesh)
    cmds.button(label="Build with Mesh",bgc=(0.5,0.7,0.5),h=40,command=buildwithMesh)
    cmds.button(label="manuell Skining",command=skining)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout( label='tools',bgc=(0.7,0.2,0.2),cll=True, borderStyle='in' )
    cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1,185),(2,100)])
    cmds.button(label="PB",w=150,command=interaktivPlayback)
    cmds.button(label="Out",command=outliner)
    Rename=cmds.textField('Rename',w=150)
    cmds.button(label="Rename",command=RenameMesh)
    Suffix=cmds.textField('Suffix',w=150)
    cmds.button(label="Suffix",command=SuffixMesh)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.showWindow()


#Locator Area
#Loc On Vertex
def createVertexOnPoint(*args):

    selectedVertices =[]
    selectedVertices = pm.ls( selection=True )
    print("Selected objects " + str(len(selectedVertices)))

    selectedVerticesLen=len(selectedVertices)
    if selectedVerticesLen==1:
        for vertex in selectedVertices:
            vertexLocator=pm.spaceLocator( p=vertex.getPosition(space='world'), name='locator1')
            pm.xform(vertexLocator,cp=1)
            #print(vertex.getPosition())
        del selectedVertices
    else:
        cmds.warning("Bitte eine Vertex auswaehlen")
#Loc On Space
def createLocator(*args):
    createLocator=cmds.spaceLocator(name="locator1")

#Loc to Target
def snapLocatorToTarget(*args):
    sel = cmds.ls( selection=True )
    sellen=len(sel)
    if sellen==2:
        E = sel[1]
        F = sel[0]
        Fmatrix = cmds.xform( F, query=True, worldSpace=True, matrix=True )
        cmds.xform( E, worldSpace=True, matrix=Fmatrix )

    else:
        cmds.warning("Bitte zuerst Driver dann Target auswaehlen")

def duplicateSpecial(*args):
    sel=cmds.ls(selection=True)
    sellen=len(sel)
    if sellen==1:
        x=null
    else:
        cmds.warning("Bitte Object auswahlen")



#Loc On Center of Object
def createLocatorOnCenter(*args):
    objectsList=cmds.ls(selection=True)
    sellen=len(objectsList)
    if sellen==1:
        ziel=objectsList[0]
        queryObjectPos=cmds.xform(ziel,query=True, worldSpace=True, matrix=True )
        print queryObjectPos
        for i in objectsList:
            createLocator=cmds.spaceLocator(p=(0,0,0),r=True,name="locator1")
            centerPivot=cmds.xform(createLocator,cp=1,worldSpace=True, matrix=queryObjectPos)

    else:
        cmds.warning("Select Object")




#load locators
def loadLoc(*args):
    if cmds.window("dynamo_locators", exists=True):
        cmds.deleteUI("dynamo_locators")
    lsloc=cmds.ls(selection=True)
    lenlsloc=len(lsloc)
    locatorsNumbermenuItem=cmds.textScrollList("locatorsNumberOptionMenu",e=True,ra=True)
    if lenlsloc>0:
        #/windows Jelly Locatorslist/
        cmds.window("dynamo_locators",title="Jelly_Locatorslist",mnb=True, mxb=False,w=80,h=50,sizeable=False)
        cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1,columnWidth=30,h=200)
        locatorOptionMenu = cmds.textScrollList("locatorOptionMenu",w=100, h = 200,dcc=selectLocator)
        cmds.showWindow()
        for locs, objects in enumerate(lsloc):
            cmds.textScrollList("locatorsNumberOptionMenu", e=True, append=locs)
            cmds.textScrollList("locatorOptionMenu", e=True, append=objects)
    else:
        cmds.warning("Select Locators")

def selectLocator(*args):
    queryLocOpMenu=cmds.textScrollList("locatorOptionMenu", q=True, si=True)[0]
    cmds.select(queryLocOpMenu)

def setStartNumber(*args):
    queryLocOpMenu=cmds.textScrollList("locatorsNumberOptionMenu", q=True, si=True)[0]
    setStart = cmds.textField('startLoc', edit=True, text=queryLocOpMenu)

def setEndNumber(*args):
    queryLocOpMenu=cmds.textScrollList("locatorsNumberOptionMenu", q=True, si=True)[0]
    setEnd = cmds.textField('endLoc', edit=True, text=queryLocOpMenu)

#/duplicate Special area/
def translateXpermanent(*args):
    sel=cmds.ls(selection=True)
    lensel=len(sel)
    if lensel ==1:
        queryCopiesX=cmds.textField('copiesXper', v=True, q=True)
        queryTransX=cmds.textField('translateXper', v=True, q=True)
        range=int(queryCopiesX)
        abstand=float(queryTransX)
        for i in xrange(range):
            j=cmds.duplicate(rr=True)
            cmds.move(abstand,j,x=True,r=True,objectSpace=True)
    else:
        cmds.warning("select Object")

def trasnlateXincreasing(*args):
    sel=cmds.ls(selection=True)
    lensel=len(sel)
    if lensel ==1:
        queryCopiesX=cmds.textField('copiesXinc', text=True, q=True)
        queryTransX=cmds.textField('translateXinc', text=True, q=True)
        range=int(queryCopiesX)
        abstand=float(queryTransX)
        for i in xrange(range):
            j=cmds.duplicate(rr=True,st=True)
            cmds.move(abstand,j,x=True,r=True,objectSpace=True)
    else:
        cmds.warning("select Object")


def duplicateSpecialX(*args):
    if cmds.window("dupSpecialX", exists=True):
        cmds.deleteUI("dupSpecialX")

    cmds.window("dupSpecialX",title="Jelly Special X",mnb=True, mxb=False,w=250,h=130,sizeable=False)
    form = cmds.formLayout()
    tabs = cmds.tabLayout(w=250, h=100, bgc = (0.3,0.3,0.3), innerMarginWidth=10, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    child1=cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1,columnWidth=250,h=110)
    cmds.text(label="Permanent Distance", bgc=(0.5,0.7,0.5))
    cmds.text(label="Number of copies", align='left')
    cmds.textField('copiesXper',w=200)
    cmds.text(label="Translate", align='left')
    cmds.textField('translateXper',w=200)
    cmds.button(label="Duplicate", bgc=(0.5,0.7,0.5),command=translateXpermanent)
    cmds.setParent( '..' )

    child2=cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1,columnWidth=250,h=110)
    cmds.text(label="Increasing Distance", bgc=(0.5,0.3,0.5))
    cmds.text(label="Number of copies", align='left')
    cmds.textField('copiesXinc',w=200)
    cmds.text(label="Translate", align='left')
    cmds.textField('translateXinc',w=200)
    cmds.button(label="Duplicate",bgc=(0.5,0.3,0.5),command=trasnlateXincreasing)
    cmds.setParent( '..' )

    cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Permanent Distance'),(child2,'Increasing Distance')))
    cmds.setParent( '..' )
    cmds.showWindow()

def translateYpermanent(*args):
    sel=cmds.ls(selection=True)
    lensel=len(sel)
    if lensel ==1:
        queryCopiesY=cmds.textField('copiesYper', text=True, q=True)
        queryTransY=cmds.textField('translateYper', text=True, q=True)
        range=int(queryCopiesY)
        abstand=float(queryTransY)
        for i in xrange(range):
            j=cmds.duplicate(rr=True)
            cmds.move(abstand,j,y=True,r=True,objectSpace=True)
    else:
        cmds.warning("select Object")

def trasnlateYincreasing(*args):
    sel=cmds.ls(selection=True)
    lensel=len(sel)
    if lensel ==1:
        queryCopiesY=cmds.textField('copiesYinc', text=True, q=True)
        queryTransY=cmds.textField('translateYinc', text=True, q=True)
        range=int(queryCopiesY)
        abstand=float(queryTransY)
        for i in xrange(range):
            j=cmds.duplicate(rr=True,st=True)
            cmds.move(abstand,j,y=True,r=True,objectSpace=True)
    else:
        cmds.warning("select Object")

def duplicateSpecialY(*args):
    if cmds.window("dupSpecialY", exists=True):
        cmds.deleteUI("dupSpecialY")

    cmds.window("dupSpecialY",title="Jelly Special Y",mnb=True, mxb=False,w=250,h=130,sizeable=False)
    form = cmds.formLayout()
    tabs = cmds.tabLayout(w=250, h=100, bgc = (0.3,0.3,0.3), innerMarginWidth=10, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    child1=cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1,columnWidth=250,h=110)
    cmds.text(label="Permanent Distance", bgc=(0.5,0.7,0.5))
    cmds.text(label="Number of copies", align='left')
    cmds.textField('copiesYper',w=200)
    cmds.text(label="Translate", align='left')
    cmds.textField('translateYper',w=200)
    cmds.button(label="Duplicate", bgc=(0.5,0.7,0.5),command=translateYpermanent)
    cmds.setParent( '..' )

    child2=cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1,columnWidth=250,h=110)
    cmds.text(label="Increasing Distance", bgc=(0.5,0.3,0.5))
    cmds.text(label="Number of copies", align='left')
    cmds.textField('copiesYinc',w=200)
    cmds.text(label="Translate", align='left')
    cmds.textField('translateYinc',w=200)
    cmds.button(label="Duplicate",bgc=(0.5,0.3,0.5),command=trasnlateYincreasing)
    cmds.setParent( '..' )

    cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Permanent Distance'),(child2,'Increasing Distance')))
    cmds.setParent( '..' )
    cmds.showWindow()


def translateZpermanent(*args):
    sel=cmds.ls(selection=True)
    lensel=len(sel)
    if lensel ==1:
        queryCopiesZ=cmds.textField('copiesZper', text=True, q=True)
        queryTransZ=cmds.textField('translateZper', text=True, q=True)
        range=int(queryCopiesZ)
        abstand=float(queryTransZ)
        for i in xrange(range):
            j=cmds.duplicate(rr=True)
            cmds.move(abstand,j,z=True,r=True,objectSpace=True)
    else:
        cmds.warning("select Object")

def trasnlateZincreasing(*args):
    sel=cmds.ls(selection=True)
    lensel=len(sel)
    if lensel ==1:
        queryCopiesZ=cmds.textField('copiesZinc', text=True, q=True)
        queryTransZ=cmds.textField('translateZinc', text=True, q=True)
        range=int(queryCopiesZ)
        abstand=float(queryTransZ)
        for i in xrange(range):
            j=cmds.duplicate(rr=True,st=True)
            cmds.move(abstand,j,z=True,r=True,objectSpace=True)
    else:
        cmds.warning("select Object")

def duplicateSpecialZ(*args):
    if cmds.window("dupSpecialZ", exists=True):
        cmds.deleteUI("dupSpecialZ")

    cmds.window("dupSpecialZ",title="Jelly Special Z",mnb=True, mxb=False,w=250,h=130,sizeable=False)
    form = cmds.formLayout()
    tabs = cmds.tabLayout(w=250, h=100, bgc = (0.3,0.3,0.3), innerMarginWidth=10, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    child1=cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1,columnWidth=250,h=110)
    cmds.text(label="Permanent Distance", bgc=(0.5,0.7,0.5))
    cmds.text(label="Number of copies", align='left')
    cmds.textField('copiesZper',w=200)
    cmds.text(label="Translate", align='left')
    cmds.textField('translateZper',w=200)
    cmds.button(label="Duplicate", bgc=(0.5,0.7,0.5),command=translateZpermanent)
    cmds.setParent( '..' )

    child2=cmds.columnLayout( columnAttach=('both', 0), rowSpacing=1,columnWidth=250,h=110)
    cmds.text(label="Increasing Distance", bgc=(0.5,0.3,0.5))
    cmds.text(label="Number of copies", align='left')
    cmds.textField('copiesZinc',w=200)
    cmds.text(label="Translate", align='left')
    cmds.textField('translateZinc',w=200)
    cmds.button(label="Duplicate",bgc=(0.5,0.3,0.5),command=trasnlateZincreasing)
    cmds.setParent( '..' )

    cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Permanent Distance'),(child2,'Increasing Distance')))
    cmds.setParent( '..' )
    cmds.showWindow()


def mayaInterface(*args):
    mel.eval('DuplicateSpecialOptions')


def RenameMesh(*args):
    queryRenameMesh=cmds.textField("Rename", text=True, q=True)
    selected_objects = cmds.ls(selection=True, long=True)
    selected_objects.reverse()
    totalObjects = len(selected_objects)
    print totalObjects

    cmds.text(label=totalObjects)

    # We are doing this in reverse, last object renamed first

    for number, object in enumerate(selected_objects):
        #print 'Old Name:', object
        #print 'New Name:', '%s%02d' % (newname, totalObjects-number)
        cmds.rename(object, ('%s%02d' % (queryRenameMesh, totalObjects-number)))

def SuffixMesh(*args):
    selected_objects = cmds.ls(selection=True, long=True)
    selected_objects_short = cmds.ls(selection=True, long=False)
    querySuffixMesh=cmds.textField("Suffix", text=True, q=True)
    selected_objects.reverse()
    selected_objects_short.reverse()
    totalObjects = len(selected_objects)
    for number, object in enumerate(selected_objects):
        #print 'Old Name:', object
        #print 'New Name:', selected_objects_short[number]+suffix
        cmds.rename(object, selected_objects_short[number]+querySuffixMesh)

def interaktivPlayback(*args):
    mel.eval('InteractivePlayback')

def outliner(*args):
    mel.eval('OutlinerWindow')

def skining(*args):
    mel.eval('SmoothBindSkinOptions')

def queryMesh(*args):
    selectBodyMesh=cmds.ls(selection=True)[0]
    addBodyMesh = cmds.textField('SMesh', edit=True, text=selectBodyMesh)






#/BUild/
def buildwitoutMesh(*args):

    if cmds.window("dynamo_locators", exists=True):
        cmds.deleteUI("dynamo_locators")

    if cmds.window("dupSpecialX", exists=True):
        cmds.deleteUI("dupSpecialX")

    if cmds.window("dupSpecialY", exists=True):
        cmds.deleteUI("dupSpecialY")

    if cmds.window("dupSpecialZ", exists=True):
        cmds.deleteUI("dupSpecialZ")


    #/joints herstellen/
    locatorListe=cmds.ls(selection=True)
    listLaenge=len(locatorListe)

    if listLaenge>4:
        firstLocator=locatorListe[0]
        queryFirstLocatorPos=cmds.xform(firstLocator,translation=True,q=True)
        createController=cmds.circle( nr=(0, 1, 0), c=(queryFirstLocatorPos),r=10,d=1,s=6,n="root_Controller")
        centerPivotController=cmds.xform(createController,cp=True)
        cmds.makeIdentity(createController,apply=True, t=1, r=1, s=1, n=0)
        jointList=[]
        for i in locatorListe:
            queryLocPos=cmds.xform(i,translation=True,q=True)
            cmds.select(clear=True)
            createJoint=cmds.joint(p=(queryLocPos))
            jointList.append(createJoint)
            cmds.select(clear=True)
        print jointList


        #parenting root_Joint to root_Controller
        mainController=createController
        #listJoint=cmds.ls(type="joint")
        firstJoint=jointList[0]
        pointConstraint=cmds.pointConstraint(mainController,firstJoint,mo=True)
        orientConstraint=cmds.orientConstraint(mainController,firstJoint,mo=True)
        cmds.select(clear=True)

        #/joints parenting/
        #jointListe = cmds.ls(type = "joint",v=True)
        for i, inhalt in enumerate(jointList):
            # Break Loop
            if i == 0:
                continue
            vorheriges = jointList[i-1]
            aktuelles = inhalt
            cmds.parent(aktuelles, vorheriges)
            cmds.select(clear=True)

        #/Query Start-End-Number/
        queryStartNumber=cmds.textField('startLoc', text=True, q=True)
        print queryStartNumber
        queryEndNumber=cmds.textField('endLoc', text=True, q=True)
        print queryEndNumber
        start=int(queryStartNumber)
        end=int(queryEndNumber)

        #/create Curve/
        #jointListe = cmds.ls(type = "joint",v=True)
        endJoint=len(jointList)
        jointListwitoutfirst=jointList[start:end]
        jnListlaenge=len(jointListwitoutfirst)
        if jnListlaenge>0:
            curve_degree = 3
            jointPos=[]
            for i in jointListwitoutfirst:
                queryJnPos=cmds.xform(i, ws=True,translation=True,query=True)
                jointPos.append(queryJnPos)
            #print jointPos
            cvCurve=cmds.curve(d=curve_degree,p=jointPos,ws=True,n="Curve1")
            epCurve=cmds.fitBspline( ch=1, tol=0.0,n="Original_Curve")
            cmds.rename("Original_Curve","DynamoOrgCurve")
            cmds.delete(cvCurve)


        #/make dynamic curve/
        mel.eval('makeCurvesDynamicHairs %d %d %d' % (True, False, True))


        #/iksplineHAndle/
        sel=cmds.ls(type="joint",v=True)
        startjoint=jointList[start]
        endeffector=jointList[end]
        #print startjoint, endeffector
        ikSplineHandle=cmds.ikHandle( n="dynamoIkHandle",sj=startjoint, ee=endeffector,solver='ikSplineSolver', p=2, c="curve1",tws="linear",pcv=True,ccv=False,snc=False)
        renameiKHandleCurve=cmds.rename("curve1","NewDynamoCurve")
        NewDyCurve=renameiKHandleCurve


        #/change follicle point lock/
        querypointLockOptionMenu=cmds.optionMenu("pointLockOptionMenu",q=True,value=True)[0]
        print querypointLockOptionMenu
        pointLock=int(querypointLockOptionMenu)
        follicleList=cmds.ls("follicle1")
        for o in follicleList:
            setPointLockBase=cmds.setAttr(o+".pointLock", pointLock)
        cmds.rename("follicle1","DynamoFollicle")

        #/hide/
        #cmds.hide( cmds.ls( type="joint" ) )

        #/renaming Joints/
        jointListe = cmds.ls(type = "joint",v=True)
        rootJoint=jointList[0]
        endJoint=jointList [0-1]
        #print endJoint
        endNewName="end_Joint"
        rootNewName="root_Joint"
        cmds.rename(rootJoint,rootNewName)
        cmds.rename(endJoint,endNewName)


        #/cleaning and parenting/
        cmds.parent("hairSystem1Follicles","root_Joint")
        cmds.hide("DynamoOrgCurve")
        cmds.select(clear=True)
        Data=cmds.group(NewDyCurve,ikSplineHandle,"hairSystem1","hairSystem1OutputCurves",w=True,n="Data")
        cmds.parent("effector1","end_Joint")
        cmds.select(clear=True)
        hideIkHandle=cmds.hide("dynamoIkHandle")
        cmds.select(clear=True)
        cmds.hide(cmds.ls(type="locator"))
        cmds.select(clear=True)



    else:
        cmds.warning("Select Locators")



def buildwithMesh(*args):

    if cmds.window("dynamo_locators", exists=True):
        cmds.deleteUI("dynamo_locators")

    if cmds.window("dupSpecialX", exists=True):
        cmds.deleteUI("dupSpecialX")

    if cmds.window("dupSpecialY", exists=True):
        cmds.deleteUI("dupSpecialY")

    if cmds.window("dupSpecialZ", exists=True):
        cmds.deleteUI("dupSpecialZ")


    #/joints herstellen/
    locatorListe=cmds.ls(selection=True)
    listLaenge=len(locatorListe)

    if listLaenge>4:
        firstLocator=locatorListe[0]
        queryFirstLocatorPos=cmds.xform(firstLocator,translation=True,q=True)
        createController=cmds.circle( nr=(0, 1, 0), c=(queryFirstLocatorPos),r=10,d=1,s=6,n="root_Controller")
        centerPivotController=cmds.xform(createController,cp=True)
        cmds.makeIdentity(createController,apply=True, t=1, r=1, s=1, n=0)
        jointList=[]
        for i in locatorListe:
            queryLocPos=cmds.xform(i,translation=True,q=True)
            cmds.select(clear=True)
            createJoint=cmds.joint(p=(queryLocPos))
            jointList.append(createJoint)
            cmds.select(clear=True)
        print jointList


        #parenting root_Joint to root_Controller
        mainController=createController
        #listJoint=cmds.ls(type="joint")
        firstJoint=jointList[0]
        pointConstraint=cmds.pointConstraint(mainController,firstJoint,mo=True)
        orientConstraint=cmds.orientConstraint(mainController,firstJoint,mo=True)
        cmds.select(clear=True)

        #/joints parenting/
        #jointListe = cmds.ls(type = "joint",v=True)
        for i, inhalt in enumerate(jointList):
            # Break Loop
            if i == 0:
                continue
            vorheriges = jointList[i-1]
            aktuelles = inhalt
            cmds.parent(aktuelles, vorheriges)
            cmds.select(clear=True)

        #/Query Start-End-Number/
        queryStartNumber=cmds.textField('startLoc', text=True, q=True)
        print queryStartNumber
        queryEndNumber=cmds.textField('endLoc', text=True, q=True)
        print queryEndNumber
        start=int(queryStartNumber)
        end=int(queryEndNumber)

        #/create Curve/
        #jointListe = cmds.ls(type = "joint",v=True)
        endJoint=len(jointList)
        jointListwitoutfirst=jointList[start:end]
        jnListlaenge=len(jointListwitoutfirst)
        if jnListlaenge>0:
            curve_degree = 3
            jointPos=[]
            for i in jointListwitoutfirst:
                queryJnPos=cmds.xform(i, ws=True,translation=True,query=True)
                jointPos.append(queryJnPos)
            #print jointPos
            cvCurve=cmds.curve(d=curve_degree,p=jointPos,ws=True,n="Curve1")
            epCurve=cmds.fitBspline( ch=1, tol=0.0,n="Original_Curve")
            cmds.rename("Original_Curve","DynamoOrgCurve")
            cmds.delete(cvCurve)


        #/make dynamic curve/
        mel.eval('makeCurvesDynamicHairs %d %d %d' % (True, False, True))


        #/iksplineHAndle/
        sel=cmds.ls(type="joint",v=True)
        startjoint=jointList[start]
        endeffector=jointList[end]
        #print startjoint, endeffector
        ikSplineHandle=cmds.ikHandle( n="dynamoIkHandle",sj=startjoint, ee=endeffector,solver='ikSplineSolver', p=2, c="curve1",tws="linear",pcv=True,ccv=False,snc=False)
        renameiKHandleCurve=cmds.rename("curve1","NewDynamoCurve")
        NewDyCurve=renameiKHandleCurve


        #/change follicle point lock/
        querypointLockOptionMenu=cmds.optionMenu("pointLockOptionMenu",q=True,value=True)[0]
        print querypointLockOptionMenu
        pointLock=int(querypointLockOptionMenu)
        follicleList=cmds.ls("follicle1")
        for o in follicleList:
            setPointLockBase=cmds.setAttr(o+".pointLock", pointLock)
        cmds.rename("follicle1","DynamoFollicle")

        #/hide/
        #cmds.hide( cmds.ls( type="joint" ) )

        #/skin/
        addBodyMesh = cmds.textField('SMesh', text=True, query=True)
        cmds.skinCluster( addBodyMesh, jointList[start:end],tsb=True,nw=3,mi=7,dr=10.0,ih=True )

        #/renaming Joints/
        jointListe = cmds.ls(type = "joint",v=True)
        rootJoint=jointList[0]
        endJoint=jointList [0-1]
        #print endJoint
        endNewName="end_Joint"
        rootNewName="root_Joint"
        cmds.rename(rootJoint,rootNewName)
        cmds.rename(endJoint,endNewName)







        #/cleaning and parenting/
        cmds.parent("hairSystem1Follicles","root_Joint")
        cmds.hide("DynamoOrgCurve")
        cmds.select(clear=True)
        Data=cmds.group(NewDyCurve,ikSplineHandle,"hairSystem1","hairSystem1OutputCurves",w=True,n="Data")
        cmds.parent("effector1","end_Joint")
        cmds.select(clear=True)
        hideIkHandle=cmds.hide("dynamoIkHandle")
        cmds.select(clear=True)
        cmds.hide(cmds.ls(type="locator"))
        cmds.select(clear=True)



    else:
        cmds.warning("Select Locators")



#clean_save by arash hosseini

import maya.cmds as cmds
import os
import time

Version= '0.5'
#zu_eigene_pfad_wechseln!!!

projects_scene_dir = "Y:/Production/3d/"


class cleanSave_UI:

    #mainwindow
    def __init__(self, windowsWidth=360,windowsHeight=400 ):

        welcome_massage=cmds.warning("Welcome, your Main Path is: "+projects_scene_dir)

        self.allUIs={}
        self.deletewindow()
        self.windowsWidth=windowsWidth
        self.windowsHeight=windowsHeight

        #window
        self.allUIs ["clean_save"]=cmds.window('clean_save', title='clean save  v '+str(Version)+' - UI ', widthHeight=(self.windowsWidth,self.windowsHeight),sizeable=False,menuBar=True, minimizeButton=True, maximizeButton=False)

        cmds.menu(label="Debug", tearOff = True)
        cmds.menuItem(label = "Debug", command=self.debug)
        cmds.setParent('..', menu=True)


        # Vars
        self.fileName = ""

        #call_mainUI//call_listFiles
        self.mainUI()


    def mainUI(self,windowsWidth=355,windowsHeight=400):

        self.windowsWidth=windowsWidth
        self.windowsHeight=windowsHeight

        #mainLayout__rowColumn
        self.allUIs["rowColumn_mainLayout"] = cmds.columnLayout( 'mainLayout',columnAttach=('both', 0), rowSpacing=1,adjustableColumn=True,w=(self.windowsWidth),h=(self.windowsHeight))


        #text info line
        self.allUIs["name_info_text"]=cmds.text(label="Character Name", align='left')
        self.allUIs["name_text_field"]=cmds.textField('nameField',bgc=(0.7,0.6,0.6),cc=(self.nameField))
        self.allUIs["department_info_text"]=cmds.text(label="Department", align='left')
        self.allUIs["department_option_box"]=cmds.optionMenu('depField',cc=(self.depField))

        self.allUIs["option_box_sculpt"]=cmds.menuItem( label='0. Off' )
        self.allUIs["option_box_sculpt"]=cmds.menuItem( label='1. Sculpt' )
        self.allUIs["option_box_sculpt"]=cmds.menuItem( label='2. Shading' )
        self.allUIs["option_box_sculpt"]=cmds.menuItem( label='3. Rigging' )
        self.allUIs["option_box_sculpt"]=cmds.menuItem( label='4. Animation' )

        self.allUIs["faktor_info_text"]=cmds.text(label="Faktor", align='left')
        self.allUIs["faktor_text_field"]=cmds.textField("faktorField",bgc=(0.6,0.6,0.7), cc=(self.faktorField))
        self.allUIs["version_info_text"]=cmds.text(label="Version", align='left')
        self.allUIs["version_text_field"]=cmds.textField("versionField",bgc=(0.7,0.7,0.6), cc=(self.versionField))
        self.allUIs["artist_info_text"]=cmds.text(label="Artist", align='left')
        self.allUIs["artist_text_field"]=cmds.textField("artistField",bgc=(0.6,0.7,0.7), cc=(self.artistField))

        #space
        self.allUIs["space"]=cmds.separator(h=10, vis=True)

        #result_layout
        self.allUIs["rowColumn_result_mainLayout"] = cmds.rowColumnLayout( 'rowColumn_result_mainLayout',numberOfColumns=5,columnWidth=[(1,70),(2,70),(3,70),(4,70),(5,70)])

        #result_text_lines
        self.allUIs["text_name_result"]=cmds.text('resultName',label="",bgc=(0.7,0.6,0.6),h=20)
        self.allUIs["text_department_result"]=cmds.text('resultDepartment',label="",bgc=(0.6,0.7,0.6),h=20)
        self.allUIs["text_faktor_result"]=cmds.text('resultFaktor',label="",bgc=(0.6,0.6,0.7),h=20)
        self.allUIs["text_version_result"]=cmds.text('resultVersion',label="",bgc=(0.7,0.7,0.6),h=20)
        self.allUIs["text_artist_result"]=cmds.text('resultArtist',label="",bgc=(0.6,0.7,0.7),h=20)


        #subLayout__Column
        self.allUIs["column_sub_mainLayout"] = cmds.columnLayout( 'column_sub_mainLayout',columnAttach=('both', 0), rowSpacing=2,adjustableColumn=True,w=(self.windowsWidth),h=(self.windowsHeight))

        #space
        self.allUIs["spaces"]=cmds.separator(h=5, vis=True, st='none')

        #save_button
        self.allUIs["save_button"] = cmds.button('save',label="Save", h=50,w=300,bgc=(0.6,0.3,0.3), command=self.saveScene)

        #Saved_file
        self.allUIs["saved_file_text"]=cmds.text(label="last Saved File", align='left')
        self.allUIs["saved_file"]=cmds.text('savedFile', label="",bgc=(0.4,0.4,0.4),h=20 )


        #Folder_item
        self.allUIs["saved_path_text"]=cmds.text(label="saved Path", align ='left')

        self.allUIs["saved_path"]=cmds.text('savedPath', label="",bgc=(0.4,0.4,0.4),h=20 )

        #upversion button
        self.allUIs["ipversion_button"] = cmds.button('upversion', label="Upversion", h=35, w=300, bgc=(0.6,0.3,0.3),command=self.sceneCheck)
        #show_window
        cmds.showWindow(self.allUIs ["clean_save"])



    def deletewindow(self,*args):
        if cmds.window('clean_save', query=True, exists=True):
            cmds.deleteUI('clean_save', window=True)
        if cmds.window("saveQuestion", exists=True):
            cmds.deleteUI("saveQuestion")
        if cmds.window("Debug", exists=True):
            cmds.deleteUI("Debug")


    def nameField(self, *args):

        #query_color_value
        queryColorDepartmentField = cmds.text('resultDepartment', bgc=True,q = True)
        queryColorFaktorField = cmds.text('resultFaktor', bgc=True,q = True)
        queryColorVersionField = cmds.text('resultVersion', bgc=True,q = True)
        queryColorArtistField = cmds.text('resultArtist', bgc=True,q = True)

        queryNameField=cmds.textField('nameField', text=True, q=True)
        len_queryNameField=len(queryNameField)

        if len_queryNameField==0:
            cmds.warning("No Character Name selected")
            self.wrongChangeSaveColor()
            self.wrongChangeNameColor()
        else:
            lowerQueryNameField=queryNameField.lower()
            cleanNameField = cmds.text('resultName', e = True)
            for name in queryNameField:
                cmds.text('resultName', e = True, label=lowerQueryNameField)
                self.changeNameColor()

            if queryColorFaktorField[0]<0.4:
                if queryColorDepartmentField[0]<0.4:
                    if queryColorVersionField[0]<0.4:
                        if queryColorArtistField[0]<0.4:
                            self.changeColors()


    def depField(self, *args):
        cmds.select(clear=True)
        #query_color_value
        queryColorNameField = cmds.text('resultName', bgc=True,q = True)
        queryColorFaktorField = cmds.text('resultFaktor', bgc=True,q = True)
        queryColorVersionField = cmds.text('resultVersion', bgc=True,q = True)
        queryColorArtistField = cmds.text('resultArtist', bgc=True,q = True)

        cleanDepField = cmds.text('resultDepartment', e = True)
        queryDepField=cmds.optionMenu('depField',q=True,value=True)[0]

        if queryDepField=="0":
            for Dep in queryDepField:
                cmds.text('resultDepartment', e=True, label="")
                self.changeDepartmentColor()
        if queryDepField=="1":
            for Dep in queryDepField:
                cmds.text('resultDepartment', e = True, label="sculpt")
                self.changeDepartmentColor()
        if queryDepField=="2":
            for Dep in queryDepField:
                cmds.text('resultDepartment', e = True, label="shader")
                self.changeDepartmentColor()
        if queryDepField=="3":
            for Dep in queryDepField:
                cmds.text('resultDepartment', e = True, label="rig")
                self.changeDepartmentColor()
        if queryDepField=="4":
            for Dep in queryDepField:
                cmds.text('resultDepartment', e = True, label="animation")
                self.changeDepartmentColor()

        if queryColorNameField[0]<0.4:
            if queryColorFaktorField[0]<0.4:
                if queryColorVersionField[0]<0.4:
                    if queryColorArtistField[0]<0.4:
                        self.changeColors()


    def faktorField(self, *args):
        #query_color_value
        queryColorNameField = cmds.text('resultName', bgc=True,q = True)
        queryColorDepartmentField = cmds.text('resultDepartment', bgc=True,q = True)
        queryColorVersionField = cmds.text('resultVersion', bgc=True,q = True)
        queryColorArtistField = cmds.text('resultArtist', bgc=True,q = True)

        queryFaktorField=cmds.textField('faktorField', text=True, q=True)
        len_queryFaktorField=len(queryFaktorField)
        if len_queryFaktorField==0:
            cmds.warning("No Faktor selected or more as One selected")
            self.wrongChangeSaveColor()
            self.wrongChangeFaktorColor()

        else:
            lowerQueryFaktorField=queryFaktorField.lower()
            cleanFaktorField = cmds.text('resultFaktor', e = True)

            result_list=["a","b","c","d","e","f","g",
                         "h","j","i","k","l","m","n",
                         "o","p","q","r","s","t",
                         "u","v","w","x","y","z"]

            if queryColorNameField[0]<0.4:
                if queryColorDepartmentField[0]<0.4:
                    if queryColorVersionField[0]<0.4:
                        if queryColorArtistField[0]<0.4:
                            self.changeColors()

            if lowerQueryFaktorField in result_list:
                for faktor in queryFaktorField:
                    cmds.text('resultFaktor', e = True, label=lowerQueryFaktorField)
                    self.changeFaktorColor()
                    cmds.select(clear=True)
            else:
                cmds.warning("only string or more as One string selected")
                self.wrongChangeSaveColor()
                self.wrongChangeFaktorColor()




    def versionField(self, *args):

        #query_color_value
        queryColorNameField = cmds.text('resultName', bgc=True,q = True)
        queryColorDepartmentField = cmds.text('resultDepartment', bgc=True,q = True)
        queryColorFaktorField = cmds.text('resultFaktor', bgc=True,q = True)
        queryColorArtistField = cmds.text('resultArtist', bgc=True,q = True)


        queryVersionField=cmds.textField('versionField', text=True, q=True)

        query_version_prefix=cmds.textField('versionField', text=True, q=True)
        query_version_member_a=cmds.textField('versionField', text=True, q=True)
        query_version_member_b=cmds.textField('versionField', text=True, q=True)
        query_version_member_c=cmds.textField('versionField', text=True, q=True)
        query_version_member_d=cmds.textField('versionField', text=True, q=True)

        cleanVersionField = cmds.text('resultVersion', e = True)

        resultNumberList=["0","1","2","3","4","5","6","7","8","9"]
        resultversionList=["v"]

        len_queryVersionField=len(queryVersionField)

        if queryColorNameField[0]<0.4:
            if queryColorDepartmentField[0]<0.4:
                if queryColorFaktorField[0]<0.4:
                    if queryColorArtistField[0]<0.4:
                        self.changeColors()
                        cmds.select(clear=True)

        if len_queryVersionField==4:
            if query_version_member_a[0] in resultNumberList:
                if query_version_member_b[1] in resultNumberList:
                    if query_version_member_c[2] in resultNumberList:
                        if query_version_member_d[3] in resultNumberList:
                            for version in queryVersionField:
                                cmds.text('resultVersion', e = True, label=queryVersionField)
                                self.changeVersionColor()
                                cmds.select(clear=True)

                        else:
                            cmds.warning("after v only int, example:v0005")
                            self.wrongChangeSaveColor()
                            self.wrongChangeVersionColor()

                    else:
                        cmds.warning("after v only int, example:v0003")
                        self.wrongChangeSaveColor()
                        self.wrongChangeVersionColor()

                else:
                    cmds.warning("after v only int, example:v0002")
                    self.wrongChangeSaveColor()
                    self.wrongChangeVersionColor()

            else:
                cmds.warning("after v only int, example:v0004")
                self.wrongChangeSaveColor()
                self.wrongChangeVersionColor()

        else:
            cmds.warning("only 4 Members , example:0001")
            self.wrongChangeSaveColor()
            self.wrongChangeVersionColor()


    def artistField(self, *args):
        queryTextArtistField=cmds.textField('artistField', text=True, q=True)
        cleanArtistField = cmds.text('resultArtist', e = True)

        #query_color_value
        queryColorNameField = cmds.text('resultName', bgc=True,q = True)
        queryColorDepartmentField = cmds.text('resultDepartment', bgc=True,q = True)
        queryColorFaktorField = cmds.text('resultFaktor', bgc=True,q = True)
        queryColorVersionField = cmds.text('resultVersion', bgc=True,q = True)

        len_queryArtistField=len(queryTextArtistField)
        lowerqueryTextArtistField = queryTextArtistField.lower()
        if len_queryArtistField==2:
            for artist in queryTextArtistField:
                cmds.text('resultArtist', e = True, label=lowerqueryTextArtistField)
                self.changeArtistColor()
                if queryColorNameField[0]<0.4:
                    if queryColorDepartmentField[0]<0.4:
                        if queryColorFaktorField[0]<0.4:
                            if queryColorVersionField[0]<0.4:
                                self.changeColors()
                                cmds.select(clear=True)
        else:
            cmds.warning("only the first member of your nick and surname, example: Max Muster= mm")
            self.wrongChangeSaveColor()
            self.wrongChangeArtistColor()



    def upversion(self, *args):
        querySceneName=cmds.file(sceneName=True, q=True)



    def changeColors(self, *args):
        changeColor=cmds.button('save', e=True,bgc=(0.3,0.7,0.3))

    def changeNameColor(self, *args):
        changeNamecolor=cmds.text('resultName', e = True, bgc=(0.3,0.6,0.3))

    def changeDepartmentColor(self, *args):
        changeNamecolor=cmds.text('resultDepartment', e = True, bgc=(0.3,0.6,0.3))

    def changeFaktorColor(self, *args):
        changeFaktorColor=cmds.text('resultFaktor', e = True, bgc=(0.3,0.6,0.3))

    def changeVersionColor(self, *args):
        changeVersionColor=cmds.text('resultVersion', e = True, bgc=(0.3,0.6,0.3))

    def changeArtistColor(self, *args):
        changeArtistColor=cmds.text('resultArtist', e = True, bgc=(0.3,0.6,0.3))

    def wrongChangeVersionColor(self, *args):
        wrongChangeVersionColor=cmds.text('resultVersion', e = True, bgc=(0.6,0.3,0.3))


    def wrongChangeArtistColor(self, *args):
        wrongChangeVersionColor=cmds.text('resultArtist', e = True, bgc=(0.6,0.3,0.3))


    def wrongChangeFaktorColor(self, *args):
        wrongChangeFaktorColor=cmds.text('resultFaktor', e = True, bgc=(0.6,0.3,0.3))


    def wrongChangeNameColor(self, *args):
        wrongChangeNameColor=cmds.text('resultName', e = True, bgc=(0.6,0.3,0.3))

    def wrongChangeDepartmentColor(self, *args):
        wrongChangeDepartmentColor=cmds.text('resultDepartment', e = True, bgc=(0.6,0.3,0.3))

    def wrongChangeSaveColor(self, *args):
        changeColorAfterSave=cmds.button('save', e=True,bgc=(0.6,0.3,0.3))


    def dontSave(self, *args):
        cmds.warning("Dont Save!")
        if cmds.window("saveQuestion", exists=True):
            cmds.deleteUI("saveQuestion")

    def debug(self, *args):
        if cmds.window("Debug", exists=True):
            cmds.deleteUI("Debug")
        debug_windows = cmds.window("Debug",title="Debug Info",mnb=True, mxb=False,w=400,h=130,sizeable=False)
        debug_layout = cmds.columnLayout(w = 250, h=160, columnAttach=('both', 0), rowSpacing=5, columnWidth=250)
        cmds.separator(h=5,vis=True, st='none')
        debug_text = cmds.text(label="Please describe your problem or suggestion.")
        debug_text_field = cmds.textField('debugTextField',h=20,text = "")
        debug_button = cmds.button(label="Send to Admin",bgc=(0.7,0.2,0.3),command=self.sendDebug)
        cmds.showWindow()

    def sendDebug(self, *args):
        query_debug_text = cmds.textField('debugTextField', text=True, query=True)
        file = open("Y:/Production/rnd/ahosseini/helga_debug_clean_save/helga_debug_file.txt", "a")
        file.write("//New Bug:"+query_debug_text+"//\n")
        file.close()
        warning = cmds.warning("successful sending to Arash")
        if cmds.window("Debug", exists=True):
            cmds.deleteUI("Debug")

    def saveLogFile(self, *args):
        query_last_save_info = cmds.text('savedFile', label= True, query = True)
        query_last_save_path = cmds.text('savedPath', label =True, query = True)
        file = open("Y:/Production/rnd/ahosseini/helga_save_log_file/helga_save_file.txt", "a")
        file.write("[saved_file: "+ query_last_save_info +""+ query_last_save_path +"]\n")
        file.close()

    def overWriteFile(self):
        if cmds.window("saveQuestion", exists=True):
            cmds.deleteUI("saveQuestion")

        save_question=cmds.window("saveQuestion",title="are you sure?",mnb=True, mxb=False,w=250,h=130,sizeable=False)
        overwrite_layout=cmds.columnLayout(w = 100, h=160, columnAttach=('both', 0), rowSpacing=5, columnWidth=200)
        cmds.separator(h=5,vis=True, st='none')
        overwrite_text=cmds.text(label="Overwrite File?", align="center")
        cmds.separator(h=5, vis=True, st='none')
        button_overwrite_no=cmds.button(label="Dont Save",bgc=(0.3,0.5,0.3), h=30, command=self.dontSave)
        button_overwrite_yes=cmds.button(label="Yes, Overwrite exists File",bgc=(0.7,0.2,0.3),h=30, command=self.saveSceneOverwrite)
        cmds.showWindow()

    def cleanTextFields(self, *args):
        cleanNameField=cmds.textField('nameField', e = True, text="")
        cleanFaktorField=cmds.textField('faktorField', e = True, text="")
        cleanVersionField=cmds.textField('versionField', e = True, text="")
        cleanArtistField=cmds.textField('artistField', e = True, text="")

    def sceneCheck(self, *args):
        scene_full_name = cmds.file(sceneName = True, q=True)
        scene_name = scene_full_name.split("/")[-1]
        if scene_full_name == "":
            cmds.warning("save the File!")
        else:
            if ('_') in scene_name:
                if scene_full_name.startswith("//bigfoot/grimmhelga/Production/3d/maya/scenes/") or ("//bigfoot/grimmhelga/Production/rnd/"):
                    self.scene_full_path = os.path.dirname(scene_full_name)
                    #print self.scene_full_path
                    #scene name
                    self.scene_name = scene_full_name.split("/")[-1]

                    #check the artist name
                    artist_name = self.scene_name.split("_")[-1]
                    #print len(artist_name)
                    #print artist_name

                    #version check
                    self.version_check = self.scene_name.split("_")[-2]

                    #path check
                    #self.path_check = scene_full_name.split("/")[7]


                    #faktor check
                    faktor_check = self.scene_name.split("_")[-3]

                    #debug
                    #print self.path_check
                    #print self.scene_name
                    #print self.version_check

                    upversion_version_number = ["0","1","2","3","4","5","6","7","8","9"]
                    upversion_faktor=["a","b","c","d","e","f","g",
                                        "h","j","i","k","l","m","n",
                                        "o","p","q","r","s","t",
                                        "u","v","w","x","y","z"]

                    if len(self.version_check) == 4:                                        #version len check
                        if self.version_check[0] in upversion_version_number:               #version member check
                            if self.version_check[1] in upversion_version_number:
                                if self.version_check[2] in upversion_version_number:
                                    if self.version_check[3] in upversion_version_number:
                                        if len(faktor_check) == 1:
                                            if faktor_check[0] in upversion_faktor:
                                                if len(artist_name) == 5:
                                                    len_version_check = len(self.version_check)
                                                    while self.version_check.startswith("0"):
                                                        self.version_check = self.version_check[1:]
                                                    version = eval(self.version_check)
                                                    version += 1
                                                    self.version_check = str(version)
                                                    self.version_check = "0"*len_version_check + self.version_check
                                                    self.version_check = self.version_check[-len_version_check:]
                                                    #print self.version_check
                                                    self.upversion()
                                                    warning_text = str("File is clean and saved on: ") + str(self.scene_full_path) +str("/")+ str(self.new_file_name)
                                                    cmds.warning(warning_text)
                                                else:
                                                    cmds.warning("more as two Members for Artist name")
                                            else:
                                                cmds.warning("only alphabet member, a,b,c...")
                                        else:
                                            cmds.warning("more as one Member for Faktor name")
                                    else:
                                        cmds.warning("only numbers for Version  1,2,3...")
                                else:
                                    cmds.warning("only numbers for Version  1,2,3... ")
                            else:
                                cmds.warning("only numbers for Version  1,2,3...")
                        else:
                            cmds.warning("only numbers for Version 1,2,3...")
                    else:
                        cmds.warning("Version have to be four Members")
                else:
                    cmds.warning("Path not clean")
            else:
                cmds.warning("Scene Name not clean")


    def upversion(self, *args):
        split_scene_name = self.scene_name.split("_")
        split_scene_name[-2] = self.version_check
        self.new_file_name = "_".join(split_scene_name)
        #print ("new File name: ") + new_file_name
        #print self.fileName
        save_scene=cmds.file(rename=(self.scene_full_path+'/'+self.new_file_name))
        cmds.file( save=True, type='mayaBinary')
        #showSavedFile
        cleanartistField = cmds.text('savedFile', e = True)
        now = time.localtime(time.time())
        for save in self.new_file_name:
            cmds.text('savedFile', e=True, label=self.new_file_name + time.strftime("  %y/%m/%d %H:%M", now), bgc=(0.3,0.5,0.3))

        cmds.text('savedPath', e=True, label=self.scene_full_path)
        self.saveLogFile()

    def saveSceneOverwrite(self, *args):
        queryNameField=cmds.text('resultName', label=True, q=True)
        queryDepartmentField=cmds.text('resultDepartment', label=True, q=True)
        queryFaktorField=cmds.text('resultFaktor', label=True, q=True)
        queryVersionField=cmds.text('resultVersion', label=True, q=True)
        queryArtistField=cmds.text('resultArtist', label=True, q=True)

        #save_query_action
        queryColorSave=cmds.button('save', bgc=True, q=True)
        queryDepField=cmds.optionMenu('depField',q=True,value=True)[0]

        if queryDepField =="0":
            savedFileResult=str(queryNameField)+"_"+str(queryFaktorField)+"_"+str(queryVersionField)+"_"+str(queryArtistField)+".mb"
            if queryColorSave[0]<0.4:
                if cmds.window("saveQuestion", exists=True):
                    cmds.deleteUI("saveQuestion")

                # DEBUG
                #print self.fileName
                #print savedFileResult
                # DEBUG ENDE

                save_scene=cmds.file(rename=(self.fileName+'/'+savedFileResult))
                cmds.file( save=True, type='mayaBinary')

                #showSavedFile
                cleanartistField = cmds.text('savedFile', e = True)
                now = time.localtime(time.time())
                for save in savedFileResult:
                    cmds.text('savedFile', e=True, label=savedFileResult + time.strftime("  %y/%m/%d %H:%M", now), bgc=(0.3,0.5,0.3))

                #show_saved_path
                cmds.text('savedPath', e=True, label=self.fileName)

                self.wrongChangeArtistColor()
                self.wrongChangeFaktorColor()
                self.wrongChangeDepartmentColor()
                self.wrongChangeNameColor()
                self.wrongChangeVersionColor()
                self.wrongChangeSaveColor()
                self.cleanTextFields()
                self.saveLogFile()
                cmds.warning("Successful Saving on "+self.fileName)

            else:
                cmds.warning("Dont Save!!! need more info")


        else:
            #savedFile_as maya_binary
            savedFileResult=str(queryNameField)+"_"+str(queryDepartmentField)+"_"+str(queryFaktorField)+"_"+str(queryVersionField)+"_"+str(queryArtistField)+".mb"
            if queryColorSave[0]<0.4:
                if cmds.window("saveQuestion", exists=True):
                    cmds.deleteUI("saveQuestion")

                # DEBUG
                #print self.fileName
                #print savedFileResult
                # DEBUG ENDE

                save_scene=cmds.file(rename=(self.fileName+'/'+savedFileResult))
                cmds.file( save=True, type='mayaBinary')

                #showSavedFile
                cleanartistField = cmds.text('savedFile', e = True)
                now = time.localtime(time.time())
                for save in savedFileResult:
                    cmds.text('savedFile', e=True, label=savedFileResult + time.strftime("  %y/%m/%d %H:%M", now), bgc=(0.3,0.5,0.3))

                #show_saved_path
                cmds.text('savedPath', e=True, label=self.fileName)

                self.wrongChangeArtistColor()
                self.wrongChangeFaktorColor()
                self.wrongChangeDepartmentColor()
                self.wrongChangeNameColor()
                self.wrongChangeVersionColor()
                self.wrongChangeSaveColor()
                self.cleanTextFields()
                self.saveLogFile()
                cmds.warning("Successful Saving on "+self.fileName)

            else:
                cmds.warning("Dont Save!!! need more info")

    def file_path(self, fileName, fileType):


        queryNameField=cmds.text('resultName', label=True, q=True)
        queryDepartmentField=cmds.text('resultDepartment', label=True, q=True)
        queryFaktorField=cmds.text('resultFaktor', label=True, q=True)
        queryVersionField=cmds.text('resultVersion', label=True, q=True)
        queryArtistField=cmds.text('resultArtist', label=True, q=True)

        self.fileName = fileName

        #savedFile_as maya_binary
        queryDepField=cmds.optionMenu('depField',q=True,value=True)[0]
        if queryDepField=="0":
            savedFileResult=str(queryNameField)+"_"+str(queryFaktorField)+"_"+str(queryVersionField)+"_"+str(queryArtistField)+".mb"

            #print "selected Folder : " + self.fileName
            if ((os.path.exists(self.fileName+'/'+savedFileResult)==True)):
                cmds.warning(savedFileResult+" alredy exists")
                self.overWriteFile()
            else:
                self.saveSceneOverwrite()

        else:
            savedFileResult=str(queryNameField)+"_"+str(queryDepartmentField)+"_"+str(queryFaktorField)+"_"+str(queryVersionField)+"_"+str(queryArtistField)+".mb"

            #print "selected Folder : " + self.fileName
            if ((os.path.exists(self.fileName+'/'+savedFileResult)==True)):
                cmds.warning(savedFileResult+" alredy exists")
                self.overWriteFile()
            else:
                self.saveSceneOverwrite()


    def saveScene(self, *args):

        #save_query_action
        queryColorSave=cmds.button('save', bgc=True, q=True)

        #save_action_function
        if queryColorSave[0]<0.4:
            cmds.fileBrowserDialog( m=4, fc=self.file_path, an='Choose folder to Save', om="Nein" )
        else:
            cmds.warning("Please set a new File-Data")

#run
#----------------------------------------------------------
#----------------------------------------------------------
def run():
    cleanSave_UI()







#test
#----------------------------------------------------------
#----------------------------------------------------------

if(__name__ == '__main__'):
    cleanSave_UI()
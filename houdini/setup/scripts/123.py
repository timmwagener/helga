


#helga 123.py (startup procedures only executed when opened without hip file)
#------------------------------------------------------------------





#Run houdini 123 default setup
#------------------------------------------------------------------

try:

    #default houdini startup when opened without hip file
    import hou
    hou.hscript("source 123.cmd")

    #SuccessMsg
    print('Successfully executed 123.cmd')

except:
    
    #FailMsg
    print('Failed to execute 123.cmd')
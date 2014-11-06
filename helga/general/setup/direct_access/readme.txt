

-----------------------------------------------------------------------
Quick guide on how to use the direct_access module:
-----------------------------------------------------------------------


1.
----------------------------------------------------------------------- 
Go into the yaml/pipeline_base_data.yaml and adjust the pathes as needed for your environment


2.
----------------------------------------------------------------------- 
PIPELINE_BASE_PATH: "//bigfoot/grimmhelga" 
This is the path to the folder that contains the Production and Organization folder

PIPELINE_FLAVOUR: "deploy" 
This is the folder name where the script environment is located in. This should never be "work", instead names like "sandbox" or "deploy"
are common

The other values point to the executables you want to use of Maya, Houdini and Nuke.
You dont need to have all of them. The preferred versions are:

Maya 2014
Houdini 13.0.547
NukeX8.05


3.
-----------------------------------------------------------------------
Navigate the shell to your direct_access package and run the following command:

python -c 'import direct_access;reload(direct_access);direct_access.run("houdini")'

Possible parameters are:

#. maya
#. houdini
#. nuke

The module should not have any dependencies apart from builtin modules, however if you have
the yaml package installed, it will use it.


4.
-----------------------------------------------------------------------
It is important that you use the folder structure provided in the supplementary_material/folder_structure folder.
Go into this folder, copy the Production and Organization folders to wherever you like and point the
PIPELINE_BASE_PATH to it.

For example if you copy to:
C:/my/pipeline/root/path then the PIPELINE_BASE_PATH variable would be "C:/my/pipeline/root/path"


5.
-----------------------------------------------------------------------
Clone the helga repo into PIPELINE_BASE_PATH + /Production/scripts/work/helga.
Copy this repo into PIPELINE_BASE_PATH + /Production/scripts/sandbox/helga and PIPELINE_BASE_PATH + /Production/scripts/deploy/helga.

Work will always be safe for pulling and never have locked plugin handles and such.
Sandbox and deploy are used in production.
Always create, write, push and pull in work and copy/deploy to sandbox or deploy.
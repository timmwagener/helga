
helga
=====

<div align="center">
	<a href="http://helga-docs.readthedocs.org/" target="_blank"><img src="http://www.kiiia.com/helga/images/github_readme_header.jpg"></a>
</div>

=====
[![Documentation Status](https://readthedocs.org/projects/helga-docs/badge/?version=latest)](https://readthedocs.org/projects/helga-docs/?badge=latest)
=====

Pipeline repo for our diploma movie with the working title "Helga". Contains the script environment for the whole project.

The currently involved DCCs are
	
	* Houdini
	* Maya
	* Nuke

Use it like this

	import sys
	sys.path.append(Path_to_helga_package)

	from helga.houdini.animation import my_tool

You can find the pipeline documentation [here](http://helga-docs.readthedocs.org/).



.. _apidoc_coding_convention:

.. 
	Coding convention for our pipeline



Coding Convention
=================

If you want to contribute to our pipeline, please let me know.
There is a place for these efforts and i will try to support you with that.
In return you are expected to follow our **coding standards** in order for your
code to integrate consistently with the codebase and make it easier for
everybody.

**Our coding convention in one sentence:**

	Do it as in :PEP:`8` or :PEP:`257` and name your objects as in the `Google Python Convention <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Naming>`_.

------------------------

.. warning::

	The current codebase contains large portions of legacy code. While still functional
	it was created before the coding conventions where active. This will be refactored
	over time.

------------------------



Important PEPs
--------------

There are a lot of PEPs. Some are more important than others. **You are expected to read and use them.** Often times in this document, i will just refer to the appropiate place in some PEP. 

	* Python Coding Style: :PEP:`8`
	* Docstring Conventions: :PEP:`257`

------------------------



Variables, Classes, Modules, Packages etc.
------------------------------------------

For naming of objects in Python we use the Google naming convention.
(:PEP:`8` does not recommend any naming).

::
	
	module_name, package_name, ClassName, method_name, ExceptionName, function_name,
	GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name,
	local_var_name.

You can find the full documentation `here <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Naming>`_.

------------------------



Tabs or spaces
--------------

:PEP:`8#tabs-or-spaces`
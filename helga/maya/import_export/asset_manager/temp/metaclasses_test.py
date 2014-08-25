





#Import
#------------------------------------------------------------------
import copy






#attr_to_create_dict
#------------------------------------------------------------------

attr_to_create_dict = {'worldSpace' : 1.0, 'startFrame' : 1}





#Metaclass test
#------------------------------------------------------------------


class TestMetaclass(type):
	"""
	Metaclass to test around.
	"""

	def __new__(meta, cls_name, base_tuple, attr_dict):
		"""
		Metaclass new. Return class object.
		"""

		print('Meta class: {0}'.format(meta))
		print('Class name: {0}'.format(cls_name))
		print('Base tuple: {0}'.format(base_tuple))

		for key, value in attr_dict.iteritems():

			print('{0} - {1}'.format(key, value))
		

		#attr_dict_customized
		attr_dict_customized = copy.deepcopy(attr_dict)

		for attr_name, default_value in attr_to_create_dict.iteritems():

			#get
			attr_dict_customized['get_'+attr_name] = getter_function_factory(attr_name)
			#set
			attr_dict_customized['set_'+attr_name] = setter_function_factory(attr_name)

		#meta_class_parent
		meta_class_parent = super(TestMetaclass, meta)

		return meta_class_parent.__new__(meta, cls_name, base_tuple, attr_dict_customized)



def getter_function_factory(attr):
	"""
	Return getter function based on input
	"""

	def wrapped_func(*args, **kwargs):
		"""
		Wrapped func
		"""

		print('Wrapped getter func start')

		self = args[0]

		value = getattr(self, attr)

		print('Wrapped getter func end')

		return value

	return wrapped_func


def setter_function_factory(attr):
	"""
	Return setter function based on input
	"""

	def wrapped_func(*args, **kwargs):
		"""
		Wrapped func
		"""

		print('Wrapped setter func start')

		self = args[0]
		value = args[1]

		setattr(self, attr, value)

		print('Wrapped setter func end')

	return wrapped_func



#Class
#------------------------------------------------------------------

class Test(object):
	"""
	Test class that is built by TestMetaclass.
	"""

	__metaclass__ = TestMetaclass

	def __init__(self, test = 5):
		"""
		Instance customization.
		"""

		self.test = test

		code_object = compile("self.x = 'sick_shit'", '<string>', 'exec')
		exec(code_object)

		#iterate and create instance attrs.
		self.worldSpace = 5
		self.startFrame = 10

	def print_test(self):
		"""
		Print test.
		"""

		print(self.test)







#Run
#------------------------------------------------------------------

def run():
	"""
	Run method
	"""

	pass







#Execute if main
#------------------------------------------------------------------

if(__name__ == '__main__'):

	test_instance_a = Test()
	test_instance_a.print_test()
	print(test_instance_a.worldSpace)
	print(test_instance_a.startFrame)
	print(test_instance_a.x)


	for member in dir(test_instance_a):
		print('{0} - {1}'.format(type(member), member))



	test_instance_b = Test()
	test_instance_b.set_worldSpace(33, 'huso', penis_priester = 'schlomo')


	print(test_instance_a.worldSpace)
	print(test_instance_b.worldSpace)

	print(test_instance_a.get_worldSpace())
	print(test_instance_b.get_worldSpace())
















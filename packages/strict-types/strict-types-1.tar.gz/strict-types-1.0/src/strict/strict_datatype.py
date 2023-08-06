from .exceptions import AssignError

def strict_datatype(func):
	""" strict_datatype is a decorator that will check the desired datatypes of a function and compare with its
	parameters datatypes. """

	def wrap(*args, **kwargs):

		# Go through every argument of the function (in order).
		for n, arg in enumerate(func.__code__.co_varnames):

			# Store the parameter datatype, being it an argument or a keyword argument.
			compare_type = type(kwargs[arg]) if arg in kwargs else type(args[n])

			# Ignore if the argument doesn't have any annotation. Otherwise, compare the annotation datatype with that of the parameter. If it doesn't match, raise an exception.
			if arg in func.__annotations__ and not compare_type in (func.__annotations__[arg].__args__ if '__args__' in dir(func.__annotations__[arg]) else (func.__annotations__[arg],)):
				raise AssignError(
					'Trying to assign an invalid datatype to the parameter "%s". Datatype must be %s, and not %s.'
					% (arg, func.__annotations__[arg] if not '__args__' in dir(func.__annotations__[arg]) else " or ".join([str(t) for t in func.__annotations__[arg].__args__]), compare_type),
					parameter=arg, required=func.__annotations__[arg].__args__ if '__args__' in dir(func.__annotations__[arg]) else (func.__annotations__[arg],), invalid=compare_type,
				)

		return func(*args, **kwargs)
	return wrap
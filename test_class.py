import inspect

#
# this is an example class.
# in order to manufacture deep copies of each object to give full functionality, ALL VARIABLES NEED
# GETTER AND SETTER METHODS. Without them, the objects are not usable.
#
# During the serialization process, it helps to have a method to automatically set fields from the dictionary.
#
class test_class:
    def __init__(self, arg1, arg2):
        if type(arg1) is dict:
            # sets all the instance variables in the class method
            self.construct_from_dictionary(arg1)
        else:
            self.num1 = arg1
            self.num2 = arg2
            self.num3 = None

    @classmethod
    def construct_from_dictionary(cls, dictionary):

        values = []
        for key in dictionary:
            values.append(dictionary[key])

        constructor_arg_length = len(inspect.signature(cls.__init__).parameters)

        # new object of this class
        obj_ = cls(values[0], values[1])

        # notice how these don't have the parenthesis around them. This is because instead of storing method calls,
        # the program dynamically uses setter methods depending on the signature of the constructor! how cool.
        field_setters = [
            cls.set_num1,
            cls.set_num2,
            cls.set_num3
        ]

        # in testing I noticed there was an order of potentially redundant setter methods,
        # since the constructor often directly assigns data to some instance variables it's necessary to
        # grab the number of setter methods, and only execute the setter methods for variables that are not in the
        # signature of the constructor.
        try:
            for x in range(len(field_setters)):
                if x > constructor_arg_length:
                    field_setters[x].__call__(values[x])
        except IndexError:
            print(Warning("<<< INDEX MISMATCH >>>"))
        return obj_

    # generic getter-setter methods
    def get_num1(self):
        return self.num1

    def get_num2(self):
        return self.num2

    def get_num3(self):
        return self.num3

    def set_num1(self, num1):
        self.num1 = num1

    def set_num2(self, num2):
        self.num2 = num2

    def set_num3(self, num3):
        self.num3 = num3

    # makes a call to a constructor-like method that returns a new object copy from the dictionary.
    def deserialize(self, dictionary):
        return self.construct_from_dictionary(dictionary)

    # serialize instance variables to dictionary object
    def serialize(self):
        obj_ = {
            'num1': self.num1,
            'num2': self.num2,
            'num3': self.num3
        }
        return obj_
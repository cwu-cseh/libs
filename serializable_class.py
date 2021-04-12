import importlib
import inspect

#
# TLDR: cool stuff
#
# in order to transfer objects from one application to the next, it's necessary to get all the fields of an object to
# produce a deep-ish copy of an object. For example, if you wanted to copy a java object and pass it to a wrapper in
# python, you would first need to format that data, read off it's data, know the constructor parameters, etc. This makes
# it all easy. With some adaptation, even your own custom classes can be called, and used in an abstract manor. The
# driver class class_list, doesn't need to know what class object it is, only it's name, then it returns an object that
# can be manipulated in the parent program.
#
# using some clever object manipulation it's possible to identify, use, and instantiate class objects without knowing
# what the file name is, or what method is it's constructor. This allows for ambiguous class object serialization and
# deserialization using a transport mechanism like json-rpc using a simple dictionary.
#
# once this object is received through the transport mechanism, the dictionary containing class fields is
class serializable_class:
    def __init__(self, name):
        self.name = name
        self.cls = importlib.import_module(name, None)
        # the below methods need to be implemented in any imported file used as a class.
        self.constructor = self.cls.__getattribute__(name)
        # self.serializer = self.constructor.__getattribute__('serialize')
        # to create an object of the imported module, use
        # obj = self.cls.serializer()

    # gets the name of the class
    def get_name(self):
        return self.name

    # returns a class object
    def get_class(self):
        return self.cls

    # constructs an object of the class and returns it.
    def construct(self, *args):
        return self.constructor(*args)

    # returns signature of the constructor
    def get_constructor_signature(self):
        return inspect.signature(self.constructor)

    # returns arguments of the constructor of the class using inspect.
    def get_constructor_args(self):
        return inspect.signature(self.constructor).parameters

    # gets class methods using inspect
    def get_class_methods(self):
        return inspect.getmembers(self.cls)

    # constructs object of the a class, and returns an object of that class.
    def construct_from_dictionary(self, dictionary):
        return self.constructor.construct_from_dictionary(dictionary)


'''
if __name__ == '__main__':
    new = serializable_class("serializer")
    other = new.new('testing')
    print(other)
    # print(other.print_string()
    # other.print_string()
'''
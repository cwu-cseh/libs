import serializable_class
import os
'''
Author: Alias
         ^^ AKA blackinkcyber

driver class that collects and dispatches calls to class objects.

for an example implementation of a class, see test_class.py it implements just about all you may need in a non-trivial
class. like a message or a cryptocurrency wallet, etc.

'''


class class_list:
    def __init__(self):
        self.class_lst = self._parse_dir()
        self.classes = self._parse_classes()

    # parses the file list, then returns what they are called so they can be imported, and called.
    def _parse_classes(self):
        classes_ = []
        for x in range(len(self.class_lst)):
            classes_.append(serializable_class.serializable_class(self.class_lst[x]))
        return classes_

    # nabs all the python files not used in the current directory, and adds them to a list of meta classes that can
    # be instantiated using the .construct(*args) method.
    def _parse_dir(self):
        file_list = os.listdir()
        class_lst = []
        for x in range(len(file_list)):
            name = file_list[x]
            # to ignore backbone python files from potential instantiation
            if name != 'class_list.py' and name != '__init__.py' and name != '__pycache__' and \
                    name != 'serializable_class.py':
                class_lst.append(file_list[x][0:-3])
        return class_lst

    def get_object(self, name, *args):
        # print(type(self.get_class(name)))
        return self.get_class(name).construct_from_dictionary(*args)

    # searches the class list for a key 'name' and returns the class if it exists in the list.
    def get_class(self, name):
        for x in range(len(self.classes)):
            if self.classes[x].get_name() == name:
                return self.classes[x]

    # once received, the program needs to know the class destination for the new object.
    # this is the name key. without it we can't know what object is to be created.
    #
    # The name key is stripped from the dictionary, and the new dictionary is passed to the
    # generate from dictionary method in the serializable_class.
    def deserialize(self, dictionary):
        obj_ = self.get_object(dictionary['name'], dictionary)
        name_stripped_dict = dict(list(dictionary.items())[1:])
        return obj_.deserialize(name_stripped_dict)


if __name__ == '__main__':
    cls = class_list()
    dictionary = {
        'name': 'test_class',
        'var1': 69,
        'var2': 420
    }

    obj1_ = cls.deserialize(dictionary)
    print('object in memory:')
    print(obj1_)
    print('calling class methods: ')
    print(obj1_.get_num1())
    print(obj1_.get_num2())
    print('\n')

    dictionary2 = {
        'name': 'test_class',
        'var1': 666,
        'var2': 777
    }

    obj2_ = cls.deserialize(dictionary2)
    print('object in memory:')
    print(obj2_)
    print('calling class methods: ')
    print(obj2_.get_num1())
    print(obj2_.get_num2())

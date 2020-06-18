# -*- encoding:utf-8 -*-


class Foo(object):
    def __init__(self, name):
        self._name = name

    @property
    def get_name(self):
        return self._name

    # noinspection PyPropertyDefinition
    @get_name.setter
    def set_name(self, value):
        if not isinstance(value, str):
            raise TypeError("%s must be str" % value)
        self._name = value


f = Foo("Linda")
print(f.get_name)
f.set_name = "Christina"
print(f.get_name)
f.set_name = "Elva"
print(f.get_name)

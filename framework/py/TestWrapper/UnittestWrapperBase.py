import types
from unittest import *
from unittest import mock

mock = mock

class TestCase(TestCase):
    def add_wrapper(self, name):
        func = getattr(self, name)

        def patched(self, *args, **kwargs):
            with wrap_class(name=name):
                return func()

        setattr(self, name, types.MethodType(patched, self))

    def __init__(self, *args, **kwargs):
        reference = super()
        for name in dir(self):
            if name.startswith("test_") and isinstance(getattr(self, name), type(self.__init__)) and not hasattr(reference, name):
                self.add_wrapper(name)
        super().__init__(*args, **kwargs)


wrap_object_map = dict()


class WrapClass:
    def __init__(self, name="method"):
        self.name = name

    def __enter__(self):
        print("Entering {a}!".format(a=self.name))

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Leaving {a}!".format(a=self.name))


wrap_class = WrapClass

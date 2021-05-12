import inspect
import os
import types
from unittest import *

from WrapClass import WrapClass

wrap_class = WrapClass


class TestCase(TestCase):
    def add_wrapper(self, name):
        func = getattr(self, name)

        def patched(*args, **kwargs):
            with wrap_class(name):
                return func()

        setattr(self, name, types.MethodType(patched, self))

    def __init__(self, *args, **kwargs):
        reference = super()
        for name in dir(self):
            if name.startswith("test_") and isinstance(getattr(self, name), type(self.__init__)) and not hasattr(
                    reference, name):
                self.add_wrapper(name)
        super().__init__(*args, **kwargs)


def pytest_wrapper(func):
    def patched(*args, **kwargs):
        with wrap_class(os.path.abspath(inspect.getfile(func)) + "::" + func.__name__):
            func(*args, **kwargs)
    return patched


def pytest_runtest_setup(item):
    if item.obj.__name__ != "patched":
        item.obj = pytest_wrapper(item.obj)

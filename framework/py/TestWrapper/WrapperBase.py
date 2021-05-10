import os
import types
from unittest import *
from unittest import mock

mock = mock


class TestCase(TestCase):
    def add_wrapper(self, name):
        func = getattr(self, name)

        def patched(*args, **kwargs):
            with wrap_class(name=name):
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
        with wrap_class(repr(func)):
            func(*args, **kwargs)

    return patched


class WrapClass:
    def __init__(self, name="method"):
        self.name = name
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        os.system('echo "{num}" > nums.txt'.format(num=self.calls))
        return WrapClass(str(args[0] if len(args) > 0 else "method"))

    def __enter__(self):
        # print("Entering {a}!".format(a=self.name))
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Leaving {a}!".format(a=self.name))


wrap_class = WrapClass()


def pytest_runtest_call(item):
    def pytest_wrapper(func):
        def patched(*args, **kwargs):
            with wrap_class(repr(func)):
                func(*args, **kwargs)

        return patched

    item.obj = pytest_wrapper(item.obj)

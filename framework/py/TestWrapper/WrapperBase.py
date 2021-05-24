import types
from unittest import *

from WrapClass import debugger, test_id

def pytest_wrapper(func, collect_fail=True):
    def patched(*args, **kwargs):
        collector = debugger.collector_class()
        try:
            with collector:
                func(*args, **kwargs)
            debugger.add_collector(debugger.PASS, collector)
        except Exception as e:
            if collect_fail:
                debugger.add_collector(debugger.FAIL, collector)
            raise e

    setattr(patched, "patched_flag", True)
    return patched


class TestCase(TestCase):
    def add_wrapper(self, name):
        func = getattr(self, name)
        if not hasattr(func, "patched_flag"):
            setattr(self, name, types.MethodType(pytest_wrapper(func), self))

    def __init__(self, *args, **kwargs):
        reference = super()
        for name in dir(self):
            if name.startswith("test_") and isinstance(getattr(self, name), type(self.__init__)) and not hasattr(
                    reference, name):
                self.add_wrapper(name)
        super().__init__(*args, **kwargs)


def pytest_runtest_setup(item):
    if item.obj.__name__ != "patched":
        item.obj = pytest_wrapper(item.obj, item.nodeid.split("[")[0] == test_id)

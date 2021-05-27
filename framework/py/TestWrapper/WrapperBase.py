import types
from unittest import *
import signal

from WrapClass import debugger, test_id

TEST_TIMEOUT = 15  # seconds


class FunctionTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise FunctionTimeout()


def test_wrapper(func, collect_fail=True, pass_args=True):
    def patched(*args, **kwargs):
        collector = debugger.collector_class()
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(TEST_TIMEOUT)
        try:
            if pass_args:
                with collector:
                    ret = func(*args, **kwargs)
            else:
                with collector:
                    ret = func()
            signal.alarm(0)
            debugger.add_collector(debugger.PASS, collector)
            return ret
        except Exception as e:
            signal.alarm(0)
            if collect_fail and not isinstance(e, FunctionTimeout):
                debugger.add_collector(debugger.FAIL, collector)
            raise e
        finally:
            signal.alarm(0)

    setattr(patched, "patched_flag", True)
    return patched


class TestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        debugger.teardown()

    def add_wrapper(self, name):
        func = getattr(self, name)
        if not hasattr(func, "patched_flag"):
            setattr(self, name, types.MethodType(test_wrapper(func, True, False), self))

    def __init__(self, *args, **kwargs):
        reference = super()
        for name in dir(self):
            if name.startswith("test_") and isinstance(getattr(self, name), type(self.__init__)) and not hasattr(
                    reference, name):
                self.add_wrapper(name)
        super().__init__(*args, **kwargs)


def pytest_runtest_setup(item):
    if item.obj.__name__ != "patched":
        item.obj = test_wrapper(item.obj, item.nodeid.split("[")[0] == test_id)


def pytest_sessionfinish(session, exitstatus):
    debugger.teardown()

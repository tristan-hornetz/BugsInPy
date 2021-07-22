import types
from unittest import *
import signal
import subprocess
import os

from WrapClass import debugger, test_ids

TEST_TIMEOUT = 45  # seconds


class FunctionTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    sp = subprocess.Popen(['ps', '-opid', '--no-headers', '--ppid', str(os.getpid())], encoding='utf8')
    child_process_ids = [int(line) for line in sp.stdout.read().splitlines()]
    for child in child_process_ids:
        os.kill(child, signal.SIGTERM)
    raise FunctionTimeout()


def pytest_item_id_matches(node_id: str):
    item_name = node_id.split("[")[0]
    if item_name in test_ids:
        return True
    if item_name.replace("::()", "") in test_ids:
        return True
    if item_name.replace("()", "") in test_ids:
        return True
    return False


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
            ref_name = f"{func.__module__}.{self.__class__.__name__}.{func.__name__}"
            collect_failure = len(test_ids) == 0
            for test_id in test_ids:
                collect_failure = collect_failure or str(test_id).endswith(ref_name)
            setattr(self, name, types.MethodType(test_wrapper(func,  collect_failure, False), self))

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        self = obj
        reference = super()
        for name in dir(self):
            if name.startswith("test_") and isinstance(getattr(self, name), type(self.__init__)) and not hasattr(
                    reference, name):
                self.add_wrapper(name)
        return obj


def pytest_runtest_call(item):
    if item.obj.__name__ != "patched":
        item.obj = test_wrapper(item.obj, pytest_item_id_matches(item.nodeid) or len(test_ids) == 0)


def pytest_sessionfinish(session, exitstatus):
    if not hasattr(debugger, "teardown_successful"):
        debugger.teardown()
        setattr(debugger, "teardown_successful", True)

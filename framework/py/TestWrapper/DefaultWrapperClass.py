import os


class RankDumper:
    def __del__(self):
        if hasattr(self, "dump_file") and hasattr(self, "rank"):
            ranking = self.rank()
            if self.dump_file != "" and len(ranking) > 0:
                if os.path.isfile(self.dump_file):
                    os.remove(self.dump_file)
                with open(self.dump_file, "x") as f:
                    f.write(str(ranking))


class DefaultWrapperClass(RankDumper):
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return DefaultWrapperClass(str(args[0] if len(args) > 0 else "method") if "name" not in kwargs.keys() else
                                   kwargs["name"])

    def __init__(self, name="method"):
        self.name = name
        self.calls = 0
        self.FAIL = 'FAIL'
        self.PASS = 'PASS'
        self.collector_class = self.__call__

        def _pass(*args, **kwargs):
            pass

        self.add_collector = _pass
        self.rank = _pass
        self.teardown = _pass
        self.dump_file = ""

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


debugger = DefaultWrapperClass()
test_ids = []

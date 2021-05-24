import os


class RankDumper:
    def __del__(self):
        ranking = self.rank() if hasattr(self, "rank") else []
        if dump_file != "" and len(ranking) > 0:
            if os.path.isfile(dump_file):
                os.remove(dump_file)
            with open(dump_file, "x") as f:
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

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


debugger = DefaultWrapperClass()
test_id = ""
dump_file = ""

class DefaultWrapperClass:
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

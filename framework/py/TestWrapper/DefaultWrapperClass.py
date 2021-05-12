class DefaultWrapperClass:
    def __init__(self, name="method"):
        self.name = name
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return DefaultWrapperClass(str(args[0] if len(args) > 0 else "method"))

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Leaving {a}!".format(a=self.name))
        if exc_val is not None:
            print(exc_type)


WrapClass = DefaultWrapperClass()

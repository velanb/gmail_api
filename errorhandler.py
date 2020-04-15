class DBError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.methodName = args[1]
        else:
            self.message = None
            self.methodName = None

    def __str__(self):
        if self.message:
            return "DBError->Error at method{}, Error message>> {}".format(self.methodName, self.message)


class UtilError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.methodName = args[1]
        else:
            self.message = None
            self.methodName = None

    def __str__(self):
        if self.message:
            return "UtilError->Error at method{}, Error message>> {}".format(self.methodName, self.message)

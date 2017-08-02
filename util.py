import sys


class Trace(object):

    def __init__(self, indent, level):
        self.indent = indent
        self.level = level

    @property
    def indent(self):
        return self._indent

    @indent.setter
    def indent(self, v):
        self._indent = v

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, v):
        self._level = v

    def printwhite(self):
        tmp = self.indent
        while tmp > 0:
            print(' ', end='')
            tmp -= 1

    def log(self, *args, **kw):
        if self.level >= 1:
            self.printwhite()
            print("LOG> ", *args, **kw)

    def debug(self, *args, **kw):
        if self.level >= 2:
            self.printwhite()
            print("DEBUG> ", *args, **kw)

    def error(self, *args, **kw):
        self.printwhite()
        print("ERROR> ", *args, **kw)
        sys.exit()

    @staticmethod
    def trace(trace_obj=None):
        def _trace(func):
            def wrapper(*args, **kw):
                nonlocal trace_obj
                if trace_obj != None and trace_obj.level >= 2:
                    trace_obj.printwhite()
                    print('%s start' % (func.__name__))
                    trace_obj.indent += 2
                try:
                    r = func(*args, **kw)
                    return r
                finally:
                    if trace_obj != None and trace_obj.level >= 2:
                        trace_obj.indent -= 2
                        trace_obj.printwhite()
                        print('%s end' % (func.__name__))

            return wrapper
        return _trace

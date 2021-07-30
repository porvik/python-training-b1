import ctypes  # https://docs.python.org/3/library/ctypes.html
import os

lib = ctypes.cdll.LoadLibrary('{}/lib/lib_test.so'.format(os.path.dirname(__file__)))


class Test(object):

    def __init__(self):
        self.obj = lib.Test_new()

    def do_some_processing(self):
        print("Processing inside the Python code ...")
        lib.Test_do_some_processing(self.obj)


f = Test()
f.do_some_processing()

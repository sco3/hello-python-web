from python import Python, PythonObject


def main():
    try:
        # asdf_mod = Python.import_module("asdf.py")
        # var bv = asdf_mod
        Python.evaluate("asdf.a('1')")
    except:
        pass

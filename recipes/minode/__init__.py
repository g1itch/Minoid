"""python-for-android recipe for MiNode"""
from pythonforandroid.recipe import PythonRecipe


class MiNodeRecipe(PythonRecipe):
    url = 'https://github.com/g1itch/MiNode/archive/b044da57841e7d4ceafe4908c71b4714cf36c148.tar.gz'
    version = '0.3.0'
    md5sum = 'c7985c92bc4d6afce595d15cef321034'
    depends = ['setuptools']
    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = MiNodeRecipe()

from distutils.core import setup

import py2exe

 

setup(
console=[{"script": "proxy.py", "icon_resources": [(1, u"wangluo256.ico")] }]
)
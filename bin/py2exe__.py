from distutils.core import setup

import py2exe

 

setup(
console=[{"script": "proxy_v1.2.py", "icon_resources": [(1, u"wangluo256.ico")] }]
)
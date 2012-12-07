from distutils.core import setup
import py2exe,sys
setup(
    console=['bincr.py'],
    options={'py2exe':{
        'dist_dir':r'.',#E:\IMES\FTP',
#        'bundle_files':1,
##        'ascii':True,
        'excludes':['ssl','select'],
        'compressed':True}}
    )

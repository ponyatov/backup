from distutils.core import setup
import py2exe,os,sys
sys.argv+=['py2exe']
setup(
    console=['backup.py'],
options={'py2exe':{
		'dist_dir':r'D:\backup',
		'compressed':True,
		'bundle_files':1,
#		'ascii':True,
		'excludes':['_ssl','bz2']
		}},
	zipfile=None
    )
os.system('rm -rf build')
raw_input('.')

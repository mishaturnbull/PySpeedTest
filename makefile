compiler = pyinstaller
target = gui.py
upx = --upx-dir="C:/Program Files (x86)/upx394wce/"
spec = --specpath build
ver_major = 0
ver_minor = 5
ver_patch = 0

windows: 
	$(compiler) -w -F --icon=icon.ico -y -n PySpeedTest_$(ver_major).$(ver_minor).$(ver_patch).exe $(target)
windows-debug:
	$(compiler) -c -F -y -n PySpeedTest_$(ver_major).$(ver_minor).$(ver_patch)-TESTREL.exe $(target)
mac:
	$(compiler) -F -y -n PySpeedTest_$(ver_major).$(ver_minor).$(ver_patch)_MAC $(target)

preclean:
	del *.pyc;
postclean:
	del *.pyc; del urllib3; del PySpeedTest_*;

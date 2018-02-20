.RECIPEPREFIX +=
compiler = pyinstaller
target = gui.py
ver_major = 0
ver_minor = 5
ver_patch = 0

windows: 
	$(compiler) -w -F -n PyInstaller_$(ver_major).$(ver_minor).$(ver_patch).exe $(target)
	

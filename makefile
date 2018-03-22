.PHONY : main all os_check clean preclean postclean

compiler = pyinstaller
target = src/gui.py

ver_major = 2
ver_minor = 0
ver_patch = 0

hiddenimports = --hidden-import urllib3
hiddenimports += --hidden-import pyspeedtest

cflags = -F -y --specpath build --clean $(hiddenimports)

ifeq ($(OS),Windows_NT)
	name = PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch).exe
	cflags += --windowed
	delete_cmd = del /S
	delete_dir = rmdir /S /q
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Darwin)
		name = PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch)_mac
		cflags += --windowed
		delete_cmd = rm
		delete_dir = rm -rf
	else
		name = PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch)_unix
		cflags += -c
		delete_cmd = rm
		delete_dir = rm -rf
	endif
endif

cflags += -n $(name)

all: dependencies preclean main postclean

no_depends: preclean main postclean

dependencies:
	python src/dependencies.py

clean: preclean postclean 

preclean:
	-$(delete_dir) dist
	-$(delete_cmd) src/*.pyc; 
	-$(delete_dir) __pycache__

postclean:
	-$(delete_dir) build
	-$(delete_cmd) src/*.pyc
	-$(delete_dir) src/urllib3

deepclean:
	$(info This will make a lot of errors!  That's okay, just ignore them.)
	-$(delete_dir) dist
	-$(delete_dir) build
	-$(delete_dir) src/__pycache__
	-$(delete_cmd) src/*.pyc
	-$(delete_dir) src/urllib3      

main:
	$(compiler) $(cflags) $(target)

debug:
	$(compiler) $(cflags) --debug $(target)

print-%  : ; @echo $* = $($*)


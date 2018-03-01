.PHONY : main all os_check clean preclean postclean

compiler = pyinstaller
target = src/gui.py

ver_major = 1
ver_minor = 5
ver_patch = 1

hiddenimports = --hidden-import urllib3
hiddenimports += --hidden-import pyspeedtest

ifeq ($(OS),Windows_NT)
	name = PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch).exe
	delete_cmd = del
	delete_dir = rmdir /S /q
else
	ifeq ($(OS),Darwin)
		name = PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch)_mac
		delete_cmd = rm
		delete_dir = rmdir -r
	else
		name = PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch)_unix
		delete_cmd = rm
		delete_dir = rm -r
	endif
endif

cflags = -F -y -n $(name) --specpath build --clean $(hiddenimports)

ifeq ($(OS),Windows_NT)
	cflags += -w
else
	ifeq ($(OS),Darwin)
		cflags += -w
	else
		# linux users like their consoles
		cflags += -c
	endif
endif

all: os_check dependencies preclean main postclean

dependencies:
	python src/dependencies.py

clean: preclean postclean

os_check:
	$(info OS has been detected: $(OS)) 

preclean:
	-$(delete_cmd) src/*.pyc
	-$(delete_cmd) dist/$(name)
	-$(delete_dir) __pycache__

postclean:
	-$(delete_cmd) src/*.pyc
	-$(delete_dir) src/urllib3
	-$(delete_dir) build

deepclean: preclean postclean
	$(info This will make a lot of errors!  That's okay, just ignore them.)
	-$(delete_dir) dist
	-$(delete_dir) __pycache
	-$(delete_cmd) src/*.pyc
	-$(delete_dir) src/urllib3
	-$(delete_dir) build

main:
	$(compiler) $(cflags) $(target)

print-%  : ; @echo $* = $($*)


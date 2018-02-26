.PHONY : main all os_check preclean postclean

compiler = pyinstaller
target = src/gui.py

ver_major = 0
ver_minor = 5
ver_patch = 0

ifeq ($(OS),Windows_NT)
	name = PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch).exe
	delete_cmd = del
	delete_dir = rmdir /S /q
else
	ifeq ($(OS),Darwin)
		name += PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch)_mac
		delete_cmd = rm
		delete_dir = rmdir -r
	else
		name += PySpeedTest_v$(ver_major).$(ver_minor).$(ver_patch)_unix
		delete_cmd = rm
		delete_dir = rm -r
	endif
endif

cflags = -F -y -n $(name) --specpath build

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

all: os_check preclean main postclean

os_check:
	@echo $(OS)
	
preclean:
	-$(delete_cmd) *.pyc
	-$(delete_cmd) dist/$(name)
	-$(delete_dir) __pycache__
	
postclean:
	-$(delete_cmd) *.pyc
	-$(delete_dir) "src/urllib3"
	-$(delete_dir) build

main: 
	$(compiler) $(cflags) $(target)


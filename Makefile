ifeq ($(OS),Windows_NT)
	SHELL=C:/Windows/System32/cmd.exe
endif
RM = rm -rf
CP = cp -rf
# /path/to/OpenDSAX (absolute path)
XBLOCKS_HOME := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
XBLOCK_MODULE = $(XBLOCKS_HOME)/xblocks/xblock-module/module
XBLOCK_JSAV = $(XBLOCKS_HOME)/xblocks/xblock-jsav/jsav
XBLOCK_CONTENT = $(XBLOCKS_HOME)/xblocks/xblock-content/content
SITE_PKG_HOME = /edx/app/edxapp/venvs/edxapp/lib/python2.7/site-packages
CONFIG_SCRIPT = tools/configure.py
PIP = pip install -r requirements.txt
TARGET = build
CSSLINTFLAGS = --quiet --errors=empty-rules,import,errors --warnings=duplicate-background-images,compatible-vendor-prefixes,display-property-grouping,fallback-colors,duplicate-properties,shorthand,gradients,font-sizes,floats,overqualified-elements,import,regex-selectors,rules-count,unqualified-attributes,vendor-prefix,zero-units
MINIMIZE = java -jar tools/yuicompressor-2.4.7.jar --nomunge

.PHONY: all clean min testX

all: testX

clean:
	- $(RM) *~
	- $(RM) Books
	@# Remove minified JS and CSS files
	- $(RM) lib/*-min.*
	- $(RM) Doc/*~
	- $(RM) Scripts/*~
	- $(RM) config/*~

min: nomin

# testX: min
# 	python $(CONFIG_SCRIPT) config/testX.json

testX:
	python $(CONFIG_SCRIPT) --edx config/$@.json
	$(CP) $(XBLOCKS_HOME)/Books/$@/html $(XBLOCK_CONTENT)/public/

ds-testX: min testX install-xblocks

fs-testX: min testX fs-install-xblocks

allBooks: testX

nomin:
	@cp JSAV/build/JSAV.js JSAV/build/JSAV-min.js
	@cp lib/odsaUtils.js lib/odsaUtils-min.js
	@cp lib/odsaMOD.js lib/odsaMOD-min.js
	@cp lib/odsaAV.js lib/odsaAV-min.js
	@cp lib/gradebook.js lib/gradebook-min.js
	@cp ODSAkhan-exercises/khan-exercise.js lib/khan-exercise-min.js
	@cp lib/registerbook.js lib/registerbook-min.js
	@cp lib/site.css lib/site-min.css
	@cat lib/normalize.css lib/odsaAV.css > lib/odsaAV-min.css
	@cp lib/odsaMOD.css lib/odsaMOD-min.css
	@cp lib/odsaStyle.css lib/odsaStyle-min.css
	@cp lib/gradebook.css lib/gradebook-min.css

pull:
	git pull
	git submodule init
	git submodule update
	$(MAKE) -s -C JSAV
	$(MAKE) -s min
	cd Doc && $(MAKE)
	$(CP) $(XBLOCKS_HOME)/lib $(XBLOCK_MODULE)/public/
	$(CP) $(XBLOCKS_HOME)/JSAV $(XBLOCK_MODULE)/public/
	$(CP) $(XBLOCKS_HOME)/AV $(XBLOCK_JSAV)/public/
	$(CP) $(XBLOCKS_HOME)/lib $(XBLOCK_JSAV)/public/
	$(CP) $(XBLOCKS_HOME)/JSAV $(XBLOCK_JSAV)/public/

install-xblocks: install-utils install-module install-jsav install-content install-binsortmcq

install-utils:
	cd $(XBLOCKS_HOME)/xblocks/xblock-utils && $(PIP)

install-module:
	cd $(XBLOCKS_HOME)/xblocks/xblock-module && $(PIP)

install-jsav:
	cd $(XBLOCKS_HOME)/xblocks/xblock-jsav && $(PIP)

install-content:
	cd $(XBLOCKS_HOME)/xblocks/xblock-content && $(PIP)

install-binsortmcq:
	cd $(XBLOCKS_HOME)/xblocks/binsortmcq && $(PIP)

# Fullstack xblock installation targets
fs-install-xblocks: fs-install-utils fs-install-module fs-install-jsav fs-install-content restart-edxapp

fs-install-jsav:	
	$(RM) $(SITE_PKG_HOME)/jsav
	$(RM) $(SITE_PKG_HOME)/xblock_jsav-0.3-py2.7.egg-info
	sudo -H -u edxapp /edx/bin/pip.edxapp install $(XBLOCKS_HOME)/xblocks/xblock-jsav/

fs-install-module:	
	$(RM) $(SITE_PKG_HOME)/module
	$(RM) $(SITE_PKG_HOME)/module_xblock-0.1-py2.7.egg-info
	sudo -H -u edxapp /edx/bin/pip.edxapp install $(XBLOCKS_HOME)/xblocks/xblock-module/

fs-install-content:	
	$(RM) $(SITE_PKG_HOME)/content
	$(RM) $(SITE_PKG_HOME)/content_xblock-0.1-py2.7.egg-info
	sudo -H -u edxapp /edx/bin/pip.edxapp install $(XBLOCKS_HOME)/xblocks/xblock-content/

fs-install-utils:	
	$(RM) $(SITE_PKG_HOME)/xblockutils
	$(RM) $(SITE_PKG_HOME)/xblock_utils-0.1a0-py2.7.egg-info
	sudo -H -u edxapp /edx/bin/pip.edxapp install $(XBLOCKS_HOME)/xblocks/xblock-utils/
    
fs-install-course:
	cd /edx/app/edxapp/edx-platform
	sudo -u www-data /edx/bin/python.edxapp ./manage.py cms --settings=aws import /edx/var/edxapp/data  $(XBLOCKS_HOME)/Books/$@/$@.tar.gz

restart-edxapp:
	sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:
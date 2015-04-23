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
    
testX: min
	python $(CONFIG_SCRIPT) --edx config/$@.json
	$(CP) $(XBLOCKS_HOME)/Books/$@/html $(XBLOCK_CONTENT)/public/
	make install-xblocks

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
	make -s -C JSAV
	make -s min
	cd Doc && $(MAKE)
	$(CP) $(XBLOCKS_HOME)/lib $(XBLOCK_MODULE)/public/
	$(CP) $(XBLOCKS_HOME)/JSAV $(XBLOCK_MODULE)/public/
	$(CP) $(XBLOCKS_HOME)/AV $(XBLOCK_JSAV)/public/
	$(CP) $(XBLOCKS_HOME)/lib $(XBLOCK_JSAV)/public/
	$(CP) $(XBLOCKS_HOME)/JSAV $(XBLOCK_JSAV)/public/


# install-jsav install-module install-content
install-xblocks: install-utils install-module install-jsav install-content

install-utils:
	cd $(XBLOCKS_HOME)/xblocks/xblock-utils && $(PIP)

install-module:
	cd $(XBLOCKS_HOME)/xblocks/xblock-module && $(PIP)

install-jsav:
	cd $(XBLOCKS_HOME)/xblocks/xblock-jsav && $(PIP)

install-content:
	cd $(XBLOCKS_HOME)/xblocks/xblock-content && $(PIP)
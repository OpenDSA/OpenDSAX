RM = rm -rf
CONFIG_SCRIPT = tools/configure.py
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

testX: min
	python $(CONFIG_SCRIPT) config/testX.json

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
	git submodule update
	make -s -C JSAV
	make -s min
	cd Doc; make

pullx: pull
	make testX
	@cp -fr /home/OpenDSAX/AV /home/OpenDSAX/xblocks/xblock-module/module/public/
	@cp -fr /home/OpenDSAX/JSAV /home/OpenDSAX/xblocks/xblock-module/module/public/
	@cp -fr /home/OpenDSAX/lib /home/OpenDSAX/xblocks/xblock-module/module/public/
	@cp -fr /home/OpenDSAX/Books/testX/html/_static /home/OpenDSAX/xblocks/xblock-module/module/public/
	@cp -fr /home/OpenDSAX/AV /home/OpenDSAX/xblocks/xblock-jsav/jsav/public/
	@cp -fr /home/OpenDSAX/JSAV /home/OpenDSAX/xblocks/xblock-jsav/jsav/public/
	@cp -fr /home/OpenDSAX/lib /home/OpenDSAX/xblocks/xblock-jsav/jsav/public/
	@cp -fr /home/OpenDSAX/Books/testX/html/_static /home/OpenDSAX/xblocks/xblock-jsav/jsav/public/
	@cp -fr /home/OpenDSAX/Books/testX/html /home/OpenDSAX/xblocks/xblock-content/content/public/
	sudo -u edxapp /edx/bin/pip.edxapp install /home/OpenDSAX/xblocks/xblock-jsav/ --upgrade
	sudo -u edxapp /edx/bin/pip.edxapp install /home/OpenDSAX/xblocks/xblock-module/ --upgrade
	sudo -u edxapp /edx/bin/pip.edxapp install /home/OpenDSAX/xblocks/xblock-content/ --upgrade

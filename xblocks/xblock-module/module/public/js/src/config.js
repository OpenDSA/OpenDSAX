(function () {
	// "use strict";
	var settings = {};
	//@efouh: added this variable back because it is needed by gradebook.html
	settings.BOOK_NAME = "testX";
	settings.BOOK_LANG = "en";
	settings.EXERCISE_SERVER = "";
	settings.LOGGING_SERVER = "";
	settings.SCORE_SERVER = "";
	settings.MODULE_ORIGIN = "http://opendsax.local";
	settings.EXERCISE_ORIGIN = "http://opendsax.local";
	settings.AV_ORIGIN = "http://opendsax.local";
	// Flag controlling whether or not the system will assign credit (scores) obtained by anonymous users to the next user to log in
	settings.ALLOW_ANON_CREDIT = true;
	settings.REQ_FULL_SS = true;
	// settings.BUILD_TO_ODSA = "../../../";
	// CMS version
	settings.BUILD_TO_ODSA = "/xblock/resource/jsav/public/";
	// workbench version
	// settings.BOOK_URL = "/resource/module/public/";
	// TODO: to be replaced with a template variable
	settings.BOOK_URL = "/xblock/resource/module/public/";

	settings.DISP_MOD_COMP = "{{displayModule}}";
	settings.MODULE_NAME = "{{shortName}}";
	settings.MODULE_LONG_NAME = "{{longName}}";
	settings.MODULE_CHAPTER = "{{chapter}}";
	settings.BUILD_DATE = "2014-12-29 14:18:41";
	settings.BUILD_CMAP = true;

	var DOCUMENTATION_OPTIONS = {
		URL_ROOT: './',
		VERSION: '0.4.1',
		COLLAPSE_INDEX: false,
		FILE_SUFFIX: '.html',
		HAS_SOURCE: true
	};

	window.ODSA = {};
	window.ODSA.SETTINGS = settings;
	window.DOCUMENTATION_OPTIONS = DOCUMENTATION_OPTIONS;
}());
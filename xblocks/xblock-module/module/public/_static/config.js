"use strict";
(function () {
  var settings = {};
  //@efouh: added this variable back because it is needed by gradebook.html
  settings.BOOK_NAME = "testX";
  settings.BOOK_LANG = "en";
  settings.EXERCISE_SERVER = "https://opendsa.cc.vt.edu";
  settings.LOGGING_SERVER = "https://opendsa.cc.vt.edu";
  settings.SCORE_SERVER = "https://opendsa.cc.vt.edu";
  settings.MODULE_ORIGIN = "http://algoviz.org";
  settings.EXERCISE_ORIGIN = "http://algoviz.org";
  settings.AV_ORIGIN = "http://algoviz.org";
  // Flag controlling whether or not the system will assign credit (scores) obtained by anonymous users to the next user to log in
  settings.ALLOW_ANON_CREDIT = true;
  settings.REQ_FULL_SS = true;
  settings.BUILD_TO_ODSA = "../../../";

  window.ODSA = {};
  window.ODSA.SETTINGS = settings;
}());

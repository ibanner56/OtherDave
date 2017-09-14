"use strict";

// Based off of kylestetz Sentencer project: https://github.com/kylestetz/Sentencer/
// Words and patterns pulled from toykeeper.net MadLib generator:
//		http://toykeeper.net/programs/mad/index

var natural = require('natural');
var nounInflector = new natural.NounInflector();
var articles = require('articles/lib/Articles.js');
var randy = require('randy');
var _ = require('lodash');

///////////////////////////////////////////////////////////////////////////////
//								Building Blocks								//
/////////////////////////////////////////////////////////////////////////////

function Complimenter() {
	var self = this;

	self._amounts = require("../data/respect/amounts.json");
    self._adjectives = require("../data/respect/adjectives.json");
	self._persons = require("../data/respect/persons.json");
	self._parts = require("../data/respect/parts.json");
	self._things = require("../data/respect/things.json");
	self._templates = require("../data/respect/templates.json");

	self.actions = {
		amount: function() {
			return randy.choice(self._amounts);
		},
		an_amount: function() {
			return articles.articlize( self.actions.amount() );
		},
		adjective: function() {
			return randy.choice(self._adjectives);
		},
		an_adjective: function() {
 	    	return articles.articlize( self.actions.adjective() );
		},
		person: function() {
			return randy.choice(self._persons);
		},
		parts: function() {
			return randy.choice(self._parts);
		},
		thing: function() {
			return randy.choice(self._things);
		},
		template: function() {
			return randy.choice(self._templates);
		}
	};
}

Complimenter.prototype.make = function() {
  	var self = this;
  	var template = self.actions.template();
  
  	var sentence = template;
  	var occurrences = template.match(/\{\{(.+?)\}\}/g);

  	if(occurrences && occurrences.length) {
    	for(var i = 0; i < occurrences.length; i++) {
    		var action = occurrences[i].replace('{{', '').replace('}}', '').trim();
      		var result = '';
      		if(action.match(/\((.+?)\)/)) {
        		try {
          			result = eval('self.actions.' + action);
        		}
        		catch(e) { }
      		} else {
        		if(self.actions[action]) {
          			result = self.actions[action]();
        		} else {
          			result = '{{ ' + action + ' }}';
        		}
      		}

      		sentence = sentence.replace(occurrences[i], result);
    	}
  	}

  	return sentence;
};

var OtherDavesGraphicRespect = new Complimenter();

function respect(logger, user, args) {
	logger.info("Respect - user: " + user + ", args: " + args);

	var target = user;

	if (args.length > 0) {
		target = args[0];
	}

	var compliment = OtherDavesGraphicRespect.make()
	return target + ", " + compliment;
}

module.exports = respect; 

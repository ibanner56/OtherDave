'use strict';

var moment = require('moment');

function drunkdraw() {
    var draw = require('./drunkdraw.json');
    var base = 'The next drunkdraw is ';

    if(draw.date) {
	base += draw.date;
    } else {
        var today = moment();
	var drawdate = moment({year: today.year(), month: today.month()});
    	drawdate.date(drawdate.date() + 14 - drawdate.day() % 7);

	if(today.date() > drawdate.date()) {
	    drawdate.month(drawdate.month() + 1);
	    drawdate.date(drawdate.date() + 14 - drawdate.day() % 7);
	}

	base += drawdate.format('dddd[,] MMMM Do ');
    }

    base += 'at ';

    if(draw.time) {
        base += draw.time;
    } else {
        base += '4:00 pm PST. ';
    }

    if(draw.theme) {
        base += 'The theme is ' + draw.theme + '. ';
	if(draw.references) {
	    base += '\nJust this once, references ARE allowed.';
	} else {
	    base += '\nAs always, references are NOT allowed.';
	}
    } else {
        base += 'Theme is still tbd.';
    }

    return base;
}

module.exports = drunkdraw;

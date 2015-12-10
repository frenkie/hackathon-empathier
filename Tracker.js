var EventEmitter = require('events').EventEmitter;
var extend = require('extend');
var spawn = require( 'child_process' ).spawn;
var util = require('util');

var Tracker = function () {

    EventEmitter.call(this);

    this.tracking = false;
};

util.inherits(Tracker, EventEmitter);


extend( Tracker.prototype, {

    handleTrackerOutput: function ( output ) {
        if ( output ) {

            try {
                var jsonString = output.toString().split( 'INFO:root:' )[ 1 ];
                var json = JSON.parse( jsonString );
                this.emit( 'data', json );

            } catch ( e ) {
                console.log('error handling tracker output', e);
            }
        }
    },

    start: function () {
        this.tracking = true;

        this.track();
    },

    stop: function () {
        this.tracking = false;
    },

    track: function () {

        var spawnArguments = ['./PythonAPI.py'];

        this.Tracker = spawn( 'python', spawnArguments );
        this.Tracker.stderr.on('data', this.handleTrackerOutput.bind( this ));
    }
});


module.exports = Tracker;
var EventEmitter = require('events').EventEmitter;
var extend = require('extend');
var spawn = require( 'child_process' ).spawn;
var util = require('util');

var PythonTracker = function () {

    EventEmitter.call(this);

    this.tracking = false;
};

util.inherits(PythonTracker, EventEmitter);


extend( PythonTracker.prototype, {

    handleTrackerOutput: function ( output ) {
        if ( output ) {
            this.emit( 'data', output.toString() );
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

        this.pythonTracker = spawn( 'python', spawnArguments );
        this.pythonTracker.stderr.on('data', this.handleTrackerOutput.bind( this ));
    }
});


module.exports = PythonTracker;
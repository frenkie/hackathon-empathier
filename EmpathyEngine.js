/**
 * Server-side empathy communication engine
 * @param {Socket.io} socket
 * @constructor
 */

var EmpathyEngine = function ( socket ) {

    this.reset();

    this.socket = socket;

    this.bindSocketEvents();
};

EmpathyEngine.prototype = {

    bindSocketEvents: function () {

        this.socket.on('connection', function ( client ) {

            console.log('connected!');

            client.on('reset', this.handleReset.bind( this ) );
            client.on('tag-update', this.handleTagUpdate.bind( this ) );

        }.bind( this ) );

    },

    handleReset: function () {
        this.reset();
        this.socket.emit('reset-story');
    },

    handleTagUpdate: function ( tags ) {

        this.socket.emit('tag-update', tags );
    },

    reset: function () {
        console.log('reset story');
        this.state = {};
    }
};

module.exports = EmpathyEngine;
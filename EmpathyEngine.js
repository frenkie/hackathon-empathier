var osc = require('osc');

/**
 * Server-side empathy communication engine
 * @param {Socket.io} socket
 * @constructor
 */

var EmpathyEngine = function ( socket ) {

    this.reset();

    this.socket = socket;
    this.oscPort = new osc.UDPPort({
        localAddress: '0.0.0.0', // URL to your server.
        localPort: 57121
    });
    this.oscPort.open();

    this.clients = ['10.0.1.125', '10.0.1.108', '10.0.1.96'];

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

        console.log( tags );
        this.sendSpeech( tags );
    },

    sendMessageToClients: function ( message ) {
        for ( var i = 0, il = this.clients.length; i < il; i++ ) {

            this.oscPort.send( message, this.clients[ i ], 8000 );
        }
    },

    sendSpeech: function ( tags ) {

        this.socket.emit( 'tag-update', tags );

        tags.forEach(function ( tag ) {

            this.sendMessageToClients({
                address: '/woorden', args: tag
            });

        }.bind(this));
    },

    reset: function () {
        console.log('reset story');
    }
};

module.exports = EmpathyEngine;
var Tracker = require('./Tracker' );
var osc = require('osc');

/**
 * Server-side empathy communication engine
 * @param {Socket.io} socket
 * @constructor
 */

var EmpathyEngine = function ( socket ) {

    this.reset();

    this.socket = socket;
    this.tracker = new Tracker();
    this.oscPort = new osc.UDPPort({
        localAddress: '0.0.0.0', // URL to your server.
        localPort: 57121
    });
    this.oscPort.open();

    this.clients = ['10.0.1.125', '10.0.1.108', '10.0.1.96'];

    this.bindSocketEvents();
    this.bindTrackerEvents();

    this.tracker.start();
};

EmpathyEngine.prototype = {

    bindSocketEvents: function () {

        this.socket.on('connection', function ( client ) {

            console.log('connected!');

            client.on('reset', this.handleReset.bind( this ) );
            client.on('tag-update', this.handleTagUpdate.bind( this ) );

        }.bind( this ) );

    },

    bindTrackerEvents: function () {
        this.tracker.on('data', this.handleTrackerData.bind( this ));
    },

    handleReset: function () {
        this.reset();
        this.socket.emit('reset-story');
    },

    handleTagUpdate: function ( tags ) {

        console.log( tags );
        this.sendSpeech( tags );
    },

    handleTrackerData: function ( data ) {

        if ( data ) {

            this.sendVisual( data );
        }
    },

    sendMessageToClients: function ( message ) {
        for ( var i = 0, il = this.clients.length; i < il; i++ ) {

            this.oscPort.send( message, this.clients[ i ], 8000 );
        }
    },

    sendVisual: function ( result ) {

        if ( result && result.Classification ) {

            result.Classification.ClassificationValues.ClassificationValue.forEach(function ( value ) {

                switch ( value.Label ) {

                    default:
                        if ( value.Value ) {
                            this.sendMessageToClients({
                                address: '/live/'+ value.Label.toLowerCase(),
                                args: parseFloat( value.Value.float )
                            });
                        }
                        break;
                }
            }.bind( this ));

        }
    },

    sendSpeech: function ( tags ) {

        this.socket.emit( 'tag-update', tags );

        this.sendMessageToClients({
            address: "/woorden", args: tags
        });
    },

    reset: function () {
        console.log('reset story');
        this.state = {};
    }
};

module.exports = EmpathyEngine;
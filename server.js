var express = require('express'); // Docs http://expressjs.com/
var socketIo = require('socket.io'); // Docs http://socket.io/

var config = require('./config.json');
var EmpathyEngine = require('./EmpathyEngine');

var app = express();
var server = require('http').Server( app );
var io = socketIo( server );

var port = config.server.port;

var adminRouter = require('./routes/admin');
var speechRouter = require('./routes/speech');
var vendorRouter = require('./routes/vendor');

app.use( vendorRouter );
app.use( adminRouter );
app.use( speechRouter );

    // binding to 0.0.0.0 allows connections from any other computer in the network
    // to your ip address
server.listen( port, '0.0.0.0', function () {

    console.log('empathy server started on localhost:'+ port );

    new EmpathyEngine( io );
} );

var PythonTracker = require('./PythonTracker' );
var pythonTracker = new PythonTracker();

pythonTracker.on('data', function ( data ) {
    console.log( 'jeejj', data );
});

pythonTracker.start();

// TESTING

//var net = require('net');
//var client = new net.Socket();
//
//client.connect( config.facetracker.port, config.facetracker.host, function() {
//	console.log('Connected to facetracker');
//});
//
//client.on('data', function(data) {
//	console.log('Received: ' + data);
//});
//
//client.on('close', function() {
//	console.log('Connection closed');
//});
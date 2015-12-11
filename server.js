var express = require('express'); // Docs http://expressjs.com/
var socketIo = require('socket.io'); // Docs http://socket.io/

var EmpathyEngine = require('./EmpathyEngine');

var app = express();
var server = require('http').Server( app );
var io = socketIo( server );

var port = process.env.PORT || 8080;

var speechRouter = require('./routes/speech');
var vendorRouter = require('./routes/vendor');

app.use( vendorRouter );
app.use( speechRouter );


    // binding to 0.0.0.0 allows connections from any other computer in the network
    // to your ip address
server.listen( port, '0.0.0.0', function () {

    console.log('empathy server started on localhost:'+ port );

    new EmpathyEngine( io );
} );
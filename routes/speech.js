var express = require('express');
var router = express.Router();

router.use('/speech-analyser', express.static( __dirname +'/../speech-analyser' ));

module.exports = router;
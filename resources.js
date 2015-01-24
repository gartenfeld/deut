var express = require('express');
var mongo = require('mongodb');
var path = require('path');
var app = express();

app.set('view engine', 'jade');
app.set('port', process.env.OPENSHIFT_NODEJS_PORT || 8080); 
app.set('ipaddr', process.env.OPENSHIFT_NODEJS_IP || "127.0.0.1");
app.use(express.static(path.join(__dirname, 'public')));

var server_port = process.env.OPENSHIFT_NODEJS_PORT || 8080,
    server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';
 
//var dbUser = process.env.SUOMI_USERNAME,
//    dbPass = process.env.SUOMI_PASSWORD;

var dbHost = "localhost",
    dbPort = 27017;

var uri = 'mongodb://' + dbHost + ':' + dbPort + '/deutsch';

function getHeadword (searchString, callback) {

    mongo.MongoClient.connect(
        uri, 
        function(err, db) {
            if(err) throw err;

            query = { "$text": { "$search": searchString.toString() } };

            var cursor = db.collection("quotes").find(
                query,  
                { 'score': { '$meta': 'textScore' } },
                { '$sort': { '$meta': 'textScore' } }
                ).limit(3);

            cursor.toArray(
                function(error, docs){
                    if (docs.length === 0) { 
                        callback(false); 
                    } else { 
                        callback(docs); 
                    } } );
        });
}

app.get('/:wort', function (req, res) {
    res.render('show', { wort: req.params.wort });
});

app.get('/json/:query', function (req, res) {
    getHeadword(req.params.query, function(docs){
        if (!docs) {
            res.status(200).json([]);
        } else {
            res.status(200).json(docs);
        }
    });
}); 

app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});

module.exports = app;

var server = app.listen(server_port, server_ip_address, function () {
  console.log( "Listening on " + server_ip_address + ", Port " + server_port );
});
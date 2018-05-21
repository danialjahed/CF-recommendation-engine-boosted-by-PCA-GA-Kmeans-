var fs = require('fs');
var mongoose = require('mongoose');
var async = require('async');
// mongo connect to
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/' + "movie_db");
var database = mongoose.connection;
database.on('error', function(err) {
    console.log('Error : Mongo connection error'.red);
});
database.once('open', function() {
    console.log("connected to mongodb");
});
var db = require('mongo_schemas');
fs.readFile('../../Server/labels_string.txt', 'utf8', function(err, data) {
    if (err) {
        console.log(err);
    } else {
        data = data.split('\n');
        data.slice(1, -1);
        for (let i = 0; i < data.length; i++) {
            db.rates.update({
                user_id: (i + 1).toString()
            }, {
                $set: {
                    'cluster_number': data[i]
                }
            }, function(err) {
                if (err)
                    console.log(err);
            });
        }
        console.log("loop is done");
    }
});

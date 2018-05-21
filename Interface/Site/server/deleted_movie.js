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
fs.readFile('deleted_movie.txt', 'utf8', function(err, data) {
    if (err) {
        return console.log(err);
    }
    data = data.split('\n');
    async.each(data, function(index, cb) {
        db.rates.update({}, {
            $pull: {
                movie_rate: {
                    movie_id: index
                }
            }
        }, {
            multi: true
        }).maxTime(1000000000).exec(function(err) {
            if (err) {
                return console.log(err);
            }
            console.log("Done");
            cb();
        })
    });


});

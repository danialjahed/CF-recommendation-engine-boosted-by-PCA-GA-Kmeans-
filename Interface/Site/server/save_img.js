var fs = require('fs');
var mongoose = require('mongoose');
var async = require('async');
var request = require('request');
var uuid = require('uuid');
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
db.movie_info.find({}).lean().exec(function(err, data) {
    if (err) {
        return console.log("Mongo Error");
    }
    data.forEach(function(index) {
        if (typeof index["Poster"] != 'undefined' && index["Poster"] != "N/A") {
            let random = uuid.v4();
            request
                .get(index["Poster"])
                .on('error', function(err) {
                    if (err) {
                        console.log("Request Error");

                    } else {}
                })

            .pipe(fs.createWriteStream('../client/public/posters/' + random + '.jpg'))
            let local_address = '../client/public/posters/' + random;
            db.movie_info.update({
                _id: index._id
            }, {
                $set: {
                    'poster_address': local_address
                }
            }, function(err) {
                if (err) {
                    console.log("Mongo Error");
                }
            });

        }
    });
});

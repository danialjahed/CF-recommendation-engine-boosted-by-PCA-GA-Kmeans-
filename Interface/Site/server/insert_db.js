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
let number_of_rates = 6040;
let template = [];
let hash_index = {};
let delete_movie = [];
fs.readFile('deleted_movie.txt', 'utf8', function(err, data) {
    deleted_movie = data.split('\n');
});
fs.readFile('movies.dat', 'utf8', function(err, allData) {
    //    console.log(deleted_movie);
    let each_movie = allData.split('\n');
    let counter = 0;
    each_movie.forEach(function(index) {
        let movie_array = index.split('::');
        let movie_name = movie_array[1];
        let movie_id = movie_array[0];
        let each_movie_schema = {};
        if (index != '') {
            if (deleted_movie.indexOf(movie_id) == -1) {
                each_movie_schema.movie_id = movie_id;
                each_movie_schema.rate = null;
                hash_index[movie_id] = counter;
                counter++;
                template.push(each_movie_schema);
            }
        }
    });
    let template_data = {};
    template_data.user_id = "0";
    template_data.movie_rate = template;
    db.rates.create(template_data, function(err, info) {
        if (err) {
            console.log(err);
        }
    });
});
fs.readFile('ratings.dat', 'utf8', function(err, data) {
    let user_rating = data.split('\n');
    let each_data = {};
    let final_data = [];
    async.each(user_rating, function(index, cb) {
        let movie_info = index.split(',');
        if (deleted_movie.indexOf(movie_info[1]) != -1) {
            return (cb());
        }
        if (each_data.user_id == movie_info[0]) {
            each_data.user_id = movie_info[0];
            let movie_index = hash_index[movie_info[1]];
            each_data.movie_rate[movie_index].rate = Number(movie_info[2]);
        } else {
            if (typeof each_data.user_id != 'undefined') {
                //                console.log(each_data);
                final_data.push(each_data);
            }
            if (index != '') {
                let movie_index = hash_index[movie_info[1]];
                each_data = {};
                each_data.movie_rate = JSON.parse(JSON.stringify(template));
                each_data.user_id = movie_info[0];
                each_data.movie_rate[movie_index].rate = Number(movie_info[2]);

            }
        }
    });
    final_data.forEach(function(index) {
        db.rates.create(index, function(err) {
            if (err) {
                console.log(err);
            }
            if (index.user_id == "6040")
                database.close();
        });
    });
});

var db = require('mongo_schemas');
var async = require('async');
var recom = require('recommended_movie');
module.exports.post = function(req, res) {
    let data = req.body;
    //TODO:check input validation
    async.waterfall([
            //remove rate form array
            function(cb) {
                // db.rates.update({
                //     user_id: req.user.session.toString(),
                //     "movie_rate.movie_id": data.movie_id
                // }, {
                //    $set: {
                //      "movie_rate.$.rate": data.rate
                //    }
                // }, function(err, info) {
                //     if (err) {
                //         console.mongo('Error', err);
                //         return (cb(err, null));
                //     }
                //     cb(null, true);
                // });
                db.rates.findOne({
                    user_id: req.user.session.toString()
                }).lean().exec(function(err, info) {
                    if (err) {
                        console.mongo('Error', err);
                        return (cb(err, null));
                    }
                    let index = -1;
                    for (let i = 0; i < info.movie_rate.length; i++) {
                        if (info.movie_rate[i].movie_id == data.movie_id) {
                            index = i;
                            break;
                        }
                    }
                    cb(null, index);
                });

            },
            function(index, cb) {
                db.rates.update({
                    user_id: req.user.session.toString()
                }, {
                    $pull: {
                        movie_rate: {
                            movie_id: data.movie_id
                        }
                    }
                }, function(err) {
                    if (err) {
                        console.mongo('Error', err);
                        return (cb(err, null));
                    }
                    cb(null, index);
                });
            },
            function(index, cb) {
                db.rates.update({
                    user_id: req.user.session.toString()
                }, {
                    $push: {
                        movie_rate: {
                            $each: [{
                                'rate': data.rate,
                                'movie_id': data.movie_id
                            }],
                            $position: index
                        }

                    }
                }, function(err) {
                    if (err) {
                        console.mongo('Error', err);
                        return (cb(err, null));
                    }
                    cb(null, true)
                })
            },
            //delete recommende movie to show new movie in the recom list
            function(res, cb) {
                db.rates.update({
                    user_id: req.user.session.toString()
                }, {
                    $pull: {
                        recom_movie: data.movie_id
                    }
                }, function(err) {
                    if (err) {
                        console.mongo('Error', err);
                        return (cb(err, null));
                    }
                    cb(null, true);
                });
            },
            //get new movie for recommendation
            function(res, cb) {
                recom.get_recommended(req.user.session.toString(), function(err, data) {
                    if (err) {
                        console.mongo('Error', err);
                        return (cb(err, null));
                    }
                    cb(null, data);
                });
            }
        ],
        function(err, result) {
            if (err) {
                return res.sendStatus(500);
            }
            return res.json(result);
        }
    );
};

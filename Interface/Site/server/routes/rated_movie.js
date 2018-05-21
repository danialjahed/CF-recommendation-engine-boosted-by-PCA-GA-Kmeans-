var db = require('mongo_schemas');
var async = require('async');
module.exports.get = function(req, res) {
    let result = [];
    db.rates.aggregate([{
        "$match": {
            "user_id": req.user.session.toString()
        }
    }, {
        "$unwind": "$movie_rate"
    }, {
        "$match": {
            "movie_rate.rate": {
                $ne: null
            }
        }
    }]).exec(function(err, indexes) {
        if (indexes == null) indexes = {};
        async.each(indexes, function(index, cb) {
            db.movie_info.findOne({
                movie_id: index.movie_rate.movie_id
            }).lean().exec(function(err, info) {
                if (err) {
                    console.mongo('Error', err);
                    cb(err, null);
                }
                if (info != null) {
                    info.user_rate = index.movie_rate.rate;
                    result.push(info);
                }
                cb();
            });
        }, function(err) {
            if (err) {
                return res.sendStatus(500);
            }
            let res_data = {};
            res_data.status = true;
            res_data.rated_movie = result;
            res.json(res_data);

        })
    });
}

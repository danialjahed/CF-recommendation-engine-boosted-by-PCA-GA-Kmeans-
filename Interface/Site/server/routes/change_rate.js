var db = require('mongo_schemas');
module.exports.post = function(req, res) {
    let data = req.body;
    //TODO :value validation
    //delete rate
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
            return res.sendStatus(500);
        }
        //add new rate
        db.rates.update({
            user_id: req.user.session.toString()
        }, {
            $push: {
                movie_rate: {
                    'rate': data.rate,
                    'movie_id': data.movie_id
                }
            }
        }, function(err) {
            if (err) {
                console.mongo('Error', err);
                return res.sendStatus(500);
            }
            res.json({
                status: true
            })
        })
    });
}

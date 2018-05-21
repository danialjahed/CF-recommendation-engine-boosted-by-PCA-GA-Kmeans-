var db = require('mongo_schemas');
var spawn = require("child_process").spawn;
var recommended = require('recommended_movie');
module.exports.get = function(req, res) {
    var _process = spawn('python3', ["Backend/CF.py", req.user.session]);
    _process.stdout.on('data', function(data) {
        recommended.get_recommended(req.user.session.toString(), function(err, data) {
            if (err) {
                if (err.status == false) {
                    return res.json(err);
                }
                console.mongo('Error', err);
                return res.sendStatus(500);
            } else {
                return res.json({
                    'status': true,
                    'recom_movie': data.recom_movie
                });
            }
        });
    });
}

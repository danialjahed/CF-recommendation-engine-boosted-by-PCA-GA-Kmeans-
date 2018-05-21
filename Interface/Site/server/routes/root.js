/**
 * Created by danial on 7/27/16.
 */
//PLANNING: change the Site UI
var error = require("djs");
var db = require('mongo_schemas');
module.exports = function(app) {
    app.all('/*', function(req, res, next) {
        req.user = {};
        if (typeof req.session._id == 'undefined') {
            req.user.session = null;
            if (req.url != "/login" && req.url != '/enroll')
                return res.redirect('/login');
            next();
        } else {
            db.users.findOne({
                _id: req.session._id
            }).lean().exec(function(err, data) {
                if (err) {
                    return error.error_handel(res, err, 500, 'internal server error');
                }
                if (data == null) {
                    req.user.session = null;
                    if (req.url != "/login" && req.url != '/enroll')
                        return res.redirect('/login');
                    return next();
                }
                req.user.name = data.first_name + " " + data.last_name;
                req.user.session = data._id;
                next();
            });
        }
    });
    require('./dynamic_routes')(app);
    app.use(function(req, res, next) {
        var err = new Error('Not Found');
        err.status = 404;
        next(err);
    });
    app.use(function(err, req, res, next) {
        res.locals.message = err.message;
        res.locals.error = req.app.get('env') === 'development' ? err : {};
        console.log(err);
        res.status(err.status || 500);
        res.render('error');
    });
};

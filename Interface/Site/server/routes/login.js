/**
 * Created by danial on 8/26/16.
 */
var db = require("mongo_schemas");
var ascync = require("async");
var bcrypt = require("bcrypt");
var form = require('form_validation');
var async = require('async');
var recommended = require('recommended_movie')
module.exports.post = function(req, res) {
    var data = req.body;
    ascync.waterfall([
        function check_input(cb) {
            let isFormValid = (form.isValid(data.username) &&
                form.isValid(data.password));
            let error = {
                'status': false,
                'message': 'مقادیر وارد شده نامعبتر است.'
            }
            if (isFormValid) {
                return (cb(null, true));
            }
            return (cb(err, null));

        },
        function check_password(res_data, callback) {
            db.users.findOne({
                username: data.username
            }, {}).lean().exec(function(err, user_data) {
                if (err) {
                    console.mongo('Error', err);
                    return (callback(err, null));
                }
                if (user_data == null) {
                    console.mongo('Info', 'Unsuccessful login wrong Username : ' + data.username + ' password: ' + data.password);
                    return (callback({
                        'status': false,
                        'message': 'نام‌کاربری‌ یا رمز‌عبور اشتباه است.'
                    }, null));
                }
                bcrypt.compare(data.password, user_data.password, function(err, hash_res) {
                    if (err) {
                        console.mongo('Error', err);
                        return (callback(err, null));
                    }
                    let res_data = {};
                    if (hash_res) {
                        console.mongo('Info', 'Successfull login Username : ' + user_data.username);
                        req.session._id = user_data._id;
                        res_data.status = true;
                        return (callback(null, res_data));
                    }
                    console.mongo('Info', 'Unsuccessful login wrong password Username : ' + user_data.username);
                    res_data.status = false;
                    res_data.message = 'نام‌کاربری‌ یا رمز‌عبور اشتباه است.';
                    return (callback(res_data, null));
                });
            });
        }
    ], function(err, result) {
        if (err) {
            if (err.status == false) {
                return res.json(err);
            }
            console.mongo('Error', err);
            return res.sendStatus(500);
        }
        result.title = 'خوش آمدید';
        result.message = 'با موفقیت وارد شدید.';
        res.json(result);
    });
}

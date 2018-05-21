/**
 * Created by danial on 9/9/16.
 */
var db = require("mongo_schemas");
var async = require("async");
var bcrypt = require("bcrypt");
var error = require('djs');
var form = require('form_validation');
var mongoose = require('mongoose');

function CleanArray(arr) {
    let clean_arr = [];
    arr.forEach(function(index) {
        clean_arr.push(index._id);
    });
    return clean_arr;
}
module.exports.post = function(req, res) {
    let data = req.body;
    let isFormValid = (form.isValid(data.username) &&
        form.isValid(data.first_name) &&
        form.isValid(data.last_name) &&
        form.isValid(data.email) &&
        form.isValid(data.password));
    if (!isFormValid) {
        let res_data = {
            'status': false,
            'message': 'تمامی فیلد های فرم باید کامل شود'
        }
        return res.json(res_data);
    }
    async.waterfall([
        check_username,
        check_email,
        generate_hashPassword,
        save_result,
        query_top_rated,
        save_rated_query

    ], function(err, result) {
        if (err) {
            if (!err.externalError)
                return error.error_handel(res, err, 500, 'internal server error');
            return res.json(err);
        }
        result.title = '';
        result.message = 'با موفقیت ثبت‌نام شدید.';
        res.json(result);
    });

    function check_username(callback) {
        db.users.count({
            username: data.username
        }).lean().exec(function(err, username) {
            if (err) {
                console.mongo(err);
                err.externalError = false;
                return (callback(err, null));
            }
            let res_data = {};
            if (username) {
                res_data.status = false;
                res_data.externalError = true;
                res_data.message = 'نام کاربری قبلا در سیستم ثبت شده است';
                return (callback(res_data, null));
            }
            res_data.status = true;
            return (callback(null, res_data));
        });
    }

    function check_email(res_data, callback) {
        db.users.count({
            email: data.email
        }).lean().exec(function(err, email) {
            if (err) {
                console.mongo(err);
                err.externalError = false;
                return (callback(err, null));
            }
            let res_data = {};
            if (email) {
                res_data.status = false;
                res_data.externalError = true;
                res_data.message = 'ایمیل قبلا در سیستم ثبت شده است';
                return (callback(res_data, null));
            }
            res_data.status = true;
            return (callback(null, res_data));
        });
    }

    function generate_hashPassword(res_data, callback) {
        bcrypt.hash(data.password, 10, function(err, hash) {
            if (err) {
                console.mongo('Error', err);
                err.externalError = false;
                return (callback(err, null));
            }
            let res_data = {
                'status': true,
                'password': hash
            }
            callback(null, res_data);
        });
    }

    function save_result(res_data, cb) {
        data.password = res_data.password;
        let temp = new db.users(data);
        temp.save(function(err) {
            if (err) {
                console.mongo('Error', err);
                err.externalError = false;
                return (cb(err, null));
            }
            return (cb(null, res_data));

        });
    }

    function query_top_rated(res_data, cb) {
        db.top_rated_movie.find().sort({
            "weight_rate": -1
        }).limit(30).lean().exec(function(err, topRated) {
            if (err) {
                console.mongo('Error', err);
                err.externalError = false;
                return (cb(err, null));
            }
            if (topRated != null) {
                res_data.topRated = CleanArray(topRated);
                return (cb(null, res_data));
            }
            console.mongo("Error", "unhandeled error in enroll.js line 116");
            res_data = {
                'status': false,
                'externalError': false
            }
            return (cb(res_data, null));
        });
    }

    function save_rated_query(res_data, cb) {
        db.users.findOne({
            username: data.username
        }, {
            _id: true
        }).lean().exec(function(err, userId) {
            if (err) {
                console.mongo('Error', err);
                err.externalError = false;
                return (cb(err, null));
            }
            db.rates.findOne({
                user_id: "0"
            }).lean().exec(function(err, info) {
                if (err) {
                    console.mongo('Error', err);
                    err.externalError = false;
                    return (cb(err, null));
                }
                let rated_data = {
                    'user_id': userId._id.toString(),
                    'movie_rate': info.movie_rate,
                    'recom_movie': res_data.topRated
                }
                let temp = new db.rates(rated_data);
                temp.save(function(err) {
                    if (err) {
                        console.mongo('Error', err);
                        err.externalError = false;
                        return (cb(err, null));
                    }
                    res_data = {
                        'status': true
                    }
                    return (cb(null, res_data));
                });
            });
        });
    }
}

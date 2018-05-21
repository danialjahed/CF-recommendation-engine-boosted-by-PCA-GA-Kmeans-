/**
 * Created by danial on 7/28/16.
 */
//TODO: add Logs post route and user edit profile
var _route = require("djs");
var get_routes = [
    '/init',
    '/logout',
    '/rated_movie',
    '/core'
];
var post_route = [
    '/login',
    '/enroll',
    '/rate',
    '/change_rate'
];
module.exports = function(app) {
    app.get('/', function(req, res) {
        res.render('index');
    });
    app.get('/login', function(req, res) {
        res.render('login');
    });
    get_routes.forEach(function(index) {
        _route.file_get(app, index);
    });
    post_route.forEach(function(index) {
        _route.file_post(app, index);
    });
};

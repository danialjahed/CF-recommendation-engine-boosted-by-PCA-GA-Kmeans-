var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require('cookie-session')
var app = express();
global.init = {};
global.init.db_name = "movie_db";
app.set('views', path.join(__dirname, 'client/views'));
app.set('view engine', 'ejs');
app.use(favicon(path.join(__dirname, 'client/public/images', 'favicon.png')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: false
}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'client/public')));
app.use(session({
    name: 'dv_seesion',
    secret: 'kytddkhovoqy'
}));

require('./server/utils/modules');
require('./server/routes/root')(app);
module.exports = app;

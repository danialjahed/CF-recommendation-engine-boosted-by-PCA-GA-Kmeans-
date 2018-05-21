/**
 * Created by danial on 8/26/16.
 */
//TODO:console mongo should change now it get two pramater for logs type and error
var db = require("mongo_schemas");
console.error = function(text) {
    var date = new Date();
    console.log("Date : " + date.getDate() + "/" + date.getMonth() + "/" + date.getFullYear() +
        " " + date.getHours() + " : " + date.getMinutes() + " : " + date.getSeconds() + " ----> Error : " + text);
};
console.mongo = function(type, text) {
    var date = new Date();
    var logs = {};
    text = "Date : " + date.getDate() + "/" + date.getMonth() + "/" + date.getFullYear() +
        " " + date.getHours() + " : " + date.getMinutes() + " : " + date.getSeconds() + " ---> " + text;
    logs.log = text;
    logs.type = type;
    db.logs(logs).save(function(err, doc) {
        if (err) {
            console.error(err);
        } else {
            console.log(text);
        }
    });
};
console.info = function(text) {
    var date = new Date();
    console.log(date.getHours() + " : " + date.getMinutes() + " : " + date.getSeconds() + " ----> " + text);
};

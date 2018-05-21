var PythonShell = require('python-shell');
var spawn = require("child_process").spawn;
var _process = spawn('python3', ["../Backend/CF.py", '58892c80859037114aee387b']);
_process.stdout.on('data', function(data) {
    console.log(data.toString());
});
_process.stderr.on('err', function(err) {
    console.log(err.toString());
});

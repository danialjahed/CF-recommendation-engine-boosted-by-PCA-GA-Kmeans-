module.exports.get = function(req, res) {
    req.session = null;
    res.json({
        status: true
    })
};

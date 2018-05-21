angular.module('user_rated_movie', ['http_engine']).service('user_rated', function(http) {
    this.get = function(cb) {
        http.get('/rated_movie', {}, function(err, data) {
            if (err) {
                toastr.error('اشکال داخلی سرور', 'خطا');
                return (cb(null));
            }
            var owl = $("#owl2");
            owl.owlCarousel({
                itemsDesktop: [640, 4],
                itemsDesktopSmall: [414, 3]
            });
            owl.data('owlCarousel').destroy();
            return (cb(data.rated_movie));
        });
    }
});

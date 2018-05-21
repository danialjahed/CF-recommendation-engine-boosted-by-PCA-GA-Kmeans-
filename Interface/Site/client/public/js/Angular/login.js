var login = angular.module('app', ['ngAnimate', 'http_engine']);
login.controller('login_controller', function($scope, http) {
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-bottom-left",
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "2000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
    $scope.login_mode = true;
    $scope.submit_title = "ورود";
    $scope.toggle_value = 'ثبت‌نام';
    $scope.form_trigger = function() {
        $scope.login_mode = !$scope.login_mode;
        var temp = $scope.submit_title;
        $scope.submit_title = $scope.toggle_value;
        $scope.toggle_value = temp;
    }
    $scope.send_form = function() {
        var form_data = ($scope.login_mode) ? $scope.login : $scope.enroll;
        var url = ($scope.login_mode) ? '/login' : '/enroll';
        http.post(url, form_data, function(err, data) {
            $scope.login = {};
            $scope.enroll = {};
            if (err) {
                return toastr.error('اشکال داخلی سرور', 'خطا');
            }
            if (data.status == true) {
                toastr.success(data.message, data.title);
                if (url == '/login') {
                    setTimeout(function() {
                        location.replace('/')
                    }, 1000);
                } else {
                    $scope.form_trigger();
                }

            } else {
                toastr.error(data.message, 'خطا');
            }

        });
    };
});

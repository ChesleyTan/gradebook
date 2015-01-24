$('form').on('submit', function() {
    if ($('#password').val() != $('#confirm_password').val()) {
        alert("The two passwords do not match! Please try again.");
        return false;
    }
    return true;
});

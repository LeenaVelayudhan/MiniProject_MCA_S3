$(document).ready(function() {
    $('#continent').on('change', function() {
        var continent = $(this).val();
        $.ajax({
            type: 'GET',
            url: '{% url "destination_page" %}',
            data: {
                continent: continent
            },
            success: function(data) {
                $('.destination-grid').html(data);
            }
        });
    });
});
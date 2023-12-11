$(document).ready(function() {
    $('#form').on('submit', function(e){
        $('#output').text('loading...');
        $.ajax({
        data : {
            holiday : $('#holiday').val(),
            receiver_name : $('#receiver_name').val(),
            receiver_location : $('#receiver_location').val(),
            select_relation : $('#select_relation').val(),           
            select_type : $('#select_type').val(),
            keywords : $('#keywords').val(),
        },
        type : 'POST',
        cache: false,
        url : '/'
        })
        .done(async function(data){
            d = await data
            $('#output').html(d.replace(/\n/g, '<br>'));
        })
        .fail(function(e){
            $('#output').text('failed!');
        });
        e.preventDefault();
    });
});

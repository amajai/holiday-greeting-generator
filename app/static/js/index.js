$(document).ready(function() {
    $('#loader').hide()
    $('#form').on('submit', function(e){
        $('#output').text('');
        $('#loader').show()
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
            $('#loader').hide()
            $('#output').html(d.replace(/\n/g, '<br>'));
        })
        .fail(function(e){ 
            $('#loader').hide()
            $('#output').text('failed!');
        });
        e.preventDefault();
    });
});

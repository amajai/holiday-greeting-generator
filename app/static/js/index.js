$(document).ready(function() {
    $('#output').hide()
    $('#loader').hide()
    $('#form').on('submit', function(e){
        $('#output').hide()
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
            $('#output').show()
            $('#output').html(d.replace(/\n/g, '<br>'));
        })
        .fail(function(e){ 
            $('#loader').hide()
            $('#output').show()
            $('#output').text('failed!');
        });
        e.preventDefault();
    });
});
function copyText () {
  const text = document.getElementById('output').innerText;
  const btnText = document.getElementById('copybtn');
  navigator.clipboard.writeText(text);
  btnText.innerText = 'Copied Text!';
  setTimeout(function () {
    btnText.innerText = 'Copy Text';
  }, 1500);
}
$(document).ready(function () {
  $('#loader').hide();
  $('#form').on('submit', function (e) {
    $(':input[type="submit"]').prop('disabled', true);
    $('#output').text('');
    $('#loader').show();
    $.ajax({
      data: {
        holiday: $('#holiday').val(),
        receiver_name: $('#receiver_name').val(),
        sentiments: $('#sentiments').val(),
        receiver_location: $('#receiver_location').val(),
        select_relation: $('#select_relation').val(),
        select_type: $('#select_type').val(),
        keywords: $('#keywords').val()
      },
      type: 'POST',
      cache: false,
      url: '/'
    })
      .done(async function (data) {
        const d = await data;
        $(':input[type="submit"]').prop('disabled', false);
        $('#loader').hide();
        $('#output').html(d.replace(/\n/g, '<br>'));
      })
      .fail(function (e) {
        $(':input[type="submit"]').prop('disabled', false);
        $('#loader').hide();
        $('#output').text('No text was generated. Please try submitting again.');
      });
    e.preventDefault();
  });
});

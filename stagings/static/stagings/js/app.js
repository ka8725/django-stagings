$(document).ready(function() {
  $('.action-link').on('click', function() {
    var $form = $(this).closest('.form-actions').prev('form'),
        url = this.href;

    $form.attr('action', url);
    $form.submit();
  });

  $('.more-description').on('click', function(e) {
    e.stopPropagation();
    e.preventDefault();

    var $link = $(this);
    var $desc = $link.prev('p');

    if ($link.data('trunc-desc')) {
      $desc.text($link.data('trunc-desc'));
      $link.data('trunc-desc', null);
    } else {
      $(this).data('trunc-desc', $desc.text());
      $.getJSON(
        $link.attr('href'),
        function(data) {
          $desc.text(data['description']);
        }
      );
    }
  });
});

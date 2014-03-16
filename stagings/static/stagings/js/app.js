$(document).ready(function() {
  $('.action-link').on('click', function() {
    var form = $(this).closest('.form-actions').prev('form'),
        url = this.href;

    form.attr('action', url);
    form.submit();
  });
});

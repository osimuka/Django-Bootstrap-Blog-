$(document).on('submit', '#comment-box', function(e){
    // prevent page refresh
	e.preventDefault();
	var newComment = $('#comment-box').serialize();
	$.ajax({
	  type: 'POST',
	  url: '',
	  data: newComment,
	  success:function (data) {
	            var notSuccessful = $(data).filter('#errors').text() !== '' ? true: false;
	            if (notSuccessful) {
	                var error_message = $(data).filter('#errors').text().replace('comment', "");
	                var error_message_html = '<div class="alert alert-danger fade in"><strong>'+ error_message + '</strong></div>';
	                $('#error').empty().append(error_message_html);
	            } else {
	                console.log($(data).filter('#comment-count').html());
                    $('.form-control').val('');
                    $('#error').empty();
                    var new_comment = $(data).filter('#new-comment').html();
                    new_comment = '<div class=row>' + new_comment + '</div>';
                    $('#comment-section').append(new_comment);
                    $('#comment-count').html($(data).filter('#comment-count').html());
                }
            },
       error: function (data) {
                console.log(data);
       }
	})
})
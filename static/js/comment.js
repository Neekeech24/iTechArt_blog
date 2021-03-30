'use_strict';

let form = document.querySelector('form[name=comment-form');

form.addEventListener('submit', function (e) {
    e.preventDefault();
    const d = new Date();
    date = d.getDate(),
        month = d.getMonth() + 1,
        year = d.getFullYear(),
        hours = d.getHours(),
        mins = d.getMinutes();
    const pub_date = `${date}.${month}.${year} ${hours}:${mins}`;
    const csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8000/create_comment',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            body: $('textarea[name=body]').val(),
            article: $('input[name=article]').val()
        },
        success: function (responseData) {
            if (typeof responseData == 'object') {
                const commentsContainer = $('.comments-block');
                commentsContainer.prepend(`
                    <div class="comment">
                        <div class="comment-body">
                            ${responseData.body}
                        </div>
                       <div class="comment-info">
                            <ul>
                                  <li>
                                      <a href="/accounts/profile/${responseData.auth_user}">${responseData.username}</a>
                                  </li>
                            <li>${pub_date}</li>
                            </ul>
                         </div>
                     </div>
                `);
            } else {
                alert('Ошибка при заполнении комментария');
            }
        }
    })
});

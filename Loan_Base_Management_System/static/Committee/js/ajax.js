$(function () {
    $('#search').keyup(function () {
        counting =0;
        $.ajax({
            url:'search/',
            type: "POST",
            data: {
                'search_text': $('#search').val(),
                // 'csrfmiddlewaretoken' : $("input [name = csrfmiddlewaretoken]").val()
                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
                // 'csrfmiddlewaretoken' : '{{ csrf_token }}'
            },
            success: searchSuccess,
            dataType: 'html',
        });
    });
});

function searchSuccess(data,textStatus,jqXHR) {
    $('#search-results').html(data)
    
}
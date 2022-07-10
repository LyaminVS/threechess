function get_list() {
    $(".point").remove()
    $.ajax({
        type: "POST",
        url: "get_list/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}"
        },
    });
}
setInterval(get_list, 10000);

$(document).on("click", "#btn_new_game", function(){
    $.ajax({
        type: "POST",
        url: "new_game/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}",

        },
    });
})
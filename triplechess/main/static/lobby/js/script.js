function lobbyCsrfToken() {
    const m = document.querySelector('meta[name="csrf-token"]');
    return m ? m.getAttribute("content") : "";
}

$(document).on("click", "#btn_new_game", function(){
    $.ajax({
        type: "GET",
        url: "new_game/",
        headers: {
            "X-CSRFToken": lobbyCsrfToken(),
        },
        success: function(data) {
            if (data["success"]) {
                document.location = "/board/" + data["room_id"]
            }else{
                document.location = "/login/"
            }
        }
    });
})

$(document).on("click", "#btn_new_sandbox", function(){
    $.ajax({
        type: "GET",
        url: "new_sandbox_game/",
        headers: {
            "X-CSRFToken": lobbyCsrfToken(),
        },
        success: function(data) {
            if (data["success"]) {
                document.location = "/board/" + data["room_id"]
            }
        }
    });
})

$(document).on("click", ".btn_join_game", function(){
    id = this.id.split("_")[3]
    document.location = "/board/" + id + "/"
})

$(document).on("click", ".btn_join_spectator", function(){
    id = this.id.split("_")[3]
    document.location = "/board/" + id + "?is_spectator=1"
})
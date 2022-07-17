$(document).on("click", "#btn_new_game", function(){
    $.ajax({
        type: "POST",
        url: "new_game/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}",

        },
    });
})

$(document).on("click", ".btn_join_game", function(){
    id = this.id.split("_")[3]
    document.location = "room/" + id + "/"
    // $.ajax({
    //     type: "GET",
    //     url: "join_game/",
    //     headers: {
    //         "X-CSRFTOKEN": "{{ csrf_token }}",
            
    //     },
    //     data:{
    //         "id": id,
    //     },
    //     success: function(response){
    //         if (response.success == false){
    //             alert("не заработало")
    //         }
    //     }
    // });
})

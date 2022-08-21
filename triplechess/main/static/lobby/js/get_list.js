let filter_status = "in_lobby"

function get_list(filter_status) {
    $(".point").remove()
    $.ajax({
        type: "POST",
        url: "get_list/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}"
        },
        data:{
            "filter_status": filter_status,
        },
        success: function (response) {
            wrapper = $(".list_games_wrapper")
            
            wrapper.empty()

            let games = JSON.parse(response.games)

            games.forEach(game => {
                wrapper.append('<div class="one_game_wrapper" id="game_' + game.id + '"></div>')
                wrapper_2 = $("#game_" + game.id)
                if (!game.player_1){
                    game.player_1 = ""
                }
                if (!game.player_2){
                    game.player_2 = ""
                }
                if (!game.player_3){
                    game.player_3 = ""
                }
                wrapper_2.append('<div class="player_in_wrapper">Игрок 1: ' + game.player_1 + '</div>')
                wrapper_2.append('<div class="player_in_wrapper">Игрок 2: ' + game.player_2 + '</div>')
                wrapper_2.append('<div class="player_in_wrapper">Игрок 3: ' + game.player_3 + '</div>')
                wrapper_2.append('<button class="btn btn-info btn_join_game" id="btn_join_game_' + game.id + '">Инфо</button>')
                wrapper_2.append('<button class="btn btn-warning btn_join_spectator" id="btn_join_spectator_' + game.id + '">Предупреждение</button>')
            });
        }
    });
}
get_list(filter_status)
let interval = setInterval(get_list, 5000, filter_status);

$(document).on("click", "#btn_in_lobby_games", function(){
    $("#btn_started_games").attr("disabled", false)
    $("#btn_in_lobby_games").attr("disabled", true)
    filter_status = "in_lobby"
    get_list(filter_status)
    clearInterval(interval)
    interval = setInterval(get_list, 5000, filter_status);
})

$(document).on("click", "#btn_started_games", function(){
    $("#btn_started_games").attr("disabled", true)
    $("#btn_in_lobby_games").attr("disabled", false)
    filter_status = "started"
    get_list(filter_status)
    clearInterval(interval)
    interval = setInterval(get_list, 5000, filter_status);
})
function get_list() {
    $(".point").remove()
    $.ajax({
        type: "POST",
        url: "get_list/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}"
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
            });
        }

    });
}
get_list()
setInterval(get_list, 5000);
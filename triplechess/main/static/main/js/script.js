url = document.location.href


roomCode = url.slice(url.length - 2, url.length - 1)
console.log(roomCode)
var connectionString = 'ws://' + window.location.host + '/ws/board/' + roomCode + '/';
var gameSocket = new WebSocket(connectionString);
connect();

let player_color = ''
let player_turn = 'white'

RED_TURN = {
    "A": "H",
    "B": "G",
    "C": "F",
    "D": "E",
    "E": "K",
    "F": "L",
    "G": "M",
    "H": "N",
    "K": "D",
    "L": "C",
    "M": "B",
    "N": "A",

    "1": "8",
    "2": "7",
    "3": "6",
    "4": "5",
    "5": "9",
    "6": "10",
    "7": "11",
    "8": "12",
    "9": "4",
    "10": "3",
    "11": "2",
    "12": "1"
}

BLACK_TURN = {
    "H": "A",
    "G": "B",
    "F": "C",
    "E": "D",
    "K": "E",
    "L": "F",
    "M": "G",
    "N": "H",
    "D": "K",
    "C": "L",
    "B": "M",
    "A": "N",

    "8": "1",
    "7": "2",
    "6": "3",
    "5": "4",
    "9": "5",
    "10": "6",
    "11": "7",
    "12": "8",
    "4": "9",
    "3": "10",
    "2": "11",
    "1": "12"
}

function connect() {
    gameSocket.onopen = function open() {
        gameSocket.send(JSON.stringify({
            "type": "START",
        }));
    };

    gameSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };

    gameSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        data = data["payload"];
        let type = data["type"];
        switch (type) {
            case "START":
                player_turn = data["turn"]
                break;
            case "END":
                break;
            case "MOVE":
                get_board($(".board"))
                break;
            case "GET_BOARD":
                $(".cell_item").addClass("old_cell")
                player_turn = data["turn"]
                let figures = data["figures"]
                figures.forEach(figure => {
                    path = img_from_type(figure[0], figure[1])
                    let letter = figure[2].slice(0, 1)
                    let number = figure[2].slice(1)
                    if (player_color == "black"){
                        letter = BLACK_TURN[letter]
                        number = BLACK_TURN[number]
                    }
                    if (player_color == "red"){
                        letter = RED_TURN[letter]
                        number = RED_TURN[number]
                    }
                    
                    if ($("#" + letter + number).attr("src") != path){
                        set_cell_picture($(".board"), path, letter, number, figure[1])
                    }else{
                        $("#" + letter + number).removeClass("old_cell")
                    }
                    
                });
                $(".old_cell").remove()
                break;
            case "GET_DOTS":
                $(".point").remove()
                dots = data["dots"]
                paint_dots(dots)
                break;
            case "CHANGE_POSITION":
                get_board($(".board"))
                break;
            case "RESET":
                clear_board()
                get_board($(".board"))
                break;
            case "CHANGE_COLOR":
                get_board($(".board"))
                // $("#btn_" + data["color"]).remove()
                break;
            default:
                break;

        }
    };

    if (gameSocket.readyState == WebSocket.OPEN) {
        gameSocket.onopen();
    }
}


function set_cell_picture(board, path, letter, number, color = false, add_class = false, id = true){
    let img_class = " cell_item cell_item"
    
    if (color){
        img_class = color + " cell_item cell_item "
    }
    if (add_class){
        img_class = add_class + img_class
    }
    new_id = ''
    if (id){
        new_id = "id='" + letter + number + "'"
    }
    img_class = img_class.trim()
    board.after("<img src = '" + path + "'" + new_id + "class='" + img_class + letter + number + "'>");
}
function remove_cell_picture(letter, number) {
    $("#" + letter + number).remove()
}

function img_from_type(type, color){
    if (type == "King"){
        img = "king"
    }
    if (type == "Peshka"){
        img = "peshka"
    }
    if (type == "Queen"){
        img = "queen"
    }
    if (type == "Tara"){
        img = "tara"
    }
    if (type == "Officer"){
        img = "officer"
    }
    if (type == "Horse"){
        img = "horse"
    }
    return "/static/main/img/" + img + "_" + color + ".png"
}

function get_board(board){
    gameSocket.send(JSON.stringify({
        "type": "GET_BOARD",
    }));
}

function clear_board(){
    $(".cell_item").remove()
}

window.onload = function() {
    
    let grey_circle = '/static/main/img/peshka_white.png';
    let letters_1 = ['A', 'B', 'C', 'D'];
    let letters_2 = ['E', 'F', 'G', 'H'];
    let letters_3 = ['K', 'L', 'M', 'N'];
    let numbers_1 = ['1', '2', '3', '4']
    let numbers_2 = ['5', '6', '7', '8']
    let numbers_3 = ['9', '10', '11', '12']
    let board = $(".board");
    gameSocket.onopen = function(board){
        reset()
    }    
 };



$(document).on("click", ".cell_item", function() {
    if (!($(this).attr("class").split(" ").includes("point"))){
        let id = $(this).attr('id')
        let letter = id.slice(0, 1)
        let number = id.slice(1)
        
        
        get_dots(letter, number)
    }
});

function reset(){
    gameSocket.send(JSON.stringify({
        "type": "RESET",
    }));
}

function paint_dots(dots){
    let red_circle = '/static/main/img/red_circle.png'
    let grey_circle = '/static/main/img/grey_circle.png';
    let green_circle = '/static/main/img/green_circle.png'
    dots[0].forEach(dot => {
        let letter = dot.slice(0, 1)
        let number = dot.slice(1)
        if (player_color == "black"){
            letter = BLACK_TURN[letter]
            number = BLACK_TURN[number]
        }
        if (player_color == "red"){
            letter = RED_TURN[letter]
            number = RED_TURN[number]
        }
        let board = $(".board");
        set_cell_picture(board, grey_circle, letter, number, false,  "point")
    });
    dots[1].forEach(dot => {
        let letter = dot.slice(0, 1)
        let number = dot.slice(1)
        if (player_color == "black"){
            letter = BLACK_TURN[letter]
            number = BLACK_TURN[number]
        }
        if (player_color == "red"){
            letter = RED_TURN[letter]
            number = RED_TURN[number]
        }
        let board = $(".board");
        set_cell_picture(board, red_circle, letter, number, false, "eat_point point", false)
    });
}

function get_dots(letter, number){
    if ($("#" + letter + number).hasClass(player_color)){
        if (player_color == "black"){
            letter = RED_TURN[letter]
            number = RED_TURN[number]
        }
        if (player_color == "red"){
            letter = BLACK_TURN[letter]
            number = BLACK_TURN[number]
        }
        
        gameSocket.send(JSON.stringify({
            "type": "GET_DOTS",
            'letter': letter,
            'number': number,
        }));
    }
 }

$(document).on("click", ".point", function() {
    if (player_turn == player_color){
        
        if (!$(this).attr("class").split(" ").includes("eat_point")){
            cell = $(this).attr("id")
            var letter = cell.slice(0, 1)
            var number = cell.slice(1)
            if (player_color == "black"){
                letter = RED_TURN[letter]
                number = RED_TURN[number]
            }
            if (player_color == "red"){
                letter = BLACK_TURN[letter]
                number = BLACK_TURN[number]
            }
            cell = letter + number
            $(".point").remove()
            gameSocket.send(JSON.stringify({
                "type": "MOVE",
                "cell": cell
            }));
        }
    }
});

$(document).on("click", ".eat_point", function(){
    if (player_turn == player_color){
        let cell_classes = $(this).attr("class")
        cell_classes = cell_classes.split(" ")
        let cell = cell_classes[cell_classes.length - 1].split("cell_item")[1]
        var letter = cell.slice(0, 1)
        var number = cell.slice(1)
            if (player_color == "black"){
                letter = RED_TURN[letter]
                number = RED_TURN[number]
            }
            if (player_color == "red"){
                letter = BLACK_TURN[letter]
                number = BLACK_TURN[number]
            }
            cell = letter + number
        $(".point").remove()
        gameSocket.send(JSON.stringify({
            "type": "CHANGE_POSITION",
            "cell": cell
        }));
    }
})

$(document).on("click", ".board", function(){
    $(".point").remove()
    gameSocket.send(JSON.stringify({
        "type": "RESET_DOTS",
    }));
})

$(document).on("click", "#btn_reset", function(){
    reset()
})

$(document).on("click", "#btn_white", function(){
    player_color = "white"
    change_color(player_color)
})

$(document).on("click", "#btn_black", function(){
    player_color = "black"
    change_color(player_color)
})

$(document).on("click", "#btn_red", function(){
    player_color = "red"
    change_color(player_color)
})

function change_color(color){
    gameSocket.send(JSON.stringify({
        "type": "CHANGE_COLOR",
        "color": color
    }));
}



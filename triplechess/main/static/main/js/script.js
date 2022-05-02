roomCode = 1

var connectionString = 'ws://' + window.location.host + '/ws/board/' + roomCode + '/';
var gameSocket = new WebSocket(connectionString);
connect();

function connect() {
    gameSocket.onopen = function open() {
        gameSocket.send(JSON.stringify({
            "event": "START",
            "message": ""
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
                break;
            case "END":
                break;
            case "MOVE":
                let old_letter = data["old_cell"].slice(0, 1)
                let old_number = data["old_cell"].slice(1)
                let letter = data["cell"].slice(0, 1)
                let number = data["cell"].slice(1)
                
                path = img_from_type(data["figure"], data["color"])
                set_cell_picture($(".board"), path, letter, number)
                remove_cell_picture(old_letter, old_number)
                break;
            case "GET_BOARD":
                let figures = data["figures"]
                figures.forEach(figure => {
                    path = img_from_type(figure[0], figure[1])
                    let letter = figure[2].slice(0, 1)
                    let number = figure[2].slice(1)
                    set_cell_picture($(".board"), path, letter, number)
                });
                break;
            case "GET_DOTS":
                $(".point").remove()
                dots = data["dots"]
                paint_dots(dots)
                break;
            default:
                break;

        }
    };

    if (gameSocket.readyState == WebSocket.OPEN) {
        gameSocket.onopen();
    }
}


function set_cell_picture(board, path, letter, number, add_class = false, id = true){
    let img_class = " cell_item cell_item"
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
    // $.ajax({
    //     type: "POST",
    //     url: "get_board/",
    //     headers: {
    //         "X-CSRFTOKEN": "{{ csrf_token }}"
    //     },
    //     success: function(data){
    //         figures = data.figures
    //         figures.forEach(figure => {
    //             path = img_from_type(figure[0], figure[1])
    //             let letter = figure[2].slice(0, 1)
    //             let number = figure[2].slice(1)
    //             set_cell_picture(board, path, letter, number)
    //         });
    //     }
    // });
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
        get_board(board) 
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
    // $.ajax({
    //     type: "POST",
    //     url: "reset/",
    //     headers: {
    //         "X-CSRFTOKEN": "{{ csrf_token }}"
    //     },
    // });
}

function paint_dots(dots){
    let red_circle = '/static/main/img/red_circle.png'
    let grey_circle = '/static/main/img/grey_circle.png';
    let green_circle = '/static/main/img/green_circle.png'
    dots[0].forEach(dot => {
        let letter = dot.slice(0, 1)
        let number = dot.slice(1)
        let board = $(".board");
        set_cell_picture(board, grey_circle, letter, number, "point")
    });
    dots[1].forEach(dot => {
        let letter = dot.slice(0, 1)
        let number = dot.slice(1)
        let board = $(".board");
        set_cell_picture(board, red_circle, letter, number, "eat_point point", false)
    });
}

function get_dots(letter, number){
    gameSocket.send(JSON.stringify({
        "type": "GET_DOTS",
        'letter': letter,
        'number': number,
    }));
    // $.ajax({
    //     type: "POST",
    //     url: "get_dots/",
    //     headers: {
    //         "X-CSRFTOKEN": "{{ csrf_token }}"
    //     },
    //     data: {
    //         'letter': letter,
    //         'number': number,
    //     },
    //     success: function(data){
    //         $(".point").remove()
    //         dots = data.dots
    //         paint_dots(dots)
    //     }
    // });
 }

$(document).on("click", ".point", function() {
    if (!$(this).attr("class").split(" ").includes("eat_point")){
        cell = $(this).attr("id")
        $(".point").remove()
        gameSocket.send(JSON.stringify({
            "type": "MOVE",
            "cell": cell
        }));
        // $.ajax({
        //     type: "POST",
        //     url: "change_position/",
        //     headers: {
        //         "X-CSRFTOKEN": "{{ csrf_token }}"
        //     },
        //     data: {
        //         "cell": cell,
        //     },
        //     success: function(data){
        //         let old_letter = data["old_cell"].slice(0, 1)
        //         let old_number = data["old_cell"].slice(1)
        //         let letter = data["cell"].slice(0, 1)
        //         let number = data["cell"].slice(1)
        //         remove_cell_picture(old_letter, old_number)
        //         path = img_from_type(data["figure"], data["color"])
        //         set_cell_picture($(".board"), path, letter, number)
        //     }
        // });
    }
});

$(document).on("click", ".eat_point", function(){
    let cell_classes = $(this).attr("class")
    cell_classes = cell_classes.split(" ")
    let cell = cell_classes[cell_classes.length - 1].split("cell_item")[1]
    let letter = cell.slice(0, 1)
    let number = cell.slice(1)
    remove_cell_picture(letter, number)
    $(".point").remove()
    $.ajax({
        type: "POST",
        url: "change_position/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}"
        },
        data: {
            "cell": cell,
        },
        success: function(data){
            let old_letter = data["old_cell"].slice(0, 1)
            let old_number = data["old_cell"].slice(1)
            let letter = data["cell"].slice(0, 1)
            let number = data["cell"].slice(1)
            remove_cell_picture(old_letter, old_number)
            path = img_from_type(data["type"], data["color"])
            set_cell_picture($(".board"), path, letter, number)
        }
    });
})

$(document).on("click", ".board", function(){
    $(".point").remove()
    gameSocket.send(JSON.stringify({
        "type": "RESET_DOTS",
    }));
    // $.ajax({
    //     type: "POST",
    //     url: "reset_dots/",
    //     headers: {
    //         "X-CSRFTOKEN": "{{ csrf_token }}"
    //     },
    // });

})


//call the connect function at the start.


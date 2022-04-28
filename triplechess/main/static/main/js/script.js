function set_cell_picture(board, path, letter, number, add_class = false){
    let img_class = "cell_item cell_item"
    if (add_class){
        img_class = add_class + img_class
    }
    board.after("<img src = '" + path + "' id='" + letter + number + "' class='" + img_class + letter + number + "'>");
}
function remove_cell_picture(cell) {
    cell.remove()
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
    $.ajax({
        type: "POST",
        url: "get_board/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}"
        },
        success: function(data){
            figures = data.figures
            figures.forEach(figure => {
                path = img_from_type(figure[0], figure[1])
                let letter = figure[2].slice(0, 1)
                let number = figure[2].slice(1)
                set_cell_picture(board, path, letter, number)
            });
        }
    });
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
    get_board(board)
 };



$(document).on("click", ".cell_item", function() {
    let id = $(this).attr('id')
    let letter = id.slice(0, 1)
    let number = id.slice(1)
    get_dots(letter, number)
});



function get_dots(letter, number){
    $.ajax({
        type: "POST",
        url: "get_dots/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}"
        },
        data: {
            'letter': letter,
            'number': number,
        },
        success: function(data){
            let grey_circle = '/static/main/img/grey_circle.png';
            dots = data.dots
            dots[0].forEach(dot => {
                let letter = dot.slice(0, 1)
                let number = dot.slice(1)
                let board = $(".board");
                set_cell_picture(board, grey_circle, letter, number, "point")
            });
            
        }
    });
 }
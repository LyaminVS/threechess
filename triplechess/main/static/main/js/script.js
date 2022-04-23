function set_cell_picture(board, path, letter, number){
    board.after("<img src = '" + path + "' id='" + letter + number + "' class='cell_item cell_item" + letter + number + "'>");
}
function remove_cell_picture(cell) {
    cell.remove()
}

window.onload = function() {
    let grey_circle = '/static/main/img/peshka_1.png';
    let letters_1 = ['A', 'B', 'C', 'D'];
    let letters_2 = ['E', 'F', 'G', 'H'];
    let letters_3 = ['K', 'L', 'M', 'N'];
    let numbers_1 = ['1', '2', '3', '4']
    let numbers_2 = ['5', '6', '7', '8']
    let numbers_3 = ['9', '10', '11', '12']
    let board = $(".board");
    for (let i = 0; i < 4; i++) {
        let letter = letters_1[i]
        for (let i = 0; i < 4; i++) {
            let number = numbers_1[i]
            set_cell_picture(board, grey_circle, letter, number)
        }
        for (let i = 0; i < 4; i++) {
            let number = numbers_3[i]
            set_cell_picture(board, grey_circle, letter, number)
        }
    }
    for (let i = 0; i < 4; i++) {
        let letter = letters_2[i]
        for (let i = 0; i < 4; i++) {
            let number = numbers_1[i]
            set_cell_picture(board, grey_circle, letter, number)
        }
        for (let i = 0; i < 4; i++) {
            let number = numbers_2[i]
            set_cell_picture(board, grey_circle, letter, number)
        }
    }
    for (let i = 0; i < 4; i++) {
        let letter = letters_3[i]
        for (let i = 0; i < 4; i++) {
            let number = numbers_2[i]
            set_cell_picture(board, grey_circle, letter, number)
        }
        for (let i = 0; i < 4; i++) {
            let number = numbers_3[i]
            set_cell_picture(board, grey_circle, letter, number)
        }
    }
    test_ajax()

 };



$(document).on("click", ".cell_item", function() {
    let id = $(this).attr('id')
    let letter = id.slice(0, 1)
    let number = id.slice(1)
    send_turn(letter, number)
});
//    remove_cell_picture($(".cell_itemA1"));});
//
//remove_cell_picture($(".cell_itemA1"))



function send_turn(letter, number){
    $.ajax({
        type: "POST",
        url: "test/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}"
        },
        data: {
            'letter': letter,
            'number': number,
        },
        success: function(data){
            console.log(data.code)
        }
    });
 }
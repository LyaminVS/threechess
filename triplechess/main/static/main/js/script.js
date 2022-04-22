function set_cell_picture(board, path, cell){
    board.after("<img src = '" + path + "' class='cell_item cell_item" + cell + "'>");
}

window.onload = function() {
    let grey_circle = '/static/main/img/grey_circle.png';
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
            let cell = letter + number
            set_cell_picture(board, grey_circle, cell)
        }
        for (let i = 0; i < 4; i++) {
            let number = numbers_3[i]
            let cell = letter + number
            set_cell_picture(board, grey_circle, cell)
        }
    }
    for (let i = 0; i < 4; i++) {
        let letter = letters_2[i]
        for (let i = 0; i < 4; i++) {
            let number = numbers_1[i]
            let cell = letter + number
            set_cell_picture(board, grey_circle, cell)
        }
        for (let i = 0; i < 4; i++) {
            let number = numbers_2[i]
            let cell = letter + number
            set_cell_picture(board, grey_circle, cell)
        }
    }
    for (let i = 0; i < 4; i++) {
        let letter = letters_3[i]
        for (let i = 0; i < 4; i++) {
            let number = numbers_2[i]
            let cell = letter + number
            set_cell_picture(board, grey_circle, cell)
        }
        for (let i = 0; i < 4; i++) {
            let number = numbers_3[i]
            let cell = letter + number
            set_cell_picture(board, grey_circle, cell)
        }
    }

    
 };
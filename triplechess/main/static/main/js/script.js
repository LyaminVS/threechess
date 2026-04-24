var roomCode = ""
if (typeof window.__BOARD_INIT__ !== "undefined" && window.__BOARD_INIT__.roomCode) {
    roomCode = String(window.__BOARD_INIT__.roomCode)
}
if (!roomCode) {
    var _m = window.location.pathname.match(/\/board\/([^/]+)\/?/)
    roomCode = _m ? _m[1] : ""
}
window.roomCode = roomCode

function boardApi(path) {
    var p = String(path).replace(/^\//, "")
    return "/board/" + encodeURIComponent(roomCode) + "/" + p
}

var wsScheme = window.location.protocol === "https:" ? "wss" : "ws"
var connectionString = wsScheme + "://" + window.location.host + "/ws/board/" + encodeURIComponent(roomCode) + "/"
var gameSocket = new WebSocket(connectionString);

function readCsrfToken() {
    var m = document.querySelector('meta[name="csrf-token"]')
    return m ? m.getAttribute("content") : ""
}

function colorRu(c) {
    var map = { white: "белые", black: "чёрные", red: "красные" }
    return map[c] || c
}

function turnBadgeClasses(turn) {
    var base = "badge rounded-pill game-turn-badge w-100 py-2 d-inline-block"
    var tone = " bg-secondary"
    if (turn === "white") tone = " bg-success bg-opacity-25 text-dark border border-success"
    else if (turn === "black") tone = " bg-dark"
    else if (turn === "red") tone = " bg-danger"
    return base + tone
}

var player_color = "white"
var sandboxMode = !!(typeof window.__BOARD_INIT__ !== "undefined" && window.__BOARD_INIT__.sandbox)
var sandboxOrderedTurn = !!(typeof window.__BOARD_INIT__ !== "undefined" && window.__BOARD_INIT__.sandboxOrderedTurn)
var activeMoveColor = null
if ($("#sandbox-banner").length && !$("#sandbox-banner").hasClass("d-none")) {
    sandboxMode = true
}
if (typeof window.__BOARD_INIT__ !== "undefined") {
    if (window.__BOARD_INIT__.roomCode) $("#room-code-display").text(window.__BOARD_INIT__.roomCode)
    if (window.__BOARD_INIT__.colorLabel) $("#player-color-display").text(window.__BOARD_INIT__.colorLabel)
    if (window.__BOARD_INIT__.modeLabel) $("#spectator-display").text(window.__BOARD_INIT__.modeLabel)
}

function setPerspective(color) {
    if (color !== "white" && color !== "black" && color !== "red") return
    player_color = color
    $(".perspective-btn").removeClass("active")
    $(".perspective-btn[data-color='" + color + "']").addClass("active")
    get_board($(".board"))
}

function updateSandboxTurnModeUI() {
    $(".turn-mode-btn").removeClass("active")
    var key = sandboxOrderedTurn ? "ordered" : "free"
    $(".turn-mode-btn[data-mode='" + key + "']").addClass("active")
}
updateSandboxTurnModeUI()

function pieceColorFromElement($el) {
    if (!$el || !$el.length) return null
    var d = $el.attr("data-piece-color")
    if (d === "white" || d === "black" || d === "red") return d
    if ($el.hasClass("white")) return "white"
    if ($el.hasClass("black")) return "black"
    if ($el.hasClass("red")) return "red"
    var src = String($el.attr("src") || "")
    if (src.indexOf("_white.") !== -1) return "white"
    if (src.indexOf("_black.") !== -1) return "black"
    if (src.indexOf("_red.") !== -1) return "red"
    return null
}

function appendLegacySprite(board, path, letter, number, color, add_class, id) {
    var classes = []
    if (color) classes.push(color)
    classes.push("cell_item")
    classes.push("cell_item" + letter + number)
    if (add_class) {
        String(add_class).split(/\s+/).forEach(function (c) {
            if (c) classes.push(c)
        })
    }
    var classStr = classes.join(" ")
    var idAttr = id ? " id='" + letter + number + "'" : ""
    var dataAttr = color ? " data-piece-color='" + color + "'" : ""
    board.after("<img src='" + path + "'" + idAttr + dataAttr + " class='" + classStr + "' />")
}

connect();
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
    gameSocket.onopen = function() {
        gameSocket.send(JSON.stringify({
            "type": "START",
            "room_id": roomCode,
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
                if (data["success"]){
                    get_board($(".board"))
                }else{
                    alert("Логотип хакеры еееееееее")
                }
                break;
            case "GET_BOARD":
                $(".cell_item").addClass("old_cell")
                player_turn = data["turn"]
                update_turn(player_turn)
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
                        $("#" + letter + number).attr("data-piece-color", figure[1])
                        $("#" + letter + number).removeClass("white black red").addClass(figure[1])
                        $("#" + letter + number).removeClass("old_cell")
                    }
                    
                });
                $(".old_cell").remove()
                let selected_figure = data["selected_figure"]
                if (selected_figure){
                    let letter = selected_figure.slice(0, 1)
                    let number = selected_figure.slice(1)
                    if (player_color == "black"){
                        letter = BLACK_TURN[letter]
                        number = BLACK_TURN[number]
                    }
                    if (player_color == "red"){
                        letter = RED_TURN[letter]
                        number = RED_TURN[number]
                    }
                    get_dots(letter, number, true)
                }
                break;
            case "GET_DOTS":
                $(".point").remove()
                dots = data["dots"]
                paint_dots(dots)
                break;
            case "CHANGE_POSITION":
                if (data["success"]){
                    get_board($(".board"))
                }else{
                    alert("Логотип хакеры еееееееее")
                }
                break;
            case "RESET":
                clear_board()
                get_board($(".board"))
                break;
            case "CHANGE_COLOR":
                get_board($(".board"))
                break;
            case "TOGGLE_READY":
                if (data["success"]){
                    update_ready(data["ready_status"])
                }
                break;
            case "START_GAME":
                $("#ready-row").addClass("d-none")
                break;
            case "SANDBOX_TURN_MODE":
                if (typeof data["ordered"] !== "undefined") {
                    sandboxOrderedTurn = !!data["ordered"]
                    updateSandboxTurnModeUI()
                    update_turn(player_turn)
                }
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
    appendLegacySprite(board, path, letter, number, color, add_class, id)
}
function remove_cell_picture(letter, number) {
    $("#" + letter + number).remove()
}

function img_from_type(type, color){
    const pieceMap = {
        "King": "k",
        "Queen": "q",
        "Tara": "r",
        "Officer": "b",
        "Horse": "n",
        "Peshka": "p",
    }
    const colorMap = {
        "white": "lt",
        "black": "dt",
        "grey": "gt",
        "red": "rt",
    }
    const piece = pieceMap[type]
    const c = colorMap[color]
    if (piece && c) {
        return "/static/main/img/Chess_" + piece + c + "45.svg"
    }
    return "/static/main/img/chess.svg"
}

function get_board(board){
    gameSocket.send(JSON.stringify({
        "type": "GET_BOARD",
        "room_id": roomCode,
        "color": player_color,
    }));
}

function clear_board(){
    $(".cell_item").remove()
}

$(function () {
    first_connect()
})

function first_connect(){
    $.ajax({
        type: "POST",
        url: boardApi("first_connect/"),
        headers: {
            "X-CSRFToken": readCsrfToken(),
        },
        success: function(response){
            if (response["success"]){
                if (response["sandbox"]) {
                    sandboxMode = true
                    $("#sandbox-banner").removeClass("d-none")
                    sandboxOrderedTurn = !!response["sandbox_ordered_turn"]
                    updateSandboxTurnModeUI()
                }
                if (response["is_spectator"]){
                    start_spectator_options()
                }
                else{
                    start_player_options()
                }
            }
        }
    })
}

function start_spectator_options(){
    $.ajax({
        type: "POST",
        url: boardApi("get_color_and_ready/"),
        headers: {
            "X-CSRFToken": readCsrfToken(),
        },
        data: {
            "is_spectator": 1,
        },
        success: function(response){
            if (response["success"]){
                player_color = "white"
                sandboxOrderedTurn = !!response["sandbox_ordered_turn"]
                updateSandboxTurnModeUI()
                $("#player-color-display").text(colorRu(player_color))
                $("#spectator-display").text("Наблюдатель")
                $("#room-code-display").text(roomCode || "—")
                $(".ready-hint").addClass("d-none")
                $("#ready-row").addClass("d-none")
                get_board($(".board"))
            }
        }
    })
}

function start_player_options(){
    $.ajax({
        type: "POST",
        url: boardApi("get_color_and_ready/"),
        headers: {
            "X-CSRFToken": readCsrfToken(),
        },
        data: {
            "is_spectator": 0,
        },
        success: function(response){
            if (response["success"]){
                player_color = response["color"]
                player_ready = response["ready"]
                if (response["sandbox"]) {
                    sandboxMode = true
                    $("#sandbox-banner").removeClass("d-none")
                    $("#sandbox-perspective").removeClass("d-none")
                    $("#sandbox-turn-mode").removeClass("d-none")
                    sandboxOrderedTurn = !!response["sandbox_ordered_turn"]
                    updateSandboxTurnModeUI()
                    $("#player-color-display").text("Все цвета (песочница)")
                } else {
                    $("#player-color-display").text(colorRu(player_color))
                }
                $("#spectator-display").text("Игрок")
                $("#room-code-display").text(roomCode || "—")
                update_ready(player_ready)
                if (response["is_started"]){
                    $("#ready-row").addClass("d-none")
                }
                get_board($(".board"))
            }
        }
    })
}

$(document).on("click", ".cell_item", function() {
    if (!($(this).attr("class").split(" ").includes("point"))){
        let id = $(this).attr('id')
        let letter = id.slice(0, 1)
        let number = id.slice(1)
        get_dots(letter, number)
    }
});

$(document).on("click", ".perspective-btn", function () {
    if (!sandboxMode) return
    const color = $(this).data("color")
    setPerspective(color)
})

$(document).on("click", ".turn-mode-btn", function () {
    if (!sandboxMode) return
    const ordered = $(this).data("mode") === "ordered"
    sandboxOrderedTurn = ordered
    updateSandboxTurnModeUI()
    update_turn(player_turn)
    gameSocket.send(JSON.stringify({
        "type": "SET_SANDBOX_TURN_MODE",
        "room_id": roomCode,
        "ordered": ordered
    }))
})

function paint_dots(dots){
    let red_circle = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="11" fill="%23d94b4b" fill-opacity="0.7" stroke="%238f1f1f" stroke-width="2"/></svg>'
    let grey_circle = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="9" fill="%23c5c9cf" fill-opacity="0.85" stroke="%23868d96" stroke-width="2"/></svg>';
    let green_circle = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="10" fill="%234ccf7a" fill-opacity="0.7" stroke="%231f8f49" stroke-width="2"/></svg>'
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
        set_cell_picture(board, red_circle, letter, number, false, "eat_point point", true)
    });
}

function get_dots(letter, number, ignore_duplication = false){
    var $cell = $("#" + letter + number)
    var pieceColor = pieceColorFromElement($cell)
    var canSelect = sandboxMode
        ? pieceColor !== null
        : $cell.hasClass(player_color)
    if (!canSelect) return
    activeMoveColor = sandboxMode ? pieceColor : player_color
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
        'color': activeMoveColor,
        'ignore_duplication': ignore_duplication,
    }));
}

$(document).on("click", ".point", async function() {
    var moveColor = sandboxMode ? activeMoveColor : player_color
    if (!sandboxMode && player_turn != player_color) return
    if (sandboxMode && !moveColor) return
    if ($(this).attr("class").split(" ").includes("eat_point")) return
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
        "cell": cell,
        "room_id": roomCode,
        "color": moveColor,
    }));
});

$(document).on("click", ".eat_point", async function(){
    var moveColor = sandboxMode ? activeMoveColor : player_color
    if (!sandboxMode && player_turn != player_color) return
    if (sandboxMode && !moveColor) return
    var cell = $(this).attr("id")
    if (!cell) return
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
        "cell": cell,
        "room_id": roomCode,
        "color": moveColor,
    }));
});


$(document).on("click", ".board", function(){
    $(".point").remove()
    gameSocket.send(JSON.stringify({
        "type": "RESET_DOTS",
        "color": player_color,
    }));
})


function change_color(color){
    gameSocket.send(JSON.stringify({
        "type": "CHANGE_COLOR",
        "color": color
    }));
}

$(document).on("click", "#btn_ready_self", function () {
    gameSocket.send(JSON.stringify({
        "type": "TOGGLE_READY",
        "color": player_color
    }));
})
    

function update_ready(player_ready) {
    var btn = $("#btn_ready_self")
    btn.removeClass("btn-outline-secondary btn-success btn-dark btn-light")
    if (player_ready == 0) {
        btn.addClass("btn-outline-secondary")
        btn.text("Не готов")
    } else {
        btn.addClass("btn-success")
        btn.text("Готов")
    }
}

function update_turn(player_turn) {
    var el = $("#turn-display")
    if (sandboxMode && !sandboxOrderedTurn) {
        el.attr("class", "badge rounded-pill game-turn-badge w-100 py-2 d-inline-block bg-warning text-dark")
        el.text("Песочница: ход без очереди")
        return
    }
    el.attr("class", turnBadgeClasses(player_turn))
    el.text("Сейчас ход: " + colorRu(player_turn))
}
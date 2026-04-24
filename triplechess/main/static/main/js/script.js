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
var privateMode = !!(typeof window.__BOARD_INIT__ !== "undefined" && window.__BOARD_INIT__.isPrivate)
var gameStarted = !!(typeof window.__BOARD_INIT__ !== "undefined" && window.__BOARD_INIT__.isStarted)
var activeMoveColor = null
var setupCellPolygons = {}
var setupCellCenters = {}
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
    // Turn mode switch is intentionally removed from UI.
}
updateSandboxTurnModeUI()

const BOARD_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "K", "L", "M", "N"]
const BOARD_NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
var selectedSetupPiece = null
const SETUP_PIECES = [
    { type: "King", color: "white" }, { type: "Queen", color: "white" }, { type: "Tara", color: "white" }, { type: "Officer", color: "white" }, { type: "Horse", color: "white" }, { type: "Peshka", color: "white" },
    { type: "King", color: "black" }, { type: "Queen", color: "black" }, { type: "Tara", color: "black" }, { type: "Officer", color: "black" }, { type: "Horse", color: "black" }, { type: "Peshka", color: "black" },
    { type: "King", color: "red" }, { type: "Queen", color: "red" }, { type: "Tara", color: "red" }, { type: "Officer", color: "red" }, { type: "Horse", color: "red" }, { type: "Peshka", color: "red" }
]

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
                $(".board-wrapper > img.cell_item").addClass("old_cell")
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
                $(".board-wrapper > img.old_cell").remove()
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
                setTimeout(function () { buildSetupHitPolygons() }, 0)
                break;
            case "GET_DOTS":
                $(".point").remove()
                dots = data["dots"]
                paint_dots(dots)
                setTimeout(function () { buildSetupHitPolygons() }, 0)
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
                gameStarted = true
                updateSetupUI()
                break;
            case "SANDBOX_TURN_MODE":
                if (typeof data["ordered"] !== "undefined") {
                    sandboxOrderedTurn = !!data["ordered"]
                    updateSandboxTurnModeUI()
                    update_turn(player_turn)
                }
                break;
            case "TURN_SET":
                if (data["turn"]) {
                    player_turn = data["turn"]
                    update_turn(player_turn)
                    get_board($(".board"))
                }
                break;
            case "SETUP_UPDATED":
                get_board($(".board"))
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
    $(".board-wrapper > img.cell_item").remove()
}

$(function () {
    renderSetupPalette()
    renderSetupDropzones()
    buildSetupHitPolygons()
    $(".board").on("load", function () {
        buildSetupHitPolygons()
    })
    updateSetupUI()
    first_connect()
})

$(window).on("resize", function () {
    buildSetupHitPolygons()
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
                privateMode = !!response["is_private"]
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
                gameStarted = true
                $("#player-color-display").text(colorRu(player_color))
                $("#spectator-display").text("Наблюдатель")
                $("#room-code-display").text(roomCode || "—")
                $(".ready-hint").addClass("d-none")
                $("#ready-row").addClass("d-none")
                updateSetupUI()
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
                    sandboxOrderedTurn = !!response["sandbox_ordered_turn"]
                    updateSandboxTurnModeUI()
                    $("#player-color-display").text("Все цвета (песочница)")
                } else {
                    $("#player-color-display").text(colorRu(player_color))
                }
                privateMode = !!response["is_private"]
                gameStarted = !!response["is_started"]
                $("#spectator-display").text("Игрок")
                $("#room-code-display").text(roomCode || "—")
                update_ready(player_ready)
                if (response["is_started"]){
                    $("#ready-row").addClass("d-none")
                }
                updateSetupUI()
                get_board($(".board"))
            }
        }
    })
}

function boardImgsOnCell(cell) {
    return $(".board-wrapper > img").filter(function () { return this.id === String(cell) })
}

$(document).on("click", ".perspective-btn", function () {
    if (!sandboxMode) return
    const color = $(this).data("color")
    setPerspective(color)
})

$(document).on("click", ".set-turn-btn", function () {
    if (!sandboxMode || !privateMode || !gameStarted) return
    const color = $(this).data("color")
    if (color !== "white" && color !== "black" && color !== "red") return
    gameSocket.send(JSON.stringify({
        "type": "SET_TURN",
        "room_id": roomCode,
        "color": color
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
    if (privateMode && !gameStarted) return
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

function sendMoveToCellFromDropzone(letter, number) {
    if (privateMode && !gameStarted) return
    var moveColor = sandboxMode ? activeMoveColor : player_color
    if (!sandboxMode && player_turn != player_color) return
    if (sandboxMode && !moveColor) return
    var l = letter
    var n = number
    if (player_color == "black") {
        l = RED_TURN[letter]
        n = RED_TURN[number]
    }
    if (player_color == "red") {
        l = BLACK_TURN[letter]
        n = BLACK_TURN[number]
    }
    var cell = l + n
    $(".point").remove()
    gameSocket.send(JSON.stringify({
        "type": "MOVE",
        "cell": cell,
        "room_id": roomCode,
        "color": moveColor
    }))
}

function sendChangePositionFromDropzone(letter, number) {
    if (privateMode && !gameStarted) return
    var moveColor = sandboxMode ? activeMoveColor : player_color
    if (!sandboxMode && player_turn != player_color) return
    if (sandboxMode && !moveColor) return
    var l = letter
    var n = number
    if (player_color == "black") {
        l = RED_TURN[letter]
        n = RED_TURN[number]
    }
    if (player_color == "red") {
        l = BLACK_TURN[letter]
        n = BLACK_TURN[number]
    }
    var cell = l + n
    $(".point").remove()
    gameSocket.send(JSON.stringify({
        "type": "CHANGE_POSITION",
        "cell": cell,
        "room_id": roomCode,
        "color": moveColor
    }))
}

function handlePlayCellFromHit(letter, number, cell) {
    var $on = boardImgsOnCell(cell)
    if ($on.filter(".eat_point").length) {
        sendChangePositionFromDropzone(letter, number)
        return
    }
    if ($on.filter(".point").length) {
        sendMoveToCellFromDropzone(letter, number)
        return
    }
    get_dots(letter, number)
}

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
    if (privateMode && !gameStarted) {
        el.attr("class", "badge rounded-pill game-turn-badge w-100 py-2 d-inline-block bg-info text-dark")
        el.text("Режим расстановки: перетащите фигуры и нажмите Старт")
        return
    }
    el.attr("class", turnBadgeClasses(player_turn))
    el.text("Сейчас ход: " + colorRu(player_turn))
}

function boardCellToCanonical(letter, number) {
    if (player_color == "black") {
        letter = RED_TURN[letter]
        number = RED_TURN[number]
    }
    if (player_color == "red") {
        letter = BLACK_TURN[letter]
        number = BLACK_TURN[number]
    }
    return { letter: letter, number: number }
}

function renderSetupPalette() {
    var box = $("#setup-pieces")
    if (!box.length) return
    box.empty()
    SETUP_PIECES.forEach(function (piece) {
        var path = img_from_type(piece.type, piece.color)
        var btn = $("<button type='button' class='setup-piece' draggable='true'></button>")
        btn.attr("data-type", piece.type)
        btn.attr("data-color", piece.color)
        btn.attr("title", piece.type + " / " + piece.color)
        btn.append("<img src='" + path + "' alt='" + piece.type + "' draggable='false'>")
        box.append(btn)
    })
    var eraser = $("<button type='button' class='setup-piece setup-piece--eraser' draggable='true' title='Убрать фигуру'>Ластик</button>")
    eraser.attr("data-action", "erase")
    box.append(eraser)
}

function renderSetupDropzones() {
    $(".setup-dropzone").remove()
    var board = $(".board")
    BOARD_LETTERS.forEach(function (letter) {
        BOARD_NUMBERS.forEach(function (number) {
            var cell = letter + number
            var dz = $("<div class='setup-dropzone cell_item cell_item" + cell + "'></div>")
            dz.attr("data-cell", cell)
            board.after(dz)
        })
    })
}

function getCellCentersFromCss() {
    var wrapper = $(".board-wrapper")
    if (!wrapper.length) return {}
    var wrapperRect = wrapper[0].getBoundingClientRect()
    var centers = {}
    $(".setup-dropzone").each(function () {
        var cell = String($(this).data("cell") || "")
        if (!cell) return
        var rect = this.getBoundingClientRect()
        centers[cell] = {
            x: rect.left + rect.width / 2 - wrapperRect.left,
            y: rect.top + rect.height / 2 - wrapperRect.top
        }
    })
    return centers
}

function midpoint(a, b) {
    return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }
}

function buildSetupHitPolygons() {
    setupCellCenters = getCellCentersFromCss()
    setupCellPolygons = {}
    var keys = Object.keys(setupCellCenters)
    if (!keys.length) return
    keys.forEach(function (cell) {
        var c = setupCellCenters[cell]
        var buckets = { ul: null, ur: null, dr: null, dl: null }
        keys.forEach(function (otherCell) {
            if (otherCell === cell) return
            var o = setupCellCenters[otherCell]
            var dx = o.x - c.x
            var dy = o.y - c.y
            if (dx === 0 || dy === 0) return
            var dist = Math.hypot(dx, dy)
            var key = null
            if (dx < 0 && dy < 0) key = "ul"
            if (dx > 0 && dy < 0) key = "ur"
            if (dx > 0 && dy > 0) key = "dr"
            if (dx < 0 && dy > 0) key = "dl"
            if (!key) return
            if (!buckets[key] || dist < buckets[key].dist) buckets[key] = { p: o, dist: dist }
        })
        if (!(buckets.ul && buckets.ur && buckets.dr && buckets.dl)) return
        setupCellPolygons[cell] = [
            midpoint(c, buckets.ul.p),
            midpoint(c, buckets.ur.p),
            midpoint(c, buckets.dr.p),
            midpoint(c, buckets.dl.p),
        ]
    })
}

function pointInPolygon(point, polygon) {
    var inside = false
    for (var i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        var xi = polygon[i].x, yi = polygon[i].y
        var xj = polygon[j].x, yj = polygon[j].y
        var intersect = ((yi > point.y) !== (yj > point.y)) &&
            (point.x < (xj - xi) * (point.y - yi) / ((yj - yi) || 1e-9) + xi)
        if (intersect) inside = !inside
    }
    return inside
}

function findSetupCellByPoint(x, y) {
    var p = { x: x, y: y }
    for (var cell in setupCellPolygons) {
        if (pointInPolygon(p, setupCellPolygons[cell])) return cell
    }
    var nearest = null
    var best = Infinity
    for (var c in setupCellCenters) {
        var cc = setupCellCenters[c]
        var d = Math.hypot(cc.x - x, cc.y - y)
        if (d < best) {
            best = d
            nearest = c
        }
    }
    // Strict fallback: only accept near-center hits.
    return best <= 26 ? nearest : null
}

function updateSetupUI() {
    if (privateMode && !gameStarted) {
        $("#setup-panel").removeClass("d-none")
        $("#setup-controls").removeClass("d-none")
        $("#sandbox-set-turn").addClass("d-none")
        $("#ready-row").addClass("d-none")
        $(".setup-dropzone").removeClass("setup-dz--play").addClass("setup-dz--setup")
        update_turn(player_turn)
        setTimeout(function () { buildSetupHitPolygons() }, 0)
        return
    }
    $("#setup-panel").addClass("d-none")
    $("#setup-controls").addClass("d-none")
    selectedSetupPiece = null
    $(".setup-piece").removeClass("active")
    if (sandboxMode) $("#sandbox-set-turn").removeClass("d-none")
    $(".setup-dropzone").removeClass("setup-dz--setup").addClass("setup-dz--play")
    setTimeout(function () { buildSetupHitPolygons() }, 0)
}

$(document).on("dragstart", ".setup-piece", function (e) {
    var payload = {
        type: $(this).data("type") || null,
        color: $(this).data("color") || null,
        action: $(this).data("action") || "place"
    }
    e.originalEvent.dataTransfer.setData("text/plain", JSON.stringify(payload))
    e.originalEvent.dataTransfer.effectAllowed = "copy"
})

$(document).on("dragover", ".setup-dropzone", function (e) {
    if (!(privateMode && !gameStarted)) return
    e.preventDefault()
    $(this).addClass("drag-over")
})

$(document).on("dragleave", ".setup-dropzone", function () {
    $(this).removeClass("drag-over")
})

$(document).on("drop", ".setup-dropzone", function (e) {
    if (!(privateMode && !gameStarted)) return
    e.preventDefault()
    e.stopPropagation()
    $(this).removeClass("drag-over")
    var raw = e.originalEvent.dataTransfer.getData("text/plain")
    if (!raw) return
    var data = null
    try { data = JSON.parse(raw) } catch (err) { return }
    var cell = String($(this).data("cell") || "")
    if (!cell) return
    var letter = cell.slice(0, 1)
    var number = cell.slice(1)
    var canonical = boardCellToCanonical(letter, number)
    gameSocket.send(JSON.stringify({
        "type": "PLACE_FIGURE",
        "room_id": roomCode,
        "cell": canonical.letter + canonical.number,
        "piece_type": data.type,
        "piece_color": data.color,
        "action": data.action || "place"
    }))
})

$(document).on("dragover", ".board-wrapper", function (e) {
    if (!(privateMode && !gameStarted)) return
    e.preventDefault()
})

$(document).on("drop", ".board-wrapper", function (e) {
    if (!(privateMode && !gameStarted)) return
    e.preventDefault()
    var raw = e.originalEvent.dataTransfer.getData("text/plain")
    if (!raw) return
    var data = null
    try { data = JSON.parse(raw) } catch (err) { return }
    var rect = this.getBoundingClientRect()
    var x = e.originalEvent.clientX - rect.left
    var y = e.originalEvent.clientY - rect.top
    var cell = findSetupCellByPoint(x, y)
    if (!cell) return
    var canonical = boardCellToCanonical(cell.slice(0, 1), cell.slice(1))
    gameSocket.send(JSON.stringify({
        "type": "PLACE_FIGURE",
        "room_id": roomCode,
        "cell": canonical.letter + canonical.number,
        "piece_type": data.type,
        "piece_color": data.color,
        "action": data.action || "place"
    }))
})

$(document).on("click", ".setup-piece", function () {
    if (!(privateMode && !gameStarted)) return
    $(".setup-piece").removeClass("active")
    $(this).addClass("active")
    selectedSetupPiece = {
        type: $(this).data("type") || null,
        color: $(this).data("color") || null,
        action: $(this).data("action") || "place"
    }
})

$(document).on("click", ".board-wrapper", function (e) {
    if ($(e.target).closest("a, button, [role='button']").length) return
    var rect = this.getBoundingClientRect()
    var x = e.clientX - rect.left
    var y = e.clientY - rect.top
    var cell = findSetupCellByPoint(x, y)

    if (privateMode && !gameStarted) {
        if (cell && selectedSetupPiece) {
            var canonical = boardCellToCanonical(cell.slice(0, 1), cell.slice(1))
            gameSocket.send(JSON.stringify({
                "type": "PLACE_FIGURE",
                "room_id": roomCode,
                "cell": canonical.letter + canonical.number,
                "piece_type": selectedSetupPiece.type,
                "piece_color": selectedSetupPiece.color,
                "action": selectedSetupPiece.action || "place"
            }))
        } else if (!cell) {
            $(".point").remove()
            gameSocket.send(JSON.stringify({
                "type": "RESET_DOTS",
                "color": player_color
            }))
        }
        return
    }

    if (!cell) {
        $(".point").remove()
        gameSocket.send(JSON.stringify({
            "type": "RESET_DOTS",
            "color": player_color
        }))
        return
    }

    var letter = cell.slice(0, 1)
    var number = cell.slice(1)
    handlePlayCellFromHit(letter, number, cell)
})

$(document).on("click", "#btn_start_private_game", function () {
    if (!(privateMode && !gameStarted)) return
    gameSocket.send(JSON.stringify({
        "type": "START_PRIVATE_GAME",
        "room_id": roomCode
    }))
})

$(document).on("click", "#btn_setup_clear", function () {
    if (!(privateMode && !gameStarted)) return
    if (!confirm("Убрать все фигуры с доски?")) return
    gameSocket.send(JSON.stringify({
        "type": "CLEAR_SETUP",
        "room_id": roomCode
    }))
})

$(document).on("click", "#btn_setup_starting", function () {
    if (!(privateMode && !gameStarted)) return
    gameSocket.send(JSON.stringify({
        "type": "LOAD_STARTING_POSITION",
        "room_id": roomCode
    }))
})
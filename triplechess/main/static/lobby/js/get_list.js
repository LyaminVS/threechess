let filter_status = "in_lobby";

function readCsrfToken() {
    const m = document.querySelector('meta[name="csrf-token"]');
    return m ? m.getAttribute("content") : "";
}

function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}

function get_list(filter_status_arg) {
    $(".point").remove();
    $.ajax({
        type: "POST",
        url: "get_list/",
        headers: {
            "X-CSRFToken": readCsrfToken(),
        },
        data: {
            filter_status: filter_status_arg,
        },
        success: function (response) {
            const wrapper = $(".list_games_wrapper");
            wrapper.empty();

            let games;
            try {
                games = JSON.parse(response.games);
            } catch (e) {
                games = [];
            }

            const emptyEl = $("#lobby-empty");
            if (!games.length) {
                emptyEl.removeClass("d-none");
            } else {
                emptyEl.addClass("d-none");
            }

            games.forEach(function (game) {
                const p1 = game.player_1 || "—";
                const p2 = game.player_2 || "—";
                const p3 = game.player_3 || "—";
                const id = game.id;
                const adminDeleteBtn = game.can_delete
                    ? '<button type="button" class="btn btn-outline-danger btn-sm btn_delete_game" id="btn_delete_game_' +
                      id +
                      '">Удалить</button>'
                    : "";

                const sandboxBadge = game.is_sandbox
                    ? '<span class="badge bg-warning text-dark ms-1">Песочница</span>'
                    : "";
                const privateBadge = game.is_private
                    ? '<span class="badge bg-info text-dark ms-1">Приватная</span>'
                    : "";
                const card = $(
                    '<div class="col-12 col-md-6 col-xl-4">' +
                        '<article class="card game-card h-100 border-0 shadow-sm" id="game_' +
                        id +
                        '">' +
                        '<div class="card-body d-flex flex-column">' +
                        '<div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-1">' +
                        '<span class="badge rounded-pill lobby-room-badge">Комната #' +
                        escapeHtml(id) +
                        "</span>" +
                        sandboxBadge +
                        privateBadge +
                        "</div>" +
                        '<ul class="list-unstyled small flex-grow-1 mb-3 lobby-players-list">' +
                        "<li><span class=\"text-muted\">Игрок 1</span> " +
                        escapeHtml(p1) +
                        "</li>" +
                        "<li><span class=\"text-muted\">Игрок 2</span> " +
                        escapeHtml(p2) +
                        "</li>" +
                        "<li><span class=\"text-muted\">Игрок 3</span> " +
                        escapeHtml(p3) +
                        "</li>" +
                        "</ul>" +
                        '<div class="d-grid gap-2 d-sm-flex justify-content-sm-end mt-auto">' +
                        '<button type="button" class="btn btn-primary btn-sm btn_join_game" id="btn_join_game_' +
                        id +
                        '">Войти в игру</button>' +
                        '<button type="button" class="btn btn-outline-secondary btn-sm btn_join_spectator" id="btn_join_spectator_' +
                        id +
                        '">Наблюдать</button>' +
                        adminDeleteBtn +
                        "</div>" +
                        "</div>" +
                        "</article>" +
                        "</div>"
                );
                wrapper.append(card);
            });
        },
    });
}

get_list(filter_status);
let interval = setInterval(get_list, 5000, filter_status);

$(document).on("click", "#btn_in_lobby_games", function () {
    $("#btn_started_games").removeClass("active");
    $("#btn_in_lobby_games").addClass("active");
    filter_status = "in_lobby";
    get_list(filter_status);
    clearInterval(interval);
    interval = setInterval(get_list, 5000, filter_status);
});

$(document).on("click", "#btn_started_games", function () {
    $("#btn_in_lobby_games").removeClass("active");
    $("#btn_started_games").addClass("active");
    filter_status = "started";
    get_list(filter_status);
    clearInterval(interval);
    interval = setInterval(get_list, 5000, filter_status);
});

$(document).on("click", ".btn_delete_game", function () {
    const id = this.id.split("_")[3];
    if (!confirm("Удалить эту игру?")) return;
    $.ajax({
        type: "POST",
        url: "delete_game/",
        headers: {
            "X-CSRFToken": readCsrfToken(),
        },
        data: {
            game_id: id,
        },
        success: function (response) {
            if (response.success) {
                get_list(filter_status);
            }
        },
    });
});

// var url = document.location.href
// var roomCode = url.split("/")[url.split("/").length - 2]
// var connectionString = 'ws://' + window.location.host + '/ws/room/' + roomCode + '/';
// var gameSocket = new WebSocket(connectionString);
// connect();

// function connect() {
//     gameSocket.onopen = function open() {
//         gameSocket.send(JSON.stringify({
//             "type": "START",
//             "roomCode": roomCode,
//         }));
//     };

//     gameSocket.onclose = function (e) {
//         console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
//         setTimeout(function () {
//             connect();
//         }, 1000);
//     };

//     gameSocket.onmessage = function (e) {
//         let data = JSON.parse(e.data);
//         data = data["payload"];
//         let type = data["type"];
//         switch (type) {
//             case "START":
//                 break;
//             case "UPDATE_USER_NAMES":
//                 if (data["player_1_name"]){
//                     $("#player_name_1").text(data["player_1_name"])
//                 }
//                 else{
//                     $("#player_name_1").text("Игрок 1")
//                 }
//                 if (data["player_2_name"]){
//                     $("#player_name_2").text(data["player_2_name"])
//                 }
//                 else{
//                     $("#player_name_2").text("Игрок 2")
//                 }
//                 if (data["player_3_name"]){
//                     $("#player_name_3").text(data["player_3_name"])
//                 }
//                 else{
//                     $("#player_name_3").text("Игрок 3")
//                 }
//                 update_radio(data)
//                 break;
//             case "END":
//                 break;
//             case "UPDATE_RADIO":
//                 update_radio(data)
//                 break
//             case "END":
//                 break;
//             default:
//                 break;

//         }
//     };

//     if (gameSocket.readyState == WebSocket.OPEN) {
//         gameSocket.onopen();
//     }

//     function update_radio(data){     
//         if (data["player_1_ready"] == 1){
//             $("#radio_wrapper_1").empty()
//             $("#radio_wrapper_1").append(data["player_1_color"])
//         }
//         if (data["player_2_ready"] == 1) {
//             $("#radio_wrapper_2").empty()
//             $("#radio_wrapper_2").append(data["player_2_color"])
//         }
//         if (data["player_3_ready"] == 1) {
//             $("#radio_wrapper_3").empty()
//             $("#radio_wrapper_3").append(data["player_3_color"])
//         }
//     }
// }



// function ajax_button_ready(player_num){

//     let value = $('input[name="radio_' + player_num + '"]:checked').val();
//     $.ajax({
//         type: "POST",
//         url: "button_pressed_check/",
//         headers: {
//             "X-CSRFTOKEN": "{{ csrf_token }}",
//         },
//         data: {
//             "player": player_num,
//             "radio": value,
//         },
//         success: function(data){
//             alert(123132)
//             $("#radio_wrapper" + player_num).html('<div class="form-check"><input class="form-check-input" name="radio_1" type="radio" id="radio_base_1" value="random"> <label class="form-check-label" for="radio_base_1">нот селектед</label></div><div class="form-check"><input class="form-check-input" name="radio_1" type="radio" id="radio_white_1" value="white"><label class="form-check-label" for="radio_white_1">Вайт</label></div><div class="form-check"><input class="form-check-input" name="radio_1" type="radio" id="radio_black_1" value="black"><label class="form-check-label" for="radio_black_1">Блэк</label></div><div class="form-check"><input class="form-check-input" name="radio_1" type="radio" id="radio_red_1" value="red"><label class="form-check-label" for="radio_red_1">Рэд</label></div>')
//             res = {
//                 "type": "UPDATE_RADIO",
//                 "roomCode": roomCode,
//             }
//             gameSocket.send(JSON.stringify(res));
                
//         }
//     });
// }

// $(document).on("click", "#btn_ready_1", function(){
//     ajax_button_ready(1)
// })

// $(document).on("click", "#btn_ready_2", function(){
//     ajax_button_ready(2)
// })

// $(document).on("click", "#btn_ready_3", function(){
//     ajax_button_ready(3)
// })

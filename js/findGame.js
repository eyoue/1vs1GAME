var hod_change = ''; // Резултат хода. Что выбрано
var state = "right"; // Каким игроком играем
var endGame = false; // Конец игры?
var GameTimer = 0; // Таймер для хода

// Вкл таймер
function setGameTimer() {
    $('.seconds').text(10)
    var _Seconds = $('.seconds').text()
    GameTimer = setInterval(function() { // запускаем интервал
        if (_Seconds > 0) {
            _Seconds--; // вычитаем 1
            $('.seconds').text(_Seconds); // выводим получившееся значение в блок
        } else {
            clearInterval(GameTimer);
            hod_change = 'a1'
            $('#btnStart').trigger('click')
        }
    }, 1000);
}

// Выкл таймер
function stopGameTimer() {
    clearInterval(GameTimer)
    $('.seconds').text("ждём..")
}

// Создать соединение
function Connect() {
    var socket = new WebSocket("ws://localhost:8881")
    socket.onopen = function() {};
    socket.onclose = function(event) {};
    socket.onmessage = function(event) {

        // Так проверяю: кто есть кто. Кто слева, а кто справа
        if (event.data == "start_1") {
            document.getElementById('mainFind').style.display = "none";
            document.getElementById('main').style.display = "";

            var def = $('.def')
            var attac = $('.attac')

            def.addClass('attac').removeClass('def');
            attac.addClass('def').removeClass('attac')
            state = "left"
            setGameTimer()

        }
        if (event.data == "start_2") {
            document.getElementById('mainFind').style.display = "none";
            document.getElementById('main').style.display = "";
            setGameTimer()
        }

        // Тут проверяем кого бить, кого не бить
        if (event.data == "hitALL") {
            hit("hitALL")
        }
        if (event.data == "hitYOU") {
            hit("hitYOU")
        }
        if (event.data == "hitOPONENT") {
            hit("hitOPONENT")
        }
        if (event.data == "NOhit") {
            hit("NOhit")
        }

        // Закрыть сессию
        if (event.data == "close") {
            closeGame()
        }


    };
    socket.onerror = function(error) {
        console.log("Ошибка " + error.message);
    };

    // Если вдруг кто-то решил закрыть во время игры страницу
    window.onbeforeunload = function() {
        setTimeout(socket.send('close'), 200)
    }

    // Кнопка отправить. Собственно берем результат хода и отправляем серверу
    $('#btnStart').click(function() {
        stopGameTimer()
        $('#btnStart').attr('src')
        if ($('#btnStart').attr('src') == "images/btnOff.png") {
            $('#btnStart').attr('src', "images/btnOn.png")
            if (hod_change == '') {
                hod_change = 'a1'
            }
            if (state == 'left') {
                setTimeout(socket.send('H' + hod_change), 500)
            } else {
                setTimeout(socket.send('H' + hod_change), 600)
            }
            hod_change == ''
        }
    })
}

// Кнопка Играть
function startGame() {
    if ($('#btnFindStart').attr('src') == "images/btnFindOn.png") {
        $('#btnFindStart').attr('src', "images/btnFindOff.png")
        $('#btnSpan').text("Играть")
    } else {
        $('#btnFindStart').attr('src', "images/btnFindOn.png")
        $('#btnSpan').text("Ожидание оппонента...")
        Connect()
    }
}

// Берем результат хода
function hod(t) {
    hod_change = $(t).attr('class').substring(0, 1) + $(t).val();

    if ($(t).is(':checked')) {
        $('input:checkbox').not(t).prop('checked', false);
    }
}

// Отнять ХП (Анимация)
function hit(_action) {

    if (_action == "hitYOU") {
        if (state == 'left') {
            $('#hpL').height($('#hpL').height())
            $('#hpL').width($("#hpL").width() - 6)
        } else {
            $('#hpR').height($('#hpR').height())
            $('#hpR').width($("#hpR").width() - 6)
        }
    }
    if (_action == "hitOPONENT") {
        if (state == 'right') {
            $('#hpL').height($('#hpL').height())
            $('#hpL').width($("#hpL").width() - 6)
        } else {
            $('#hpR').height($('#hpR').height())
            $('#hpR').width($("#hpR").width() - 6)
        }

    }
    if (_action == "NOhit") {}

    if (_action == "hitALL") {
        $('#hpL').height($('#hpL').height())
        $('#hpL').width($("#hpL").width() - 6)
        $('#hpR').height($('#hpR').height())
        $('#hpR').width($("#hpR").width() - 6)
    }


    $('#btnStart').attr('src', "images/btnOff.png")
    $('body input:checkbox').prop('checked', false);

    setGameTimer()

    if ($('#hpL').width() == 0 || $('#hpR').width() == 0) {
        closeGame()
    }
}

// Закрыть игру: умнее перезагрузки ничего не придумал
function closeGame() {
    location.reload()

}
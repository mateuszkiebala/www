<!-- Modal script -->
$(document).ready (function () {
    var modal = document.getElementById('myModal'); // New template of modal_table.
    var newModalTable = '<table id="modal_table" class="display" width="100%" cellspacing="0"> <thead> </thead> <tbody> </tbody></table>';
    var span = document.getElementsByClassName("close")[0]; // Get the <span> element that closes the modal
    var rowCount = 0;   // Number of rows in modal table.
    var clicked = '';    // Clicked field in array.
    var headers = ['Gmina', 'Województwo', 'Mieszkańcy', 'Uprawnione osoby', 'Wydane karty', 'Głosy', 'Ważne głosy'];    // List of headers.
    var engHeaders = ['commune', 'province_name', 'inhabitants', 'entitled_inhabitants', 'distributed_ballots', 'votes', 'valid_votes'];
    var candidates = []; // Names of candidates.
    var disableInputData = ['Gmina', 'Województwo']; // List of disable headers.

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        closeEvent();
    };

    // Action that happens while closing modal.
    function closeEvent () {
        getMapData();
        generalInfoHandler();
        provinceTableHandler();
        communeTypeTableHandler();
        rangesTableHandler();
        modal.style.display = "none";
        $('#modal_table').remove();
        $('.modal-body').append(newModalTable);
    }

    // When the user clicks anywhere outside of the modal, close it.
    window.onclick = function(event) {
        if (event.target == modal) {
            closeEvent();
        }
    };

    if (window.addEventListener) {
        window.addEventListener('load', run, false);
    } else if (window.attachEvent) {
        window.attachEvent('onload', run);
    }

    // Creates html that displays headers for modal table.
    function setHeaders(data) {
        for (var i = 0; i < data.length; i++) {
            var html = '';
            var candidates_start_index = 7;
            var val = JSON.parse(data[i]);
            headers[candidates_start_index] = val['candidate_0'];
            headers[candidates_start_index + 1] = val['candidate_1'];
            candidates[0] = val['candidate_0'];
            candidates[1] = val['candidate_1'];
            for (var j = 0; j < headers.length; j++) {
                html += '<td class="modal_header_data">' + headers[j] + '</td>';
            }
            headers[candidates_start_index] = 'candidate_0_votes';
            headers[candidates_start_index + 1] = 'candidate_1_votes';
            engHeaders[candidates_start_index] = headers[candidates_start_index];
            engHeaders[candidates_start_index + 1] = headers[candidates_start_index + 1];

            $('#modal_table thead').append('<tr>' + html + '</tr>');
        }
    }

    // Creates html that displays table with data from server.
    function setModalData(data) {
        rowCount = data.length;
        for (var i = 0; i < data.length; i++) {
            var html = '';
            var val = JSON.parse(data[i]);
            for (var j = 0; j < headers.length; j++) {
                html += '<td class="data_change_' + i + ' modal_data_style ">' + val[engHeaders[j]] + '</td>';
            }
            var id = 'id="button_change_' + i + '"';
            var button = '<td> <button ' + id + '>Modyfikuj</button> </td>';
            $('#modal_table tbody').append('<tr>' + html + button + '</tr>');
            modalButtonsControl(i);
        }
    }

    // Handler for modify button state.
    function modifyButton(button, fields) {
        for (var j = 0; j < fields.length; j++) {
            if ($.inArray(headers[j], disableInputData) == -1) {
                fields[j].innerHTML = '<input size="3" type="text" value="' + fields[j].innerText + '"/>';
            }
        }
        button.innerHTML = "Zapisz";
    }

    // Gets data from clicked row.
    function prepareDataToSend(fields) {
        var dataToSend = new Object();
        // Add candidates names.
        for (var j = 0; j < candidates.length; j++) {
            var index_name = 'candidate_' + j + '_name';
            dataToSend[index_name] = candidates[j];
        }

        for (var j = 0; j < fields.length; j++) {
            if ($.inArray(headers[j], disableInputData) == -1) {
                dataToSend[engHeaders[j]] = fields[j].childNodes[0].value;
            } else {
                dataToSend[engHeaders[j]] = fields[j].innerText;
            }
        }
        return dataToSend;
    }

    // Display info about modification.
    function showDialogBox(resp) {
        resp = JSON.parse(resp);
        var user = resp['user'];
        var date = resp['date'];
        return confirm("Ostatnia modyfikacja została wykonana przez użytkownika:\n"
                + user + " dnia " + date + "\n" + "Czy chcesz nadpisać modyfikację?");
    }

    // Handler for save button.
    // Sends request to server for last modification info.
    // If user clicks OK button data is saved else
    // data is reloaded in modal window.
    function saveButtonHandler(button, fields) {
        var key = getCommuneWithProvince(button);
        var commune = key.split("_")[0];
        var province = key.split("_")[1];
        $.ajax({
            url: '/api/last_mod/',
            type: 'GET',
            contentType: 'json',
            data: {commune: commune, province: province},
            'success': function(resp) {
                var ret = showDialogBox(resp, fields);
                if (ret == true) {
                    var data = prepareDataToSend(fields);
                    sendChanges(JSON.stringify(data), button, fields);
                } else {
                    updateRow(button, fields);
                }
            }
        });
    }

    // Changes button for "Modyfikuj" and "Zapisz".
    // Checks whether you can start updating.
    function buttonClickHandler(button) {
        var splitted = button.id.split('_');
        var id = splitted[2];
        var class_name = 'data_change_' + id;
        var fields = document.getElementsByClassName(class_name);
        var button_text = document.getElementById(button.id).innerHTML;
        if (button_text.localeCompare("Modyfikuj") == 0) {
            updateRow(button, fields);
        } else if (button_text.localeCompare("Zapisz") == 0) {
            saveButtonHandler(button, fields);
        }
    }

    function getCommuneWithProvince(button) {
        var splitted = button.id.split('_');
        var id = splitted[2];
        var class_name = 'data_change_' + id;
        var fields = document.getElementsByClassName(class_name);
        var key = '';
        for (var j = 0; j < fields.length; j++) {
            // Header is in disable_input_data
            if ($.inArray(headers[j], disableInputData) != -1) {
                key += fields[j].innerHTML + '_';
            }
        }
        return key;
    }

    // Handler for button's function onClick.
    function modalButtonsControl(i) {
        $('#modal_table').on('click', '#button_change_' + i, function() {
            var button = this;
            // Check whether user is logged in.
            $.ajax({
                url: '/user/isLogged/',
                type: 'GET',
                'success': function(resp) {
                    if(resp === "True") {
                        buttonClickHandler(button);
                    } else {
                        alert("Musisz być zalogowany, aby móc zmieniać wyniki.")
                    }
                }
            });
        });
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // Send data to server and changes text for input if response is positive.
    // Method uses POST so we need to send CSRF token.
    function sendChanges( data, button, fields) {
        var csrftoken = Cookies.get('csrftoken');
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/update_results/', true);
        xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
        //xhr.setRequestHeader("Content-length", data.length);
        //xhr.setRequestHeader("Connection", "close");
        if (!csrfSafeMethod('POST') && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }

        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                if (xhr.responseText === 'Zmiany zostały wprowadzone.') {
                    inputForText(fields);
                    button.innerHTML = "Modyfikuj";
                }
                alert(xhr.responseText);
            } else if (xhr.readyState == 4 && xhr.status != 200) {
                alert("Error " + xhr.status + "\n" + xhr.responseText);
            }
        };
        xhr.send(data);
    }

    // Changes input for text.
    function inputForText ( fields ) {
        for (var j = 0; j < fields.length; j++) {
            if ($.inArray(headers[j], disableInputData) == -1) {
                fields[j].innerHTML = fields[j].childNodes[0].value;
            }
        }
    }

    // Run whole action for modal view.
    function run() {
        var cells = document.getElementsByClassName('col5');
        for (var i = 0; i < cells.length; i++) {
            cells[i].onclick = function (event) {
                var target = event.target || event.srcElement;
                while (target && target.nodeName != 'SPAN') {
                    target = target.parentElement;
                }
                if (!target) { return; } //span should be always found
                clicked = target.innerHTML;
                var title = document.getElementById('modal_title');
                title.innerHTML = "Wyniki: " + clicked;
                getData();
                modal.style.display = "block";
            }
        }
    }

    function getData () {
        // Get headers for table.
        $.ajax({
            url: '/api/headers/',
            type: 'GET',
            data: {clicked: clicked},
            'success': function ( data ) {
                setHeaders(data);
            }
        });

        // Get data for table.
        $.ajax({
            url: '/api/communes/',
            type: 'GET',
            data: {clicked: clicked},
            'success': function ( data ) {
                setModalData(data);
            }
        });
    }

    // Updates row, checks if someone is updating this row, calling button action.
    function updateRow ( button, fields ) {
        var key = getCommuneWithProvince( button );
        var commune_name = key.split('_')[0];
        var province_name = key.split('_')[1];
        $.ajax({
            url: '/api/row/',
            type: 'GET',
            data: {commune_name: commune_name, province_name: province_name },
            'success': function( data ) {
                // Updates row where button was clicked.
                data = JSON.parse(data);
                console.log(data);
                for (var j = 0; j < headers.length; j++) {
                    if ($.inArray(headers[j], disableInputData) == -1) {
                        fields[j].innerHTML = data[engHeaders[j]];
                        console.log(data[engHeaders[j]]);
                    }
                }

                if (button.innerHTML === "Modyfikuj") {
                    modifyButton(button, fields);
                } else if (button.innerHTML === "Zapisz") {
                    button.innerHTML = "Modyfikuj";
                }
            }
        });
    }
});

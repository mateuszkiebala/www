$(document).ready(function(){
   getMapData();
});

/* Get percentages of each candidate in every province */
function getMapData() {
    $.ajax({
        url: '/api/map_data/',
        type: 'GET',
        'success': function (response) {
            $.each(response, function (key, val) {
                for (var i = 0; i < val.length; i++) {
                    var province = JSON.parse(val[i]);
                    localStorage.setItem(province['name'], province['value']);
                }
            });
            drawRegionsMap();
        }
    });
}
<!-- Script for commune type table -->
$(document).ready (function (){
    communeTypeTableHandler();
});

function communeTypeTableHandler() {
    loadCommuneTypes();
    getCommuneTypesTable();
}

function getCommuneTypesTable() {
    $.ajax({
        url: '/api/commune_types_table/',
        type: 'GET',
        'success': function(response) {
            var index = 1;
            $.each(response, function(key, val) {
                var jsonRow = JSON.parse(val);
                localStorage.setItem("ctt_type_name_" + index, jsonRow['type_name']);
                localStorage.setItem("ctt_valid_votes_" + index, jsonRow['valid_votes']);
                localStorage.setItem("ctt_cand0_votes_" + index, jsonRow['candidate_0_votes']);
                localStorage.setItem("ctt_cand0_per_" + index, jsonRow['candidate_0_per']);
                localStorage.setItem("ctt_cand1_votes_" + index, jsonRow['candidate_1_votes']);
                localStorage.setItem("ctt_cand1_per_" + index, jsonRow['candidate_1_per']);
                index++;
            });
            localStorage.setItem("types_count", (index - 1).toString(10));
            loadCommuneTypes();
        }
    });
}

function loadCommuneTypes() {
    var typesCount = localStorage.getItem('types_count');
    for (var i = 1; i <= typesCount; i++) {
        document.getElementById("ctt_type_name_" + i).textContent = localStorage.getItem("ctt_type_name_" + i);
        document.getElementById("ctt_valid_votes_" + i).textContent = localStorage.getItem("ctt_valid_votes_" + i);
        document.getElementById("ctt_cand0_votes_" + i).textContent = localStorage.getItem("ctt_cand0_votes_" + i);
        document.getElementById("ctt_cand0_per_" + i).textContent = localStorage.getItem("ctt_cand0_per_" + i);
        document.getElementById("ctt_cand1_votes_" + i).textContent = localStorage.getItem("ctt_cand1_votes_" + i);
        document.getElementById("ctt_cand1_per_" + i).textContent = localStorage.getItem("ctt_cand1_per_" + i);
        resizeBark(document.getElementById("ctt_bark0_" + i), localStorage.getItem("ctt_cand0_per_" + i));
        resizeBark(document.getElementById("ctt_bark1_" + i), localStorage.getItem("ctt_cand1_per_" + i));
    }
}

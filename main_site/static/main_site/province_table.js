<!-- Script for province table and bark resize -->
$(document).ready (function (){
    provinceTableHandler();
});

function provinceTableHandler() {
    loadProvinces();
    getProvincesTable();
}

function getProvincesTable() {
    $.ajax({
        url: '/api/province_table/',
        type: 'GET',
        'success': function(response) {
            var index = 1;
            $.each(response, function(key, val) {
                var jsonRow = JSON.parse(val);
                localStorage.setItem("pt_prov_name_" + index, jsonRow['province_name']);
                localStorage.setItem("pt_valid_votes_" + index, jsonRow['valid_votes']);
                localStorage.setItem("pt_cand0_votes_" + index, jsonRow['candidate_0_votes']);
                localStorage.setItem("pt_cand0_per_" + index, jsonRow['candidate_0_per']);
                localStorage.setItem("pt_cand1_votes_" + index, jsonRow['candidate_1_votes']);
                localStorage.setItem("pt_cand1_per_" + index, jsonRow['candidate_1_per']);
                index++;
            });
            localStorage.setItem("provinces_count", (index - 1).toString(10));
            loadProvinces();
        }
    });
}

function loadProvinces() {
    var provincesCount = localStorage.getItem('provinces_count');
    for (var i = 1; i <= provincesCount; i++) {
        document.getElementById("pt_prov_name_" + i).textContent = localStorage.getItem("pt_prov_name_" + i);
        document.getElementById("pt_valid_votes_" + i).textContent = localStorage.getItem("pt_valid_votes_" + i);
        document.getElementById("pt_cand0_votes_" + i).textContent = localStorage.getItem("pt_cand0_votes_" + i);
        document.getElementById("pt_cand0_per_" + i).textContent = localStorage.getItem("pt_cand0_per_" + i);
        document.getElementById("pt_cand1_votes_" + i).textContent = localStorage.getItem("pt_cand1_votes_" + i);
        document.getElementById("pt_cand1_per_" + i).textContent = localStorage.getItem("pt_cand1_per_" + i);
        resizeBark(document.getElementById("pt_bark0_" + i), localStorage.getItem("pt_cand0_per_" + i));
        resizeBark(document.getElementById("pt_bark1_" + i), localStorage.getItem("pt_cand1_per_" + i));
    }
}

function resizeBark(bark, newWidth) {
    if (bark && bark.style) {
        bark.style.width = newWidth.toString() + "%";
    }
}
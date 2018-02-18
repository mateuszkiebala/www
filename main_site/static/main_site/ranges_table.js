<!-- Script for inhabitants range table -->
$(document).ready (function (){
    rangesTableHandler();
});

function rangesTableHandler() {
    loadRanges();
    getRangesTable();
}

function getRangesTable() {
    $.ajax({
        url: '/api/ranges_table/',
        type: 'GET',
        'success': function(response) {
            var index = 1;
            $.each(response, function(key, val) {
                var jsonRow = JSON.parse(val);
                localStorage.setItem("rt_range_name_" + index, jsonRow['range_name']);
                localStorage.setItem("rt_valid_votes_" + index, jsonRow['valid_votes']);
                localStorage.setItem("rt_cand0_votes_" + index, jsonRow['candidate_0_votes']);
                localStorage.setItem("rt_cand0_per_" + index, jsonRow['candidate_0_per']);
                localStorage.setItem("rt_cand1_votes_" + index, jsonRow['candidate_1_votes']);
                localStorage.setItem("rt_cand1_per_" + index, jsonRow['candidate_1_per']);
                index++;
            });
            localStorage.setItem("ranges_count", (index - 1).toString(10));
            loadRanges();
        }
    });
}

function loadRanges() {
    var rangesCount = localStorage.getItem('ranges_count');
    for (var i = 1; i <= rangesCount; i++) {
        document.getElementById("rt_range_name_" + i).textContent = localStorage.getItem("rt_range_name_" + i);
        document.getElementById("rt_valid_votes_" + i).textContent = localStorage.getItem("rt_valid_votes_" + i);
        document.getElementById("rt_cand0_votes_" + i).textContent = localStorage.getItem("rt_cand0_votes_" + i);
        document.getElementById("rt_cand0_per_" + i).textContent = localStorage.getItem("rt_cand0_per_" + i);
        document.getElementById("rt_cand1_votes_" + i).textContent = localStorage.getItem("rt_cand1_votes_" + i);
        document.getElementById("rt_cand1_per_" + i).textContent = localStorage.getItem("rt_cand1_per_" + i);
        resizeBark(document.getElementById("rt_bark0_" + i), localStorage.getItem("rt_cand0_per_" + i));
        resizeBark(document.getElementById("rt_bark1_" + i), localStorage.getItem("rt_cand1_per_" + i));
    }
        }
